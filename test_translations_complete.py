#!/usr/bin/env python
"""
اختبار شامل للترجمات - Complete Translation Test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.utils.translation import activate

User = get_user_model()

# Create test client
client = Client()

# Get or create admin user
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Login
client.login(username='admin', password='admin123')

print("=" * 80)
print("🧪 اختبار الترجمات الشامل - Complete Translation Test")
print("=" * 80)

# Test URLs in both languages
test_urls = [
    ('/', 'Dashboard'),
    ('/dashboard/', 'Dashboard'),
    ('/permits/', 'Permits'),
    ('/maintenance/', 'Maintenance'),
    ('/complaints/', 'Complaints'),
    ('/marketing/', 'Marketing'),
    ('/hr/', 'HR'),
]

# Test Arabic
print("\n📝 Testing Arabic (ar) URLs:")
print("-" * 80)
activate('ar')
for url, name in test_urls:
    full_url = f'/ar{url}'
    response = client.get(full_url, follow=True)
    status = "✅" if response.status_code == 200 else "❌"
    print(f"{status} {full_url:30} → {response.status_code}")
    
    # Check for Arabic text in response
    content = response.content.decode('utf-8')
    if 'لوحة التحكم' in content or 'التصاريح' in content or 'الصيانة' in content:
        print(f"   ✅ Arabic text found")
    else:
        print(f"   ⚠️  No Arabic text detected")

# Test English
print("\n📝 Testing English (en) URLs:")
print("-" * 80)
activate('en')
for url, name in test_urls:
    full_url = f'/en{url}'
    response = client.get(full_url, follow=True)
    status = "✅" if response.status_code == 200 else "❌"
    print(f"{status} {full_url:30} → {response.status_code}")
    
    # Check for English text in response
    content = response.content.decode('utf-8')
    if 'Dashboard' in content or 'Permits' in content or 'Maintenance' in content:
        print(f"   ✅ English text found")
    else:
        print(f"   ⚠️  No English text detected")

# Test specific sections
print("\n📝 Testing Specific Sections:")
print("-" * 80)

sections = [
    ('/ar/complaints/', ['الشكاوى', 'شكوى جديدة', 'نوع القضية']),
    ('/en/complaints/', ['Complaints', 'New Complaint', 'Case Type']),
    ('/ar/marketing/', ['الفعاليات', 'فعالية جديدة', 'نوع الفعالية']),
    ('/en/marketing/', ['Events', 'New Event', 'Event Type']),
    ('/ar/hr/', ['الإجازات', 'طلب إجازة', 'نوع الإجازة']),
    ('/en/hr/', ['Leave Requests', 'Leave Request', 'Leave Type']),
]

for url, expected_texts in sections:
    response = client.get(url, follow=True)
    content = response.content.decode('utf-8')
    
    print(f"\n{url}")
    for text in expected_texts:
        if text in content:
            print(f"   ✅ Found: {text}")
        else:
            print(f"   ❌ Missing: {text}")

# Test Model Choices Translation
print("\n📝 Testing Model Choices Translation:")
print("-" * 80)

from apps.complaints.models import Case
from apps.marketing.models import Event
from apps.hr.models import LeaveRequest

activate('ar')
print("\n🇸🇦 Arabic Choices:")
print(f"   Case Types: {[choice[1] for choice in Case.CASE_TYPE_CHOICES]}")
print(f"   Event Types: {[choice[1] for choice in Event.EVENT_TYPE_CHOICES[:3]]}")
print(f"   Leave Types: {[choice[1] for choice in LeaveRequest.LEAVE_TYPE_CHOICES[:3]]}")

activate('en')
print("\n🇬🇧 English Choices:")
print(f"   Case Types: {[choice[1] for choice in Case.CASE_TYPE_CHOICES]}")
print(f"   Event Types: {[choice[1] for choice in Event.EVENT_TYPE_CHOICES[:3]]}")
print(f"   Leave Types: {[choice[1] for choice in LeaveRequest.LEAVE_TYPE_CHOICES[:3]]}")

print("\n" + "=" * 80)
print("✅ Translation Test Completed!")
print("=" * 80)

