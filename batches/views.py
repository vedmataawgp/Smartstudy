from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, View
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import (Batch, BatchSubject, BatchEnrollment, Order, Lecture, DPP, DPPAttempt, 
                     DPPAnswer, DPPSolution, Comment)
from referrals.models import ReferralCode, SalesExecutive

class BatchListView(ListView):
    model = Batch
    template_name = 'batches/list.html'
    context_object_name = 'batches'
    
    def get_queryset(self):
        return Batch.objects.filter(is_active=True).select_related('category')

class BatchDetailView(DetailView):
    model = Batch
    template_name = 'batches/detail.html'
    context_object_name = 'batch'
    pk_url_kwarg = 'batch_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = BatchEnrollment.objects.filter(
                user=self.request.user, batch=self.object, is_active=True
            ).exists()
        return context

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = BatchSubject
    template_name = 'batches/subject_detail.html'
    context_object_name = 'subject'
    pk_url_kwarg = 'subject_id'
    
    def dispatch(self, request, *args, **kwargs):
        subject = get_object_or_404(BatchSubject, id=kwargs['subject_id'])
        if not BatchEnrollment.objects.filter(user=request.user, batch=subject.batch, is_active=True).exists():
            messages.error(request, 'You need to enroll in this batch to access content.')
            return redirect('batches:detail', batch_id=subject.batch.id)
        return super().dispatch(request, *args, **kwargs)

class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'batches/lecture_detail.html'
    context_object_name = 'lecture'
    pk_url_kwarg = 'lecture_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lecture = self.object
        
        # Get comments for this lecture
        comments = Comment.objects.filter(
            content_type='lecture',
            object_id=lecture.id,
            parent=None,
            is_active=True
        ).select_related('user').prefetch_related('replies__user')
        
        context['comments'] = comments
        return context

class DPPDetailView(LoginRequiredMixin, DetailView):
    model = DPP
    template_name = 'batches/dpp_detail.html'
    context_object_name = 'dpp'
    pk_url_kwarg = 'dpp_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_attempts = DPPAttempt.objects.filter(
            user=self.request.user,
            dpp=self.object
        ).order_by('-started_at')
        
        context.update({
            'user_attempts': user_attempts,
            'questions_count': self.object.questions.count(),
            'has_attempted': user_attempts.exists(),
        })
        return context

class StartDPPView(LoginRequiredMixin, View):
    def post(self, request, dpp_id):
        dpp = get_object_or_404(DPP, id=dpp_id, is_active=True)
        
        attempt = DPPAttempt.objects.create(
            user=request.user,
            dpp=dpp,
            total_marks=dpp.total_marks,
            started_at=timezone.now()
        )
        
        # Create answer records for all questions
        questions = dpp.questions.all()
        for question in questions:
            DPPAnswer.objects.create(
                attempt=attempt,
                question=question
            )
        
        return redirect('batches:take_dpp', attempt_id=attempt.id)

class TakeDPPView(LoginRequiredMixin, TemplateView):
    template_name = 'batches/take_dpp.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = get_object_or_404(DPPAttempt, id=kwargs['attempt_id'], user=self.request.user)
        
        if attempt.completed_at:
            return redirect('batches:dpp_results', attempt_id=attempt.id)
        
        questions = attempt.dpp.questions.all().order_by('order_index')
        answers = DPPAnswer.objects.filter(attempt=attempt).select_related('question')
        answer_dict = {answer.question_id: answer for answer in answers}
        
        context.update({
            'attempt': attempt,
            'questions': questions,
            'answer_dict': answer_dict,
        })
        return context
    
    def post(self, request, attempt_id):
        attempt = get_object_or_404(DPPAttempt, id=attempt_id, user=request.user)
        
        if attempt.completed_at:
            return redirect('batches:dpp_results', attempt_id=attempt.id)
        
        total_score = 0
        with transaction.atomic():
            for question in attempt.dpp.questions.all():
                answer_key = f'question_{question.id}'
                selected_answer = request.POST.get(answer_key)
                
                if selected_answer:
                    dpp_answer = DPPAnswer.objects.get(
                        attempt=attempt,
                        question=question
                    )
                    dpp_answer.selected_answer = selected_answer
                    dpp_answer.save()
                    
                    if dpp_answer.is_correct:
                        total_score += dpp_answer.marks_obtained
            
            # Update attempt
            attempt.score = total_score
            attempt.completed_at = timezone.now()
            if attempt.total_marks > 0:
                attempt.percentage = (total_score / attempt.total_marks) * 100
            
            time_taken = (attempt.completed_at - attempt.started_at).total_seconds() / 60
            attempt.time_taken_minutes = int(time_taken)
            attempt.save()
        
        return redirect('batches:dpp_results', attempt_id=attempt.id)

class DPPResultsView(LoginRequiredMixin, DetailView):
    model = DPPAttempt
    template_name = 'batches/dpp_results.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_queryset(self):
        return DPPAttempt.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.object.answers.select_related('question').all()
        context['answers'] = answers
        return context

class DPPSolutionView(LoginRequiredMixin, DetailView):
    model = DPPSolution
    template_name = 'batches/dpp_solution.html'
    context_object_name = 'solution'
    pk_url_kwarg = 'solution_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solution = self.object
        
        # Get comments for this solution
        comments = Comment.objects.filter(
            content_type='solution',
            object_id=solution.id,
            parent=None,
            is_active=True
        ).select_related('user').prefetch_related('replies__user')
        
        context['comments'] = comments
        return context

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        
        if not all([content_type, object_id, text]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
        
        comment = Comment.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            text=text,
            parent=parent
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'user': comment.user.get_full_name() or comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'likes_count': 0,
                'dislikes_count': 0
            }
        })

class ToggleCommentLikeView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        action = request.POST.get('action')  # 'like' or 'dislike'
        
        if action == 'like':
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)
                liked = False
            else:
                comment.likes.add(request.user)
                comment.dislikes.remove(request.user)
                liked = True
        elif action == 'dislike':
            if request.user in comment.dislikes.all():
                comment.dislikes.remove(request.user)
                disliked = False
            else:
                comment.dislikes.add(request.user)
                comment.likes.remove(request.user)
                disliked = True
        
        return JsonResponse({
            'likes_count': comment.likes_count,
            'dislikes_count': comment.dislikes_count,
            'user_liked': request.user in comment.likes.all(),
            'user_disliked': request.user in comment.dislikes.all()
        })

# Existing views from previous implementation
class EnrollBatchView(LoginRequiredMixin, TemplateView):
    def post(self, request, batch_id):
        batch = get_object_or_404(Batch, id=batch_id, is_active=True)
        
        if BatchEnrollment.objects.filter(user=request.user, batch=batch, is_active=True).exists():
            messages.info(request, 'You are already enrolled in this batch.')
            return redirect('batches:my_batches')
        
        if batch.is_free:
            BatchEnrollment.objects.create(user=request.user, batch=batch)
            messages.success(request, f'Successfully enrolled in {batch.name}!')
            return redirect('batches:my_batches')
        else:
            return redirect('batches:purchase', batch_id=batch.id)

class ValidateReferralView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        referral_code = data.get('referral_code')
        batch_price = float(data.get('batch_price', 0))
        
        try:
            referral = ReferralCode.objects.get(code=referral_code, is_active=True)
            discount_amount = (batch_price * referral.discount_percentage) / 100
            
            return JsonResponse({
                'valid': True,
                'discount_percentage': float(referral.discount_percentage),
                'discount_amount': discount_amount,
                'sales_executive': referral.sales_executive.user.get_full_name()
            })
        except ReferralCode.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid referral code'
            })

class PurchaseBatchView(LoginRequiredMixin, TemplateView):
    template_name = 'batches/purchase.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = get_object_or_404(Batch, id=kwargs['batch_id'], is_active=True)
        context['batch'] = batch
        return context
    
    def post(self, request, batch_id):
        batch = get_object_or_404(Batch, id=batch_id, is_active=True)
        payment_mode = request.POST.get('payment_mode', 'card')
        referral_code = request.POST.get('referral_code', '').strip()
        
        original_amount = batch.price
        discount_amount = 0
        sales_executive = None
        
        if referral_code:
            try:
                referral = ReferralCode.objects.get(code=referral_code, is_active=True)
                discount_amount = (original_amount * referral.discount_percentage) / 100
                sales_executive = referral.sales_executive
            except ReferralCode.DoesNotExist:
                messages.error(request, 'Invalid referral code')
                return redirect('batches:purchase', batch_id=batch.id)
        
        final_amount = original_amount - discount_amount
        
        order = Order.objects.create(
            user=request.user,
            batch=batch,
            original_amount=original_amount,
            discount_amount=discount_amount,
            amount=final_amount,
            referral_code=referral_code,
            sales_executive=sales_executive,
            payment_mode=payment_mode,
            payment_status='successful',
            payment_date=timezone.now()
        )
        
        BatchEnrollment.objects.create(user=request.user, batch=batch)
        messages.success(request, f'Payment successful! Order ID: {order.order_id}')
        return redirect('batches:order_detail', order_id=order.order_id)

class MyBatchesView(LoginRequiredMixin, TemplateView):
    template_name = 'batches/my_batches.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = BatchEnrollment.objects.filter(
            user=self.request.user, is_active=True
        ).select_related('batch__category')
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'batches/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)