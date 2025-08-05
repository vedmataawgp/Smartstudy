from django.contrib import admin
from .models import Subject, Chapter, Lecture, PDF, Progress, Enrollment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_level', 'stream', 'created_at']
    list_filter = ['class_level', 'stream', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['class_level', 'stream', 'name']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order_index', 'created_at']
    list_filter = ['subject__class_level', 'subject__stream', 'created_at']
    search_fields = ['name', 'subject__name']
    ordering = ['subject', 'order_index']

class PDFInline(admin.TabularInline):
    model = PDF
    extra = 0

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'order_index', 'duration', 'is_free', 'created_at']
    list_filter = ['chapter__subject__class_level', 'chapter__subject__stream', 'is_free', 'created_at']
    search_fields = ['title', 'chapter__name', 'chapter__subject__name']
    ordering = ['chapter', 'order_index']
    inlines = [PDFInline]

@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ['title', 'lecture', 'file_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'lecture__title']
    readonly_fields = ['file_size']

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lecture', 'watched_duration', 'is_completed', 'last_watched']
    list_filter = ['is_completed', 'last_watched']
    search_fields = ['user__username', 'lecture__title']
    readonly_fields = ['last_watched']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course_type', 'class_level', 'stream', 'amount_paid', 'payment_status', 'enrolled_at']
    list_filter = ['course_type', 'class_level', 'stream', 'payment_status', 'enrolled_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['enrolled_at']