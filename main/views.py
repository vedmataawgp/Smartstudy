from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from courses.models import Subject, Lecture
from quizzes.models import Quiz

class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_subjects': Subject.objects.count(),
            'total_lectures': Lecture.objects.count(),
            'total_quizzes': Quiz.objects.count(),
            'featured_subjects': Subject.objects.all()[:6],
        })
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

class ContactView(TemplateView):
    template_name = 'main/contact.html'

class PricingView(TemplateView):
    template_name = 'main/pricing.html'

class SearchView(TemplateView):
    template_name = 'main/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            subjects = Subject.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            lectures = Lecture.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            quizzes = Quiz.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            subjects = Subject.objects.none()
            lectures = Lecture.objects.none()
            quizzes = Quiz.objects.none()
        
        context.update({
            'query': query,
            'subjects': subjects,
            'lectures': lectures,
            'quizzes': quizzes,
        })
        return context