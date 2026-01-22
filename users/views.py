from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_salesman():
                return reverse_lazy('sales_list')
            elif user.is_accountant():
                # For now redirect accountant to sales list as well, or a future dashboard
                return reverse_lazy('sales_list') 
            elif user.is_super_admin():
                return reverse_lazy('sales_list') # Or admin:index
        return reverse_lazy('sales_list')
