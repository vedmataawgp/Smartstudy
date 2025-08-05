from django.contrib import admin
from .models import (Category, Batch, BatchSubject, Lecture, DPP, DPPQuestion, 
                     DPPSolution, DPPAttempt, Comment, BatchEnrollment, Order)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class BatchSubjectInline(admin.TabularInline):
    model = BatchSubject
    extra = 1
    fields = ['name', 'description', 'order_index']

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_free', 'is_active', 'created_at']
    list_filter = ['category', 'is_free', 'is_active']
    search_fields = ['name', 'category__name']
    inlines = [BatchSubjectInline]

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1
    fields = ['day_number', 'topic_name', 'video_type', 'video_url', 'duration_minutes']

@admin.register(BatchSubject)
class BatchSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'batch', 'order_index']
    list_filter = ['batch']
    search_fields = ['name', 'batch__name']
    inlines = [LectureInline]

class DPPInline(admin.StackedInline):
    model = DPP
    extra = 0
    fields = ['title', 'time_limit_minutes', 'is_active']

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['topic_name', 'subject', 'day_number', 'video_type', 'duration_minutes', 'is_active']
    list_filter = ['subject__batch', 'video_type', 'is_active']
    search_fields = ['topic_name', 'subject__name']
    inlines = [DPPInline]

class DPPQuestionInline(admin.TabularInline):
    model = DPPQuestion
    extra = 1
    fields = ['question_text', 'question_type', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'marks']

@admin.register(DPP)
class DPPAdmin(admin.ModelAdmin):
    list_display = ['title', 'lecture', 'time_limit_minutes', 'total_marks', 'is_active']
    list_filter = ['lecture__subject__batch', 'is_active']
    search_fields = ['title', 'lecture__topic_name']
    inlines = [DPPQuestionInline]

@admin.register(DPPQuestion)
class DPPQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'dpp', 'question_type', 'marks', 'order_index']
    list_filter = ['question_type', 'dpp__lecture__subject__batch']
    search_fields = ['question_text']

@admin.register(DPPSolution)
class DPPSolutionAdmin(admin.ModelAdmin):
    list_display = ['dpp', 'video_type', 'created_at']
    list_filter = ['video_type', 'dpp__lecture__subject__batch']

@admin.register(DPPAttempt)
class DPPAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'dpp', 'score', 'total_marks', 'percentage', 'completed_at']
    list_filter = ['dpp__lecture__subject__batch', 'completed_at']
    search_fields = ['user__username', 'dpp__title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'text', 'likes_count', 'created_at', 'is_active']
    list_filter = ['content_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'text']

@admin.register(BatchEnrollment)
class BatchEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'batch', 'enrolled_at', 'is_active']
    list_filter = ['batch', 'is_active', 'enrolled_at']
    search_fields = ['user__username', 'batch__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'batch', 'amount', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'payment_mode', 'created_at']
    search_fields = ['order_id', 'user__username', 'batch__name']
    readonly_fields = ['order_id', 'created_at']