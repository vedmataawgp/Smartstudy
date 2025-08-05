from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from batches.models import Order
from .models import SalesExecutive, ReferralCode

class SalesExecutiveDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'referrals/executive_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_sales_executive:
            return redirect('main:index')
        try:
            self.sales_executive = request.user.sales_executive
        except:
            self.sales_executive = None
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.sales_executive:
            # Get all orders for this sales executive
            all_orders = Order.objects.filter(sales_executive=self.sales_executive)
            
            # Successful orders (enrolled students)
            enrolled_orders = all_orders.filter(payment_status='successful')
            
            # Pending orders
            pending_orders = all_orders.filter(payment_status='pending')
            
            # Failed/cancelled orders
            cancelled_orders = all_orders.filter(payment_status='failed')
            
            # Statistics
            total_revenue = enrolled_orders.aggregate(Sum('amount'))['amount__sum'] or 0
            total_discount_given = enrolled_orders.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
            active_referral_codes = self.sales_executive.referral_codes.filter(is_active=True)
        else:
            enrolled_orders = pending_orders = cancelled_orders = Order.objects.none()
            total_revenue = total_discount_given = 0
            active_referral_codes = []
        
        context.update({
            'sales_executive': self.sales_executive,
            'enrolled_orders': enrolled_orders.select_related('user', 'batch'),
            'pending_orders': pending_orders.select_related('user', 'batch'),
            'cancelled_orders': cancelled_orders.select_related('user', 'batch'),
            'total_enrolled': enrolled_orders.count(),
            'total_pending': pending_orders.count(),
            'total_cancelled': cancelled_orders.count(),
            'total_revenue': total_revenue,
            'total_discount_given': total_discount_given,
            'active_referral_codes': active_referral_codes,
        })
        
        return context

class SalesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'referrals/sales_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all sales executives with their stats
        sales_executives = SalesExecutive.objects.filter(is_active=True)
        
        sales_data = []
        for executive in sales_executives:
            orders = Order.objects.filter(
                sales_executive=executive,
                payment_status='successful'
            )
            
            total_sales = orders.aggregate(
                total_amount=Sum('amount'),
                total_orders=Count('id')
            )
            
            sales_data.append({
                'executive': executive,
                'total_amount': total_sales['total_amount'] or 0,
                'total_orders': total_sales['total_orders'] or 0,
                'referral_codes': executive.referral_codes.filter(is_active=True).count()
            })
        
        # Overall stats
        total_referral_orders = Order.objects.filter(
            referral_code__isnull=False,
            payment_status='successful'
        ).count()
        
        total_referral_revenue = Order.objects.filter(
            referral_code__isnull=False,
            payment_status='successful'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        context.update({
            'sales_data': sales_data,
            'total_referral_orders': total_referral_orders,
            'total_referral_revenue': total_referral_revenue,
        })
        
        return context