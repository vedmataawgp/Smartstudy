from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Doubt(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='doubts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='assigned_doubts', limit_choices_to={'role__name': 'teacher'})
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def resolve(self, resolution_text, teacher):
        self.status = 'resolved'
        self.resolution = resolution_text
        self.teacher = teacher
        self.resolved_at = timezone.now()
        self.save()
    
    def assign_to_teacher(self, teacher):
        self.teacher = teacher
        self.status = 'in_progress'
        self.save()
    
    @property
    def is_resolved(self):
        return self.status == 'resolved'
    
    @property
    def time_since_submission(self):
        return timezone.now() - self.created_at