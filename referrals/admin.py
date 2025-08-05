from django.contrib import admin
from .models import SalesExecutive, ReferralCode

@admin.register(SalesExecutive)
class SalesExecutiveAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'employee_id']

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'sales_executive', 'discount_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'sales_executive__user__username']