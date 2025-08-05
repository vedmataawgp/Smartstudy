from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from courses.models import Chapter

User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=60, help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return f"{self.chapter.name} - {self.title}"
    
    def get_question_count(self):
        return self.questions.count()

class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True)
    marks = models.PositiveIntegerField(default=1)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.id}"
    
    def get_options(self):
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken = models.PositiveIntegerField(help_text="Time taken in minutes", null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_marks}"
    
    def calculate_percentage(self):
        if self.total_marks > 0:
            self.percentage = (self.score / self.total_marks) * 100
        else:
            self.percentage = 0.0
        return self.percentage
    
    def is_completed(self):
        return self.completed_at is not None

class QuizAnswer(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.quiz.title} - Q{self.question.id}"
    
    def save(self, *args, **kwargs):
        if self.selected_answer:
            self.is_correct = self.selected_answer == self.question.correct_answer
            self.marks_obtained = self.question.marks if self.is_correct else 0
        super().save(*args, **kwargs)

class DailyPracticeProblem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    question_text = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='practice_problems')
    created_at = models.DateTimeField(default=timezone.now)
    date_assigned = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_assigned']
    
    def __str__(self):
        return f"{self.title} - {self.chapter.name}"