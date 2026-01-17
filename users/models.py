from django.contrib.auth.models import AbstractUser
from django.db import models

class AirShopUser(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        SALESMAN = 'SALESMAN', 'Salesman'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SALESMAN
    )

    def is_super_admin(self):
        return self.is_superuser or self.role == self.Role.SUPER_ADMIN

    def is_accountant(self):
        return self.role == self.Role.ACCOUNTANT
    
    def is_salesman(self):
        return self.role == self.Role.SALESMAN
