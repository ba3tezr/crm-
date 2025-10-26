#!/usr/bin/env python
"""
اختبار شامل لجميع صفحات النظام والترجمات
Comprehensive test for all system pages and translations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.permits.models import Permit
from apps.maintenance.models import Ticket
from apps.complaints.models import Case
from apps.marketing.models import Event
from apps.hr.models import LeaveRequest

User = get_user_model()

# Create test client
client = Client()

# Get or create admin user
try:
    admin = User.objects.get(username='admin')
    print(f"✅ Found admin user: {admin.username}")
except User.DoesNotExist:
    print("❌ Admin user not found. Please create one first.")
    exit(1)

# Login
login_success = client.login(username='admin', password='admin123')
if login_success:
    print("✅ Login successful")
else:
    print("❌ Login failed")
    exit(1)

print("\n" + "="*80)
print("🧪 TESTING ALL PAGES - اختبار جميع الصفحات")
print("="*80 + "\n")

# Test URLs
test_urls = {
    'Dashboard': '/dashboard/',
    
    # Permits
    'Permits List': '/permits/',
    'Permit Create': '/permits/create/',
    
    # Maintenance
    'Maintenance List': '/maintenance/',
    'Maintenance Create': '/maintenance/create/',
    
    # Complaints
    'Complaints List': '/complaints/',
    'Complaint Create': '/complaints/create/',
    
    # Marketing
    'Marketing List': '/marketing/',
    'Marketing Create': '/marketing/create/',
    
    # HR
    'HR List': '/hr/',
    'HR Create': '/hr/create/',
}

# Test each URL
results = {'success': 0, 'failed': 0}
for name, url in test_urls.items():
    try:
        response = client.get(url)
        if response.status_code in [200, 302]:
            print(f"✅ {name:25} → {url:30} → {response.status_code}")
            results['success'] += 1
        else:
            print(f"❌ {name:25} → {url:30} → {response.status_code}")
            results['failed'] += 1
    except Exception as e:
        print(f"❌ {name:25} → {url:30} → ERROR: {str(e)[:50]}")
        results['failed'] += 1

print("\n" + "="*80)
print("🌐 TESTING TRANSLATIONS - اختبار الترجمات")
print("="*80 + "\n")

# Test Arabic (default)
print("📝 Testing Arabic (العربية)...")
response = client.get('/dashboard/', HTTP_ACCEPT_LANGUAGE='ar')
content = response.content.decode('utf-8')

arabic_terms = [
    'لوحة التحكم',
    'التصاريح',
    'الصيانة',
    'الشكاوى',
    'التسويق',
    'الموارد البشرية',
]

ar_found = 0
for term in arabic_terms:
    if term in content:
        print(f"  ✅ Found: {term}")
        ar_found += 1
    else:
        print(f"  ❌ Missing: {term}")

print(f"\n  Arabic terms found: {ar_found}/{len(arabic_terms)}")

# Test English
print("\n📝 Testing English...")
# Switch to English
client.post('/i18n/setlang/', {'language': 'en', 'next': '/dashboard/'})
response = client.get('/dashboard/', HTTP_ACCEPT_LANGUAGE='en')
content = response.content.decode('utf-8')

english_terms = [
    'Dashboard',
    'Permits',
    'Maintenance',
    'Complaints',
    'Marketing',
]

en_found = 0
for term in english_terms:
    if term in content:
        print(f"  ✅ Found: {term}")
        en_found += 1
    else:
        print(f"  ❌ Missing: {term}")

print(f"\n  English terms found: {en_found}/{len(english_terms)}")

print("\n" + "="*80)
print("📊 TESTING DATA MODELS - اختبار نماذج البيانات")
print("="*80 + "\n")

# Count existing data
permits_count = Permit.objects.count()
tickets_count = Ticket.objects.count()
cases_count = Case.objects.count()
events_count = Event.objects.count()
leaves_count = LeaveRequest.objects.count()

print(f"  📋 Permits: {permits_count}")
print(f"  🔧 Maintenance Tickets: {tickets_count}")
print(f"  💬 Complaints: {cases_count}")
print(f"  📅 Marketing Events: {events_count}")
print(f"  🏖️  Leave Requests: {leaves_count}")

print("\n" + "="*80)
print("📈 FINAL RESULTS - النتائج النهائية")
print("="*80 + "\n")

total_tests = results['success'] + results['failed']
success_rate = (results['success'] / total_tests * 100) if total_tests > 0 else 0

print(f"  ✅ Successful: {results['success']}/{total_tests}")
print(f"  ❌ Failed: {results['failed']}/{total_tests}")
print(f"  📊 Success Rate: {success_rate:.1f}%")

if results['failed'] == 0:
    print("\n  🎉 ALL TESTS PASSED! - جميع الاختبارات نجحت!")
else:
    print(f"\n  ⚠️  {results['failed']} tests failed - فشل {results['failed']} اختبار")

print("\n" + "="*80)

