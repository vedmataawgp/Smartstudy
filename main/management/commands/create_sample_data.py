from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role
from courses.models import Subject, Chapter, Lecture, PDF
from quizzes.models import Quiz, Question
from doubts.models import Doubt

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for Smart Study application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create roles
        admin_role, _ = Role.objects.get_or_create(name='admin', defaults={'description': 'Administrator'})
        teacher_role, _ = Role.objects.get_or_create(name='teacher', defaults={'description': 'Teacher'})
        student_role, _ = Role.objects.get_or_create(name='student', defaults={'description': 'Student'})
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@smartstudy.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=admin_role
            )
            self.stdout.write(f'Created admin user: admin/admin123')
        
        # Create teacher user
        if not User.objects.filter(username='teacher1').exists():
            teacher_user = User.objects.create_user(
                username='teacher1',
                email='teacher@smartstudy.com',
                password='teacher123',
                first_name='John',
                last_name='Teacher',
                role=teacher_role
            )
            self.stdout.write(f'Created teacher user: teacher1/teacher123')
        
        # Create student user
        if not User.objects.filter(username='student1').exists():
            student_user = User.objects.create_user(
                username='student1',
                email='student@smartstudy.com',
                password='student123',
                first_name='Jane',
                last_name='Student',
                class_level='12th',
                stream='Science',
                role=student_role
            )
            self.stdout.write(f'Created student user: student1/student123')
        
        # Create subjects
        subjects_data = [
            {'name': 'Physics', 'class_level': '12th', 'stream': 'Science', 'description': 'Advanced Physics for Class 12'},
            {'name': 'Chemistry', 'class_level': '12th', 'stream': 'Science', 'description': 'Advanced Chemistry for Class 12'},
            {'name': 'Mathematics', 'class_level': '12th', 'stream': 'Science', 'description': 'Advanced Mathematics for Class 12'},
            {'name': 'Biology', 'class_level': '12th', 'stream': 'NEET', 'description': 'Biology for NEET preparation'},
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(**subject_data)
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
                
                # Create chapters for each subject
                chapters_data = [
                    {'name': f'{subject.name} Chapter 1', 'description': f'Introduction to {subject.name}', 'order_index': 1},
                    {'name': f'{subject.name} Chapter 2', 'description': f'Advanced {subject.name} concepts', 'order_index': 2},
                ]
                
                for chapter_data in chapters_data:
                    chapter_data['subject'] = subject
                    chapter, created = Chapter.objects.get_or_create(**chapter_data)
                    if created:
                        self.stdout.write(f'Created chapter: {chapter.name}')
                        
                        # Create lectures for each chapter
                        lectures_data = [
                            {'title': f'{chapter.name} - Lecture 1', 'description': 'Introduction lecture', 'duration': 45, 'order_index': 1},
                            {'title': f'{chapter.name} - Lecture 2', 'description': 'Advanced concepts', 'duration': 50, 'order_index': 2},
                        ]
                        
                        for lecture_data in lectures_data:
                            lecture_data['chapter'] = chapter
                            lecture, created = Lecture.objects.get_or_create(**lecture_data)
                            if created:
                                self.stdout.write(f'Created lecture: {lecture.title}')
                                
                                # Create quiz for chapter
                                quiz, created = Quiz.objects.get_or_create(
                                    title=f'{chapter.name} Quiz',
                                    chapter=chapter,
                                    defaults={
                                        'description': f'Test your knowledge of {chapter.name}',
                                        'total_marks': 10,
                                        'duration': 30
                                    }
                                )
                                if created:
                                    self.stdout.write(f'Created quiz: {quiz.title}')
                                    
                                    # Create sample questions
                                    questions_data = [
                                        {
                                            'question_text': f'What is the main concept in {chapter.name}?',
                                            'option_a': 'Option A',
                                            'option_b': 'Option B',
                                            'option_c': 'Option C',
                                            'option_d': 'Option D',
                                            'correct_answer': 'A',
                                            'explanation': 'This is the correct answer because...',
                                            'marks': 2
                                        },
                                        {
                                            'question_text': f'Which formula is used in {chapter.name}?',
                                            'option_a': 'Formula A',
                                            'option_b': 'Formula B',
                                            'option_c': 'Formula C',
                                            'option_d': 'Formula D',
                                            'correct_answer': 'B',
                                            'explanation': 'Formula B is correct because...',
                                            'marks': 3
                                        }
                                    ]
                                    
                                    for question_data in questions_data:
                                        question_data['quiz'] = quiz
                                        question, created = Question.objects.get_or_create(**question_data)
                                        if created:
                                            self.stdout.write(f'Created question for quiz: {quiz.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Teacher: teacher1/teacher123')
        self.stdout.write('Student: student1/student123')