#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_study.settings')
django.setup()

User = get_user_model()
client = Client()

# Test URLs that don't require authentication
public_urls = [
    ('main:index', {}),
    ('main:about', {}),
    ('main:contact', {}),
    ('main:pricing', {}),
    ('accounts:login', {}),
    ('accounts:register', {}),
    ('accounts:password_reset', {}),
    ('batches:list', {}),
    ('courses:list', {}),
]

# Test URLs that require authentication
auth_urls = [
    ('accounts:dashboard', {}),
    ('accounts:profile', {}),
    ('accounts:logout', {}),
    ('batches:my_batches', {}),
    ('doubts:submit', {}),
    ('doubts:my_doubts', {}),
    ('quizzes:list', {}),
    ('quizzes:my_attempts', {}),
]

# Test URLs with parameters (need existing objects)
param_urls = [
    ('batches:detail', {'batch_id': 1}),
    ('batches:subject_detail', {'subject_id': 1}),
    ('batches:lecture_detail', {'lecture_id': 1}),
    ('batches:dpp_detail', {'dpp_id': 1}),
    ('courses:subject_detail', {'subject_id': 1}),
    ('courses:lecture_detail', {'lecture_id': 1}),
    ('quizzes:detail', {'quiz_id': 1}),
    ('doubts:detail', {'doubt_id': 1}),
]

def test_url(url_name, kwargs=None, auth_required=False):
    try:
        url = reverse(url_name, kwargs=kwargs)
        if auth_required:
            # Create test user if not exists
            user, created = User.objects.get_or_create(
                username='testuser',
                defaults={'email': 'test@example.com'}
            )
            client.force_login(user)
        
        response = client.get(url)
        status = response.status_code
        
        if status == 200:
            result = "✓ OK"
        elif status == 302:
            result = "→ REDIRECT"
        elif status == 404:
            result = "✗ NOT FOUND"
        elif status == 403:
            result = "✗ FORBIDDEN"
        elif status == 500:
            result = "✗ SERVER ERROR"
        else:
            result = f"? STATUS {status}"
            
        print(f"{url_name:<30} {url:<40} {result}")
        return status
        
    except Exception as e:
        print(f"{url_name:<30} {'ERROR':<40} ✗ {str(e)}")
        return None

print("=" * 80)
print("SMART STUDY - URL TESTING REPORT")
print("=" * 80)

print("\n1. PUBLIC URLs (No Authentication Required):")
print("-" * 50)
for url_name, kwargs in public_urls:
    test_url(url_name, kwargs, auth_required=False)

print("\n2. AUTHENTICATED URLs (Login Required):")
print("-" * 50)
for url_name, kwargs in auth_urls:
    test_url(url_name, kwargs, auth_required=True)

print("\n3. PARAMETRIZED URLs (May need existing data):")
print("-" * 50)
for url_name, kwargs in param_urls:
    test_url(url_name, kwargs, auth_required=True)

print("\n4. ADMIN URLs:")
print("-" * 50)
test_url('admin:index', auth_required=False)

print("\n" + "=" * 80)
print("URL TEST COMPLETED")
print("=" * 80)