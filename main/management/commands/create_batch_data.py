from django.core.management.base import BaseCommand
from batches.models import Category, Batch, BatchSubject, BatchChapter

class Command(BaseCommand):
    help = 'Create sample batch data'

    def handle(self, *args, **options):
        # Create categories
        cat9, _ = Category.objects.get_or_create(name='Class 9', defaults={'description': 'Class 9 courses'})
        cat10, _ = Category.objects.get_or_create(name='Class 10', defaults={'description': 'Class 10 courses'})
        cat12, _ = Category.objects.get_or_create(name='Class 12', defaults={'description': 'Class 12 courses'})
        
        # Create batches
        titans, _ = Batch.objects.get_or_create(
            name='Titans',
            category=cat9,
            defaults={'description': 'Premium batch for Class 9 students', 'price': 1299.00, 'is_free': False}
        )
        
        warriors, _ = Batch.objects.get_or_create(
            name='Warriors',
            category=cat10,
            defaults={'description': 'Free batch for Class 10 students', 'price': 0.00, 'is_free': True}
        )
        
        champions, _ = Batch.objects.get_or_create(
            name='Champions',
            category=cat12,
            defaults={'description': 'Advanced batch for Class 12 students', 'price': 1999.00, 'is_free': False}
        )
        
        # Add subjects to Titans batch
        subjects_data = [
            {'name': 'Science', 'description': 'Physics, Chemistry, Biology'},
            {'name': 'Mathematics', 'description': 'Algebra, Geometry, Statistics'},
            {'name': 'English', 'description': 'Grammar, Literature, Writing'},
        ]
        
        for i, subject_data in enumerate(subjects_data):
            subject, created = BatchSubject.objects.get_or_create(
                batch=titans,
                name=subject_data['name'],
                defaults={'description': subject_data['description'], 'order_index': i+1}
            )
            
            if created:
                # Add chapters
                for j in range(1, 4):
                    BatchChapter.objects.get_or_create(
                        subject=subject,
                        name=f'{subject.name} Chapter {j}',
                        defaults={'description': f'Chapter {j} content', 'order_index': j}
                    )
        
        self.stdout.write(self.style.SUCCESS('Batch data created successfully!'))