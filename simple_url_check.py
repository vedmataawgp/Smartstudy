#!/usr/bin/env python
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_study.settings')
django.setup()

def check_urls():
    print("=" * 80)
    print("SMART STUDY - URL CHECK REPORT")
    print("=" * 80)
    
    # Simple URLs (no parameters)
    simple_urls = [
        'main:index',
        'main:about', 
        'main:contact',
        'main:pricing',
        'main:search',
        'accounts:login',
        'accounts:register',
        'accounts:dashboard',
        'accounts:profile',
        'accounts:logout',
        'accounts:password_reset',
        'accounts:password_reset_done',
        'batches:list',
        'batches:my_batches',
        'courses:list',
        'courses:enrollment',
        'courses:payment',
        'courses:payment_success',
        'quizzes:list',
        'quizzes:my_attempts',
        'doubts:list',
        'doubts:submit',
        'doubts:my_doubts',
        'doubts:teacher_dashboard',
        'admin:index',
    ]
    
    print("\n1. SIMPLE URLs (No Parameters):")
    print("-" * 50)
    
    working_urls = 0
    total_urls = len(simple_urls)
    
    for url_name in simple_urls:
        try:
            url = reverse(url_name)
            print(f"OK   {url_name:<30} -> {url}")
            working_urls += 1
        except NoReverseMatch as e:
            print(f"FAIL {url_name:<30} -> {str(e)}")
        except Exception as e:
            print(f"ERR  {url_name:<30} -> {str(e)}")
    
    # Parametrized URLs
    param_urls = [
        ('batches:detail', {'batch_id': 1}),
        ('batches:enroll', {'batch_id': 1}),
        ('batches:purchase', {'batch_id': 1}),
        ('batches:order_detail', {'order_id': 'ORD123456'}),
        ('batches:subject_detail', {'subject_id': 1}),
        ('batches:lecture_detail', {'lecture_id': 1}),
        ('batches:dpp_detail', {'dpp_id': 1}),
        ('batches:start_dpp', {'dpp_id': 1}),
        ('batches:take_dpp', {'attempt_id': 1}),
        ('batches:dpp_results', {'attempt_id': 1}),
        ('batches:dpp_solution', {'solution_id': 1}),
        ('batches:add_comment', {}),
        ('batches:toggle_comment_like', {'comment_id': 1}),
        ('courses:subject_detail', {'subject_id': 1}),
        ('courses:lecture_detail', {'lecture_id': 1}),
        ('courses:mark_complete', {'lecture_id': 1}),
        ('quizzes:detail', {'quiz_id': 1}),
        ('quizzes:start', {'quiz_id': 1}),
        ('quizzes:submit', {'quiz_id': 1}),
        ('quizzes:results', {'attempt_id': 1}),
        ('doubts:detail', {'doubt_id': 1}),
        ('doubts:resolve', {'doubt_id': 1}),
        ('accounts:password_reset_confirm', {'uidb64': 'test', 'token': 'test'}),
        ('accounts:password_reset_complete', {}),
    ]
    
    print("\n2. PARAMETRIZED URLs:")
    print("-" * 50)
    
    param_working = 0
    param_total = len(param_urls)
    
    for url_name, kwargs in param_urls:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"OK   {url_name:<30} -> {url}")
            param_working += 1
        except NoReverseMatch as e:
            print(f"FAIL {url_name:<30} -> {str(e)}")
        except Exception as e:
            print(f"ERR  {url_name:<30} -> {str(e)}")
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print(f"Simple URLs:      {working_urls}/{total_urls} working")
    print(f"Parametrized URLs: {param_working}/{param_total} working")
    print(f"Total URLs:       {working_urls + param_working}/{total_urls + param_total} working")
    print("=" * 80)

if __name__ == '__main__':
    check_urls()