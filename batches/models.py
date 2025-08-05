from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
import re

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='batches')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"

class BatchSubject(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order_index = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order_index', 'name']
        unique_together = ['batch', 'name']
    
    def __str__(self):
        return f"{self.batch.name} - {self.name}"

class Lecture(models.Model):
    VIDEO_TYPES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('drive', 'Google Drive'),
        ('upload', 'Upload'),
        ('url', 'Direct URL'),
    ]
    
    subject = models.ForeignKey(BatchSubject, on_delete=models.CASCADE, related_name='lectures')
    day_number = models.PositiveIntegerField()
    topic_name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    # Video fields
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES, default='youtube')
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo/Drive URL or direct video URL")
    video_file = models.FileField(upload_to='lectures/videos/', blank=True, null=True)
    
    # PDF field
    lecture_pdf = models.FileField(upload_to='lectures/pdfs/', blank=True, null=True)
    
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['day_number']
        unique_together = ['subject', 'day_number']
    
    def __str__(self):
        return f"Day {self.day_number}: {self.topic_name}"
    
    def get_embed_url(self):
        if self.video_type == 'youtube' and self.video_url:
            video_id = self.extract_youtube_id(self.video_url)
            return f"https://www.youtube.com/embed/{video_id}" if video_id else None
        elif self.video_type == 'vimeo' and self.video_url:
            video_id = self.extract_vimeo_id(self.video_url)
            return f"https://player.vimeo.com/video/{video_id}" if video_id else None
        elif self.video_type == 'drive' and self.video_url:
            file_id = self.extract_drive_id(self.video_url)
            return f"https://drive.google.com/file/d/{file_id}/preview" if file_id else None
        return self.video_url
    
    def extract_youtube_id(self, url):
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def extract_vimeo_id(self, url):
        match = re.search(r'vimeo\.com\/(\d+)', url)
        return match.group(1) if match else None
    
    def extract_drive_id(self, url):
        patterns = [
            r'drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

class DPP(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name='dpp')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(default=60)
    total_marks = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"DPP - {self.lecture.topic_name}"

class DPPQuestion(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('numerical', 'Numerical'),
        ('true_false', 'True/False'),
    ]
    
    dpp = models.ForeignKey(DPP, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    
    # MCQ Options
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    
    correct_answer = models.CharField(max_length=100)
    explanation = models.TextField(blank=True)
    marks = models.PositiveIntegerField(default=1)
    order_index = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order_index']
    
    def __str__(self):
        return f"Q{self.order_index}: {self.question_text[:50]}"

class DPPSolution(models.Model):
    VIDEO_TYPES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('drive', 'Google Drive'),
        ('upload', 'Upload'),
        ('url', 'Direct URL'),
    ]
    
    dpp = models.OneToOneField(DPP, on_delete=models.CASCADE, related_name='solution')
    
    # Solution PDF
    solution_pdf = models.FileField(upload_to='dpp/solutions/pdfs/', blank=True, null=True)
    
    # Solution Video
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES, default='youtube')
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='dpp/solutions/videos/', blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Solution - {self.dpp.title}"
    
    def get_embed_url(self):
        if self.video_type == 'youtube' and self.video_url:
            video_id = self.extract_youtube_id(self.video_url)
            return f"https://www.youtube.com/embed/{video_id}" if video_id else None
        elif self.video_type == 'vimeo' and self.video_url:
            video_id = self.extract_vimeo_id(self.video_url)
            return f"https://player.vimeo.com/video/{video_id}" if video_id else None
        elif self.video_type == 'drive' and self.video_url:
            file_id = self.extract_drive_id(self.video_url)
            return f"https://drive.google.com/file/d/{file_id}/preview" if file_id else None
        return self.video_url
    
    def extract_youtube_id(self, url):
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def extract_vimeo_id(self, url):
        match = re.search(r'vimeo\.com\/(\d+)', url)
        return match.group(1) if match else None
    
    def extract_drive_id(self, url):
        patterns = [
            r'drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

class DPPAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dpp_attempts')
    dpp = models.ForeignKey(DPP, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken_minutes = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.dpp.title} - {self.score}/{self.total_marks}"

class DPPAnswer(models.Model):
    attempt = models.ForeignKey(DPPAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(DPPQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def save(self, *args, **kwargs):
        if self.selected_answer:
            self.is_correct = self.selected_answer == self.question.correct_answer
            self.marks_obtained = self.question.marks if self.is_correct else 0
        super().save(*args, **kwargs)

class Comment(models.Model):
    CONTENT_TYPES = [
        ('lecture', 'Lecture'),
        ('solution', 'DPP Solution'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_comments')
    dislikes = models.ManyToManyField(User, blank=True, related_name='disliked_comments')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def dislikes_count(self):
        return self.dislikes.count()

class BatchEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batch_enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'batch']
    
    def __str__(self):
        return f"{self.user.username} - {self.batch.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_MODES = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='orders')
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    sales_executive = models.ForeignKey('referrals.SalesExecutive', on_delete=models.SET_NULL, null=True, blank=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, default='card')
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"SS{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"