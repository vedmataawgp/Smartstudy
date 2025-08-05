from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
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
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    class_level = models.CharField(max_length=10, choices=CLASS_CHOICES)
    stream = models.CharField(max_length=20, choices=STREAM_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['name', 'class_level', 'stream']
        ordering = ['class_level', 'stream', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.class_level} {self.stream}"

class Chapter(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order_index = models.PositiveIntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order_index', 'name']
        unique_together = ['subject', 'order_index']
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    order_index = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lectures')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order_index', 'title']
    
    def __str__(self):
        return f"{self.chapter.name} - {self.title}"

class PDF(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='pdfs')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.lecture.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='progress_records')
    watched_duration = models.PositiveIntegerField(default=0, help_text="Duration in seconds")
    is_completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'lecture']
    
    def __str__(self):
        return f"{self.user.username} - {self.lecture.title}"

class Enrollment(models.Model):
    COURSE_TYPES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course_type = models.CharField(max_length=50, choices=COURSE_TYPES)
    class_level = models.CharField(max_length=10)
    stream = models.CharField(max_length=20)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    enrolled_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course_type} - {self.class_level} {self.stream}"
    
    @property
    def is_active(self):
        if self.expires_at:
            return timezone.now() < self.expires_at
        return True