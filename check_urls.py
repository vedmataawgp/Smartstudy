#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_study.settings')
django.setup()

User = get_user_model()

def check_url_patterns():
    """Check all URL patterns for syntax errors"""
    print("=" * 80)
    print("SMART STUDY - URL PATTERN CHECK")
    print("=" * 80)
    
    # Test URL patterns that don't require parameters
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
    
    print("\n1. SIMPLE URL PATTERNS (No Parameters):")
    print("-" * 50)
    
    for url_name in simple_urls:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name:<30} -> {url}")
        except NoReverseMatch as e:
            print(f"✗ {url_name:<30} -> ERROR: {str(e)}")
        except Exception as e:
            print(f"? {url_name:<30} -> UNKNOWN ERROR: {str(e)}")
    
    # Test URL patterns that require parameters
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
    
    print("\n2. PARAMETRIZED URL PATTERNS:")
    print("-" * 50)
    
    for url_name, kwargs in param_urls:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"✓ {url_name:<30} -> {url}")
        except NoReverseMatch as e:
            print(f"✗ {url_name:<30} -> ERROR: {str(e)}")
        except Exception as e:
            print(f"? {url_name:<30} -> UNKNOWN ERROR: {str(e)}")

def check_template_existence():
    """Check if templates exist for views"""
    print("\n3. TEMPLATE EXISTENCE CHECK:")
    print("-" * 50)
    
    templates_to_check = [
        'main/index.html',
        'main/about.html',
        'main/contact.html',
        'main/pricing.html',
        'main/search_results.html',
        'accounts/login.html',
        'accounts/register.html',
        'accounts/dashboard.html',
        'accounts/profile.html',
        'accounts/password_reset.html',
        'accounts/password_reset_done.html',
        'accounts/password_reset_confirm.html',
        'accounts/password_reset_complete.html',
        'batches/list.html',
        'batches/detail.html',
        'batches/my_batches.html',
        'batches/purchase.html',
        'batches/order_detail.html',
        'batches/subject_detail.html',
        'batches/lecture_detail.html',
        'batches/dpp_detail.html',
        'batches/take_dpp.html',
        'batches/dpp_results.html',
        'batches/dpp_solution.html',
        'courses/list.html',
        'courses/subject_detail.html',
        'courses/lecture_detail.html',
        'courses/enrollment.html',
        'courses/payment.html',
        'courses/payment_success.html',
        'quizzes/list.html',
        'quizzes/detail.html',
        'quizzes/submit.html',
        'quizzes/results.html',
        'quizzes/my_attempts.html',
        'doubts/list.html',
        'doubts/submit.html',
        'doubts/detail.html',
        'doubts/resolve.html',
        'doubts/my_doubts.html',
        'doubts/teacher_dashboard.html',
    ]
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    for template_name in templates_to_check:
        try:
            get_template(template_name)
            print(f"✓ {template_name}")
        except TemplateDoesNotExist:
            print(f"✗ {template_name} -> MISSING")
        except Exception as e:
            print(f"? {template_name} -> ERROR: {str(e)}")

def check_view_imports():
    """Check if all views can be imported"""
    print("\n4. VIEW IMPORT CHECK:")
    print("-" * 50)
    
    view_modules = [
        'main.views',
        'accounts.views',
        'batches.views',
        'courses.views',
        'quizzes.views',
        'doubts.views',
    ]
    
    for module_name in view_modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name}")
        except ImportError as e:
            print(f"✗ {module_name} -> IMPORT ERROR: {str(e)}")
        except Exception as e:
            print(f"? {module_name} -> ERROR: {str(e)}")

if __name__ == '__main__':
    check_url_patterns()
    check_template_existence()
    check_view_imports()
    
    print("\n" + "=" * 80)
    print("URL CHECK COMPLETED")
    print("=" * 80)