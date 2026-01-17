from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Sale, Transaction, Supplier, Agent

def create_sale(user, sale_data, payment_account=None):
    """
    Creates a Sale record and atomically updates related financial balances.
    
    Args:
        user: The user (Salesman) creating the sale.
        sale_data: Dictionary containing Sale model fields.
        payment_account: Account instance where money is received (required for Individual sales).
    
    Returns:
        The created Sale instance.
    """
    with transaction.atomic():
        # 1. Create Sale
        # We ensure 'salesman' is set to the user passed in
        sale_data['salesman'] = user
        sale = Sale.objects.create(**sale_data)

        # 2. Update Supplier Balance (We owe them)
        # We assume Purchase Price is always "We owe supplier"
        supplier = sale.supplier
        if sale.purchase_currency == Sale.Currency.UZS:
            supplier.balance_uzs += sale.total_purchase_cost
        else:
            supplier.balance_usd += sale.total_purchase_cost
        supplier.save()

        # 3. Handle Client Type
        if sale.sales_channel == Sale.SalesChannel.INDIVIDUAL:
             # Logic: Individual pays immediately.
             if not payment_account:
                 raise ValidationError("Payment account is required for Individual sales.")
             
             # Validate currency consistency
             if payment_account.currency != sale.sold_currency:
                 raise ValidationError(f"Payment account currency ({payment_account.currency}) must match sale currency ({sale.sold_currency}).")
             
             Transaction.objects.create(
                 amount=sale.total_sold_price,
                 currency=sale.sold_currency,
                 category=Transaction.Category.SALE,
                 source_account=None, # Client pays (external source)
                 destination_account=payment_account, # Shop receives
                 sale=sale,
                 description=f"Sale #{sale.id} - {sale.get_ticket_type_display()} to {sale.destination} (Individual)"
             )
             
        elif sale.sales_channel == Sale.SalesChannel.AGENT:
            # Logic: Agent owes us. No cash transaction yet.
            if not sale.agent:
                raise ValidationError("Agent is required for Agent sales.")

            agent = sale.agent
            if sale.sold_currency == Sale.Currency.UZS:
                agent.balance_uzs += sale.total_sold_price
            else:
                agent.balance_usd += sale.total_sold_price
            agent.save()
            
        return sale
