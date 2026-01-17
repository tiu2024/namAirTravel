from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Account(models.Model):
    class Type(models.TextChoices):
        CASH_UZS = 'CASH_UZS', 'Cash UZS'
        UZCARD = 'UZCARD', 'Uzcard'
        HUMO = 'HUMO', 'Humo'
        VISA = 'VISA', 'Visa'
        MASTERCARD = 'MASTERCARD', 'Mastercard'
        CASH_USD = 'CASH_USD', 'Cash USD'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type.choices)
    currency = models.CharField(max_length=3, choices=Currency.choices, editable=False)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Auto-set currency based on type
        if self.type in [self.Type.CASH_UZS, self.Type.UZCARD, self.Type.HUMO]:
            self.currency = self.Currency.UZS
        else:
            self.currency = self.Currency.USD
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    balance_uzs = models.DecimalField(max_digits=14, decimal_places=2, default=0, help_text="Amount we owe supplier in UZS")
    balance_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0, help_text="Amount we owe supplier in USD")

    def __str__(self):
        return self.name

class Agent(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    balance_uzs = models.DecimalField(max_digits=14, decimal_places=2, default=0, help_text="Amount agent owes us in UZS")
    balance_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0, help_text="Amount agent owes us in USD")

    def __str__(self):
        return self.name

class Sale(models.Model):
    class TicketType(models.TextChoices):
        AIRTICKET = 'AIRTICKET', 'Airticket'
        TOUR = 'TOUR', 'Tour'
        UMRA = 'UMRA', 'Umra'

    class SalesChannel(models.TextChoices):
        AGENT = 'AGENT', 'Agent'
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'

    date = models.DateField(default=timezone.now)
    salesman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sales')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='sales')
    
    ticket_type = models.CharField(max_length=20, choices=TicketType.choices)
    destination = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    # Cost
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    total_purchase_cost = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    
    # Revenue
    sales_channel = models.CharField(max_length=20, choices=SalesChannel.choices)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, null=True, blank=True, related_name='purchases')
    
    sold_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    sold_currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    total_sold_price = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    
    # Profit
    profit_uzs = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)
    profit_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)
    
    comment = models.TextField(blank=True)

    def clean(self):
        if self.sales_channel == self.SalesChannel.AGENT and not self.agent:
            raise ValidationError({'agent': 'Agent is required when sales channel is Agent.'})

    def save(self, *args, **kwargs):
        self.total_purchase_cost = self.purchase_price * self.quantity
        self.total_sold_price = self.sold_price * self.quantity
        
        # Reset profits
        self.profit_uzs = 0
        self.profit_usd = 0

        # Calculate UZS profit
        revenue_uzs = self.total_sold_price if self.sold_currency == self.Currency.UZS else 0
        cost_uzs = self.total_purchase_cost if self.purchase_currency == self.Currency.UZS else 0
        self.profit_uzs = revenue_uzs - cost_uzs

        # Calculate USD profit
        revenue_usd = self.total_sold_price if self.sold_currency == self.Currency.USD else 0
        cost_usd = self.total_purchase_cost if self.purchase_currency == self.Currency.USD else 0
        self.profit_usd = revenue_usd - cost_usd

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_type} to {self.destination} ({self.date})"

class Transaction(models.Model):
    class Category(models.TextChoices):
        SALE = 'SALE', 'Sale'
        SUPPLIER_PAYMENT = 'SUPPLIER_PAYMENT', 'Supplier Payment'
        AGENT_PAYMENT = 'AGENT_PAYMENT', 'Agent Payment'
        EXPENSE = 'EXPENSE', 'Expense'
        TRANSFER = 'TRANSFER', 'Transfer'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'

    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    category = models.CharField(max_length=20, choices=Category.choices)
    
    source_account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True, related_name='outgoing_transactions')
    destination_account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True, related_name='incoming_transactions')
    sale = models.ForeignKey('Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.get_category_display()} - {self.amount} {self.currency}"

