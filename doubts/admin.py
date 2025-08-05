from django.contrib import admin
from .models import Doubt

@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'teacher', 'status', 'created_at', 'resolved_at']
    list_filter = ['status', 'created_at', 'resolved_at']
    search_fields = ['title', 'user__username', 'teacher__username']
    readonly_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Doubt Information', {
            'fields': ('title', 'description', 'image', 'user')
        }),
        ('Resolution', {
            'fields': ('status', 'teacher', 'resolution', 'resolved_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields