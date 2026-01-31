from django import forms
from django.contrib.auth import get_user_model
from .models import Sale, Supplier

User = get_user_model()

class SaleFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'rounded-lg border-slate-200 text-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False,
        empty_label="All Suppliers",
        widget=forms.Select(attrs={
            'class': 'rounded-lg border-slate-200 text-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )
    ticket_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Sale.TicketType.choices,
        required=False,
        widget=forms.Select(attrs={
            'class': 'rounded-lg border-slate-200 text-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )
    currency = forms.ChoiceField(
        choices=[('', 'All Currencies')] + Sale.Currency.choices,
        required=False,
        label='Currency',
        widget=forms.Select(attrs={
            'class': 'rounded-lg border-slate-200 text-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add salesman filter for admins/accountants
        if user and (user.is_super_admin() or user.is_accountant()):
            self.fields['salesman'] = forms.ModelChoiceField(
                queryset=User.objects.filter(role=User.Role.SALESMAN),
                required=False,
                empty_label="All Salesmen",
                widget=forms.Select(attrs={
                    'class': 'rounded-lg border-slate-200 text-sm focus:ring-blue-500 focus:border-blue-500'
                })
            )
