from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('dashboard/', views.SalesExecutiveDashboardView.as_view(), name='executive_dashboard'),
    path('sales-dashboard/', views.SalesDashboardView.as_view(), name='sales_dashboard'),
]