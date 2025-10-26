#!/usr/bin/env python
"""
اختبار شامل لجميع صفحات النظام
Comprehensive test for all system pages
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
client = Client()

# Login as admin
user = User.objects.get(username='admin')
client.force_login(user)

print("=" * 80)
print("🧪 اختبار شامل لجميع صفحات النظام - Comprehensive System Test")
print("=" * 80)

# Test URLs
test_urls = {
    "الصفحة الرئيسية - Home": "/",
    "لوحة التحكم - Dashboard": "/dashboard/",
    
    # Permits
    "قائمة التصاريح - Permits List": "/permits/",
    "إنشاء تصريح - Create Permit": "/permits/create/",
    "تصدير التصاريح - Export Permits": "/permits/export/",
    
    # Maintenance
    "قائمة الصيانة - Maintenance List": "/maintenance/",
    "إنشاء طلب صيانة - Create Ticket": "/maintenance/create/",
    "تصدير الصيانة - Export Tickets": "/maintenance/export/",
    
    # Complaints
    "قائمة الشكاوى - Complaints List": "/complaints/",
    "إنشاء شكوى - Create Case": "/complaints/create/",
    "تصدير الشكاوى - Export Cases": "/complaints/export/",
    
    # Marketing
    "قائمة الفعاليات - Events List": "/marketing/",
    "إنشاء فعالية - Create Event": "/marketing/create/",
    "تصدير الفعاليات - Export Events": "/marketing/export/",
    
    # HR
    "قائمة الإجازات - Leave Requests List": "/hr/",
    "إنشاء طلب إجازة - Create Leave Request": "/hr/create/",
}

print("\n📋 اختبار الصفحات - Testing Pages:")
print("-" * 80)

passed = 0
failed = 0

for name, url in test_urls.items():
    try:
        response = client.get(url)
        if response.status_code in [200, 302]:
            print(f"✅ {name}")
            print(f"   URL: {url} → {response.status_code}")
            passed += 1
        else:
            print(f"❌ {name}")
            print(f"   URL: {url} → {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ {name}")
        print(f"   URL: {url} → ERROR: {str(e)[:100]}")
        failed += 1

print("\n" + "=" * 80)
print(f"📊 النتائج - Results:")
print(f"   ✅ نجح - Passed: {passed}")
print(f"   ❌ فشل - Failed: {failed}")
print(f"   📈 النسبة - Success Rate: {(passed/(passed+failed)*100):.1f}%")
print("=" * 80)

# Create test data
print("\n📝 إنشاء بيانات تجريبية - Creating Test Data:")
print("-" * 80)

try:
    # Create Permit
    permit = Permit.objects.create(
        permit_number="TEST-001",
        permit_type="entry",
        direction="in",
        title="تصريح تجريبي - Test Permit",
        company_name="شركة تجريبية",
        contact_person="محمد أحمد",
        contact_phone="0501234567",
        created_by=user,
        tenant=user,
        status="pending"
    )
    print(f"✅ تم إنشاء تصريح - Permit created: {permit.permit_number}")
    
    # Create Ticket
    ticket = Ticket.objects.create(
        ticket_number="TICKET-001",
        category="plumbing",
        priority="high",
        title="مشكلة تجريبية - Test Issue",
        description="وصف المشكلة",
        unit_number="101",
        floor_number="1",
        building_name="مبنى A",
        created_by=user,
        assigned_to=user,
        status="open"
    )
    print(f"✅ تم إنشاء طلب صيانة - Ticket created: {ticket.ticket_number}")
    
    # Create Case
    case = Case.objects.create(
        case_number="CASE-001",
        case_type="complaint",
        title="شكوى تجريبية - Test Complaint",
        description="وصف الشكوى",
        department="Operations",
        created_by=user,
        assigned_to=user,
        status="open"
    )
    print(f"✅ تم إنشاء شكوى - Case created: {case.case_number}")
    
    # Create Event
    event = Event.objects.create(
        event_number="EVENT-001",
        event_type="seminar",
        title="فعالية تجريبية - Test Event",
        description="وصف الفعالية",
        location="قاعة المؤتمرات",
        budget=10000.00,
        created_by=user,
        responsible_person=user,
        status="planned"
    )
    print(f"✅ تم إنشاء فعالية - Event created: {event.event_number}")
    
    # Create Leave Request
    from datetime import date, timedelta
    leave = LeaveRequest.objects.create(
        request_number="LEAVE-001",
        employee=user,
        leave_type="annual",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=5),
        days_count=5,
        reason="إجازة سنوية",
        status="pending"
    )
    print(f"✅ تم إنشاء طلب إجازة - Leave Request created: {leave.request_number}")
    
except Exception as e:
    print(f"❌ خطأ في إنشاء البيانات - Error creating data: {str(e)[:100]}")

# Test detail pages
print("\n📄 اختبار صفحات التفاصيل - Testing Detail Pages:")
print("-" * 80)

detail_urls = {
    f"تفاصيل التصريح - Permit Detail": f"/permits/{permit.id}/",
    f"تعديل التصريح - Edit Permit": f"/permits/{permit.id}/update/",
    f"حذف التصريح - Delete Permit": f"/permits/{permit.id}/delete/",
    
    f"تفاصيل الصيانة - Ticket Detail": f"/maintenance/{ticket.id}/",
    f"تعديل الصيانة - Edit Ticket": f"/maintenance/{ticket.id}/update/",
    f"حذف الصيانة - Delete Ticket": f"/maintenance/{ticket.id}/delete/",
    
    f"تفاصيل الشكوى - Case Detail": f"/complaints/{case.id}/",
    f"تعديل الشكوى - Edit Case": f"/complaints/{case.id}/update/",
    f"حذف الشكوى - Delete Case": f"/complaints/{case.id}/delete/",
    
    f"تفاصيل الفعالية - Event Detail": f"/marketing/{event.id}/",
    f"تعديل الفعالية - Edit Event": f"/marketing/{event.id}/update/",
    f"حذف الفعالية - Delete Event": f"/marketing/{event.id}/delete/",
    
    f"تفاصيل الإجازة - Leave Detail": f"/hr/{leave.id}/",
    f"تعديل الإجازة - Edit Leave": f"/hr/{leave.id}/update/",
}

detail_passed = 0
detail_failed = 0

for name, url in detail_urls.items():
    try:
        response = client.get(url)
        if response.status_code in [200, 302]:
            print(f"✅ {name}")
            detail_passed += 1
        else:
            print(f"❌ {name} → {response.status_code}")
            detail_failed += 1
    except Exception as e:
        print(f"❌ {name} → ERROR: {str(e)[:100]}")
        detail_failed += 1

print("\n" + "=" * 80)
print(f"📊 نتائج صفحات التفاصيل - Detail Pages Results:")
print(f"   ✅ نجح - Passed: {detail_passed}")
print(f"   ❌ فشل - Failed: {detail_failed}")
print(f"   📈 النسبة - Success Rate: {(detail_passed/(detail_passed+detail_failed)*100):.1f}%")
print("=" * 80)

print("\n🎉 انتهى الاختبار - Test Completed!")
