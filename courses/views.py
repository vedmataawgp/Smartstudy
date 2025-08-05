from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Subject, Chapter, Lecture, Progress, Enrollment

class CourseListView(ListView):
    model = Subject
    template_name = 'courses/list.html'
    context_object_name = 'subjects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        class_filter = self.request.GET.get('class')
        stream_filter = self.request.GET.get('stream')
        
        if class_filter:
            queryset = queryset.filter(class_level=class_filter)
        if stream_filter:
            queryset = queryset.filter(stream=stream_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'class_choices': Subject.CLASS_CHOICES,
            'stream_choices': Subject.STREAM_CHOICES,
            'selected_class': self.request.GET.get('class', ''),
            'selected_stream': self.request.GET.get('stream', ''),
        })
        return context

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'courses/subject_detail.html'
    context_object_name = 'subject'
    pk_url_kwarg = 'subject_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapters = self.object.chapters.prefetch_related('lectures').all()
        
        if self.request.user.is_authenticated:
            user_progress = Progress.objects.filter(
                user=self.request.user,
                lecture__chapter__subject=self.object
            ).select_related('lecture')
            progress_dict = {p.lecture_id: p for p in user_progress}
        else:
            progress_dict = {}
        
        context.update({
            'chapters': chapters,
            'progress_dict': progress_dict,
        })
        return context

class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'
    context_object_name = 'lecture'
    pk_url_kwarg = 'lecture_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create progress record
        progress, created = Progress.objects.get_or_create(
            user=self.request.user,
            lecture=self.object,
            defaults={'watched_duration': 0}
        )
        
        context.update({
            'progress': progress,
            'pdfs': self.object.pdfs.all(),
            'chapter_lectures': self.object.chapter.lectures.all(),
        })
        return context

class MarkLectureCompleteView(LoginRequiredMixin, View):
    def post(self, request, lecture_id):
        lecture = get_object_or_404(Lecture, id=lecture_id)
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            lecture=lecture
        )
        
        progress.is_completed = True
        progress.watched_duration = lecture.duration * 60 if lecture.duration else 0
        progress.last_watched = timezone.now()
        progress.save()
        
        messages.success(request, f'Lecture "{lecture.title}" marked as complete!')
        return redirect('courses:lecture_detail', lecture_id=lecture.id)

class EnrollmentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/enrollment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_enrollments = Enrollment.objects.filter(user=self.request.user)
        context['enrollments'] = user_enrollments
        return context

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get parameters from URL or session
        context.update({
            'course_type': self.request.GET.get('course_type', 'basic'),
            'class_level': self.request.GET.get('class_level', ''),
            'stream': self.request.GET.get('stream', ''),
        })
        return context
    
    def post(self, request):
        course_type = request.POST.get('course_type')
        class_level = request.POST.get('class_level')
        stream = request.POST.get('stream')
        
        # Validate required fields
        if not all([course_type, class_level, stream]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('courses:enrollment')
        
        # Payment simulation
        if course_type == 'premium':
            amount = 1299.00
        elif course_type == 'basic':
            amount = 799.00
        else:
            amount = 0.00
        
        try:
            # Create enrollment
            enrollment = Enrollment.objects.create(
                user=request.user,
                course_type=course_type,
                class_level=class_level,
                stream=stream,
                amount_paid=amount,
                payment_status='completed',
                expires_at=timezone.now() + timedelta(days=365)
            )
            
            messages.success(request, 'Payment successful! You are now enrolled.')
            return redirect('courses:payment_success')
        except Exception as e:
            messages.error(request, 'Payment processing failed. Please try again.')
            return redirect('courses:enrollment')

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/payment_success.html'