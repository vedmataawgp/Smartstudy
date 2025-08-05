from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('sales_executive', 'Sales Executive'),
    ]
    
    name = models.CharField(max_length=64, unique=True, choices=ROLE_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    CLASS_CHOICES = [
        ('9th', '9th Grade'),
        ('10th', '10th Grade'),
        ('11th', '11th Grade'),
        ('12th', '12th Grade'),
    ]
    
    STREAM_CHOICES = [
        ('Science', 'Science'),
        ('NEET', 'NEET'),
        ('JEE', 'JEE'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    class_level = models.CharField(max_length=10, choices=CLASS_CHOICES, blank=True)
    stream = models.CharField(max_length=20, choices=STREAM_CHOICES, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_admin(self):
        return self.role and self.role.name == 'admin'
    
    @property
    def is_teacher(self):
        return self.role and self.role.name == 'teacher'
    
    @property
    def is_student(self):
        return self.role and self.role.name == 'student'
    
    @property
    def is_sales_executive(self):
        return self.role and self.role.name == 'sales_executive'

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('general', 'General'),
        ('doubt', 'Doubt'),
        ('quiz', 'Quiz'),
        ('payment', 'Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='general')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"