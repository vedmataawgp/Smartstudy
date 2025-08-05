from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .forms import UserRegistrationForm, CustomLoginForm, ProfileForm
from .models import User, Role
from courses.models import Progress, Enrollment
from quizzes.models import QuizAttempt
from doubts.models import Doubt

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('admin:index')
        elif user.is_teacher:
            return reverse_lazy('doubts:teacher_dashboard')
        else:
            return reverse_lazy('accounts:dashboard')

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign student role by default
        try:
            student_role = Role.objects.get(name='student')
            self.object.role = student_role
            self.object.save()
        except Role.DoesNotExist:
            pass
        
        messages.success(self.request, 'Registration successful! Please login.')
        return response

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_student:
            # Student dashboard data
            context.update({
                'total_lectures': Progress.objects.filter(user=user).count(),
                'completed_lectures': Progress.objects.filter(user=user, is_completed=True).count(),
                'quiz_attempts': QuizAttempt.objects.filter(user=user).count(),
                'pending_doubts': Doubt.objects.filter(user=user, status='submitted').count(),
                'recent_attempts': QuizAttempt.objects.filter(user=user).order_by('-started_at')[:5],
                'recent_doubts': Doubt.objects.filter(user=user).order_by('-created_at')[:5],
                'enrollments': Enrollment.objects.filter(user=user, payment_status='completed'),
            })
        elif user.is_teacher:
            # Teacher dashboard data
            context.update({
                'assigned_doubts': Doubt.objects.filter(teacher=user, status='in_progress').count(),
                'resolved_doubts': Doubt.objects.filter(teacher=user, status='resolved').count(),
                'pending_assignments': Doubt.objects.filter(status='submitted').count(),
                'recent_doubts': Doubt.objects.filter(teacher=user).order_by('-created_at')[:5],
            })
        elif user.is_admin:
            # Admin dashboard data
            context.update({
                'total_users': User.objects.count(),
                'total_students': User.objects.filter(role__name='student').count(),
                'total_teachers': User.objects.filter(role__name='teacher').count(),
                'total_doubts': Doubt.objects.count(),
                'pending_doubts': Doubt.objects.filter(status='submitted').count(),
                'recent_registrations': User.objects.order_by('-date_joined')[:5],
            })
        
        return context