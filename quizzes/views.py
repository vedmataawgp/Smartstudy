from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from .models import Quiz, Question, QuizAttempt, QuizAnswer

class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quizzes/list.html'
    context_object_name = 'quizzes'
    paginate_by = 12
    
    def get_queryset(self):
        return Quiz.objects.filter(is_active=True).select_related('chapter__subject')

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quizzes/detail.html'
    context_object_name = 'quiz'
    pk_url_kwarg = 'quiz_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_attempts = QuizAttempt.objects.filter(
            user=self.request.user,
            quiz=self.object
        ).order_by('-started_at')
        
        context.update({
            'user_attempts': user_attempts,
            'questions_count': self.object.questions.count(),
            'has_attempted': user_attempts.exists(),
        })
        return context

class StartQuizView(LoginRequiredMixin, View):
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        
        # Create new attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            total_marks=quiz.total_marks,
            started_at=timezone.now()
        )
        
        # Create answer records for all questions
        questions = quiz.questions.all()
        for question in questions:
            QuizAnswer.objects.create(
                attempt=attempt,
                question=question
            )
        
        messages.success(request, f'Quiz "{quiz.title}" started successfully!')
        return redirect('quizzes:submit', quiz_id=quiz.id)

class SubmitQuizView(LoginRequiredMixin, TemplateView):
    template_name = 'quizzes/submit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = get_object_or_404(Quiz, id=kwargs['quiz_id'], is_active=True)
        
        # Get the latest attempt for this user and quiz
        attempt = QuizAttempt.objects.filter(
            user=self.request.user,
            quiz=quiz,
            completed_at__isnull=True
        ).order_by('-started_at').first()
        
        if not attempt:
            messages.error(self.request, 'No active quiz attempt found.')
            return redirect('quizzes:detail', quiz_id=quiz.id)
        
        questions = quiz.questions.all().order_by('id')
        answers = QuizAnswer.objects.filter(attempt=attempt).select_related('question')
        answer_dict = {answer.question_id: answer for answer in answers}
        
        context.update({
            'quiz': quiz,
            'attempt': attempt,
            'questions': questions,
            'answer_dict': answer_dict,
        })
        return context
    
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        
        # Get the latest attempt
        attempt = QuizAttempt.objects.filter(
            user=request.user,
            quiz=quiz,
            completed_at__isnull=True
        ).order_by('-started_at').first()
        
        if not attempt:
            messages.error(request, 'No active quiz attempt found.')
            return redirect('quizzes:detail', quiz_id=quiz.id)
        
        # Process submitted answers
        total_score = 0
        with transaction.atomic():
            for question in quiz.questions.all():
                answer_key = f'question_{question.id}'
                selected_answer = request.POST.get(answer_key)
                
                if selected_answer:
                    quiz_answer = QuizAnswer.objects.get(
                        attempt=attempt,
                        question=question
                    )
                    quiz_answer.selected_answer = selected_answer
                    quiz_answer.save()  # This will trigger the save method to set is_correct and marks
                    
                    if quiz_answer.is_correct:
                        total_score += quiz_answer.marks_obtained
            
            # Update attempt
            attempt.score = total_score
            attempt.completed_at = timezone.now()
            attempt.calculate_percentage()
            
            # Calculate time taken
            time_taken_seconds = (attempt.completed_at - attempt.started_at).total_seconds()
            attempt.time_taken = int(time_taken_seconds / 60)  # Convert to minutes
            attempt.save()
        
        messages.success(request, f'Quiz submitted successfully! Score: {total_score}/{quiz.total_marks}')
        return redirect('quizzes:results', attempt_id=attempt.id)

class QuizResultsView(LoginRequiredMixin, DetailView):
    model = QuizAttempt
    template_name = 'quizzes/results.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.object.answers.select_related('question').all()
        
        context.update({
            'answers': answers,
            'quiz': self.object.quiz,
        })
        return context

class MyAttemptsView(LoginRequiredMixin, ListView):
    model = QuizAttempt
    template_name = 'quizzes/my_attempts.html'
    context_object_name = 'attempts'
    paginate_by = 20
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(
            user=self.request.user,
            completed_at__isnull=False
        ).select_related('quiz__chapter__subject').order_by('-completed_at')