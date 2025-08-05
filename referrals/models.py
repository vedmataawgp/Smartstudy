from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import string
import random

User = get_user_model()

class SalesExecutive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales_executive')
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class ReferralCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    sales_executive = models.ForeignKey(SalesExecutive, on_delete=models.CASCADE, related_name='referral_codes')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)
    
    def generate_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not ReferralCode.objects.filter(code=code).exists():
                return code
    
    def __str__(self):
        return f"{self.code} - {self.sales_executive.user.get_full_name()}"