from django.urls import path
from .views import SalesListView, SupplierBalanceView

urlpatterns = [
    path('sales/', SalesListView.as_view(), name='sales_list'),
    path('suppliers/<int:pk>/balance/', SupplierBalanceView.as_view(), name='supplier_balance'),
]
