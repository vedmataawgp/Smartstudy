from django.contrib import admin
from .models import Quiz, Question, QuizAttempt, QuizAnswer, DailyPracticeProblem

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'marks']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'total_marks', 'duration', 'is_active', 'created_at']
    list_filter = ['chapter__subject__class_level', 'chapter__subject__stream', 'is_active', 'created_at']
    search_fields = ['title', 'chapter__name', 'chapter__subject__name']
    ordering = ['-created_at']
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update total marks based on questions
        total_marks = sum(q.marks for q in obj.questions.all())
        if total_marks != obj.total_marks:
            obj.total_marks = total_marks
            obj.save()

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer', 'marks', 'created_at']
    list_filter = ['quiz__chapter__subject__class_level', 'quiz__chapter__subject__stream', 'correct_answer', 'created_at']
    search_fields = ['question_text', 'quiz__title']
    ordering = ['quiz', 'id']

class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answer', 'is_correct', 'marks_obtained']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_marks', 'percentage', 'time_taken', 'started_at', 'completed_at']
    list_filter = ['quiz__chapter__subject__class_level', 'quiz__chapter__subject__stream', 'started_at', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at', 'percentage']
    ordering = ['-started_at']
    inlines = [QuizAnswerInline]

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_answer', 'is_correct', 'marks_obtained']
    list_filter = ['is_correct', 'selected_answer']
    search_fields = ['attempt__user__username', 'question__quiz__title']
    readonly_fields = ['is_correct', 'marks_obtained']

@admin.register(DailyPracticeProblem)
class DailyPracticeProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'difficulty', 'date_assigned', 'created_at']
    list_filter = ['difficulty', 'chapter__subject__class_level', 'chapter__subject__stream', 'date_assigned']
    search_fields = ['title', 'chapter__name']
    ordering = ['-date_assigned']