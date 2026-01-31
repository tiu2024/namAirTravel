from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Sale, Supplier

from .forms import SaleFilterForm

class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'agency/sales_list.html'
    context_object_name = 'sales'
    ordering = ['-date']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Base role filtering
        if user.is_super_admin() or user.is_accountant():
            pass # Access to all sales
        elif user.is_salesman():
            queryset = queryset.filter(salesman=user)
        else:
            return queryset.none()

        # Apply Form Filters
        form = SaleFilterForm(self.request.GET, user=user)
        print(f"DEBUG: GET params: {self.request.GET}")
        if form.is_valid():
            if form.cleaned_data.get('date'):
                queryset = queryset.filter(date=form.cleaned_data['date'])
            if form.cleaned_data.get('supplier'):
                queryset = queryset.filter(supplier=form.cleaned_data['supplier'])
            if form.cleaned_data.get('ticket_type'):
                queryset = queryset.filter(ticket_type=form.cleaned_data['ticket_type'])
            if form.cleaned_data.get('currency'):
                queryset = queryset.filter(sold_currency=form.cleaned_data['currency'])
            if form.cleaned_data.get('salesman'):
                queryset = queryset.filter(salesman=form.cleaned_data['salesman'])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Re-bind form with GET data to show selected values (and errors if any)
        context['form'] = SaleFilterForm(self.request.GET, user=self.request.user)
        
        # Calculate totals using self.object_list (already filtered)
        # Note: self.object_list is available because this is called after get_queryset()
        totals = self.object_list.aggregate(
            total_uzs=Sum('profit_uzs'),
            total_usd=Sum('profit_usd')
        )
        context['total_profit_uzs'] = totals['total_uzs'] or 0
        context['total_profit_usd'] = totals['total_usd'] or 0
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.htmx:
            return render(request, 'agency/partials/sales_table.html', context)
        return self.render_to_response(context)


class SupplierBalanceView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'agency/supplier_balance.html'
    context_object_name = 'sales'
    ordering = ['-date']
    paginate_by = 20

    def get_queryset(self):
        return Sale.objects.filter(supplier_id=self.kwargs['pk']).order_by('-date')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We need to fetch the supplier instance
        # Since we might not have fetched it in get_queryset (optimized query), let's get it here or store it in self
        # Better: get_object_or_404 in dispatch or get_queryset? 
        # Simpler: just get it.
        from django.shortcuts import get_object_or_404
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        context['supplier'] = supplier
        return context
