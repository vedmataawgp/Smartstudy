from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Doubt
from .forms import DoubtSubmissionForm, DoubtResolutionForm
from accounts.models import User

class DoubtListView(LoginRequiredMixin, ListView):
    model = Doubt
    template_name = 'doubts/list.html'
    context_object_name = 'doubts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Doubt.objects.all().select_related('user', 'teacher')
        status_filter = self.request.GET.get('status')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter based on user role
        if self.request.user.is_student:
            queryset = queryset.filter(user=self.request.user)
        elif self.request.user.is_teacher:
            queryset = queryset.filter(
                Q(teacher=self.request.user) | Q(status='submitted')
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'status_choices': Doubt.STATUS_CHOICES,
            'selected_status': self.request.GET.get('status', ''),
        })
        return context

class SubmitDoubtView(LoginRequiredMixin, CreateView):
    model = Doubt
    form_class = DoubtSubmissionForm
    template_name = 'doubts/submit.html'
    success_url = reverse_lazy('doubts:my_doubts')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Doubt submitted successfully!')
        return super().form_valid(form)

class DoubtDetailView(LoginRequiredMixin, DetailView):
    model = Doubt
    template_name = 'doubts/detail.html'
    context_object_name = 'doubt'
    pk_url_kwarg = 'doubt_id'
    
    def get_queryset(self):
        # Students can only see their own doubts
        if self.request.user.is_student:
            return Doubt.objects.filter(user=self.request.user)
        # Teachers and admins can see all doubts
        return Doubt.objects.all()

class ResolveDoubtView(LoginRequiredMixin, UpdateView):
    model = Doubt
    form_class = DoubtResolutionForm
    template_name = 'doubts/resolve.html'
    pk_url_kwarg = 'doubt_id'
    
    def get_queryset(self):
        # Only teachers and admins can resolve doubts
        if self.request.user.is_teacher or self.request.user.is_admin:
            return Doubt.objects.all()
        return Doubt.objects.none()
    
    def form_valid(self, form):
        doubt = form.instance
        doubt.resolve(form.cleaned_data['resolution'], self.request.user)
        messages.success(self.request, 'Doubt resolved successfully!')
        return redirect('doubts:detail', doubt_id=doubt.id)
    
    def get_success_url(self):
        return reverse_lazy('doubts:detail', kwargs={'doubt_id': self.object.id})

class MyDoubtsView(LoginRequiredMixin, ListView):
    model = Doubt
    template_name = 'doubts/my_doubts.html'
    context_object_name = 'doubts'
    paginate_by = 20
    
    def get_queryset(self):
        return Doubt.objects.filter(user=self.request.user).order_by('-created_at')

class TeacherDoubtDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'doubts/teacher_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher and not request.user.is_admin:
            messages.error(request, 'Access denied. Teachers only.')
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'pending_doubts': Doubt.objects.filter(status='submitted').order_by('-created_at'),
            'my_assigned_doubts': Doubt.objects.filter(
                teacher=self.request.user,
                status='in_progress'
            ).order_by('-created_at'),
            'recently_resolved': Doubt.objects.filter(
                teacher=self.request.user,
                status='resolved'
            ).order_by('-resolved_at')[:10],
            'total_pending': Doubt.objects.filter(status='submitted').count(),
            'total_assigned': Doubt.objects.filter(
                teacher=self.request.user,
                status='in_progress'
            ).count(),
            'total_resolved': Doubt.objects.filter(
                teacher=self.request.user,
                status='resolved'
            ).count(),
        })
        return context
    
    def post(self, request):
        # Handle doubt assignment to teacher
        doubt_id = request.POST.get('doubt_id')
        action = request.POST.get('action')
        
        if action == 'assign_to_me':
            doubt = get_object_or_404(Doubt, id=doubt_id, status='submitted')
            doubt.assign_to_teacher(request.user)
            messages.success(request, f'Doubt "{doubt.title}" assigned to you.')
        
        return redirect('doubts:teacher_dashboard')