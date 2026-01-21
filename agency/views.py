from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Sale

class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'agency/sales_list.html'
    context_object_name = 'sales'
    ordering = ['-date']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_super_admin() or user.is_accountant():
            return queryset
        elif user.is_salesman():
            return queryset.filter(salesman=user)
        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate totals for the entire queryset (not just the page)
        queryset = self.get_queryset()
        totals = queryset.aggregate(
            total_uzs=Sum('profit_uzs'),
            total_usd=Sum('profit_usd')
        )
        context['total_profit_uzs'] = totals['total_uzs'] or 0
        context['total_profit_usd'] = totals['total_usd'] or 0
        return context

