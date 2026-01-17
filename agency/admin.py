from django.contrib import admin
from .models import Account, Supplier, Agent, Sale, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'currency', 'balance')
    list_filter = ('type', 'currency')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance_uzs', 'balance_usd')
    search_fields = ('name',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance_uzs', 'balance_usd')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'ticket_type', 'destination', 'salesman', 'total_sold_price', 'sold_currency', 'profit_uzs', 'profit_usd')
    list_filter = ('date', 'ticket_type', 'sales_channel', 'salesman')
    search_fields = ('destination', 'comment', 'agent__name', 'supplier__name')
    readonly_fields = ('total_purchase_cost', 'total_sold_price', 'profit_uzs', 'profit_usd')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'currency', 'source_account', 'destination_account', 'sale')
    list_filter = ('date', 'category', 'currency')
    search_fields = ('description', 'sale__id')
