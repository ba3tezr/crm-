#!/usr/bin/env python
"""
Create Sample Data for CRM System
إنشاء بيانات افتراضية لنظام CRM
"""
import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import Department, TenantProfile
from apps.permits.models import Permit, PermitApproval
from apps.maintenance.models import Ticket
from apps.complaints.models import Case
from apps.marketing.models import Event
from apps.hr.models import LeaveRequest
from apps.finance.models import Invoice, InvoiceItem, Payment
from apps.core.models import SystemSettings

User = get_user_model()


def create_departments():
    """إنشاء الأقسام - Create Departments"""
    print("\n" + "="*80)
    print("📁 Creating Departments...")
    print("="*80)
    
    departments_data = [
        {'name': 'operations', 'name_ar': 'العمليات', 'name_en': 'Operations', 'description': 'Operations Department'},
        {'name': 'technical', 'name_ar': 'الفني', 'name_en': 'Technical', 'description': 'Technical Department'},
        {'name': 'marketing', 'name_ar': 'التسويق', 'name_en': 'Marketing', 'description': 'Marketing Department'},
        {'name': 'hr', 'name_ar': 'الموارد البشرية', 'name_en': 'Human Resources', 'description': 'HR Department'},
        {'name': 'customer_service', 'name_ar': 'خدمة العملاء', 'name_en': 'Customer Service', 'description': 'Customer Service Department'},
        {'name': 'maintenance', 'name_ar': 'الصيانة', 'name_en': 'Maintenance', 'description': 'Maintenance Department'},
        {'name': 'security', 'name_ar': 'الأمن', 'name_en': 'Security', 'description': 'Security Department'},
        {'name': 'tenants', 'name_ar': 'المستأجرين', 'name_en': 'Tenants', 'description': 'Tenants Department'},
        {'name': 'finance', 'name_ar': 'المالية', 'name_en': 'Finance', 'description': 'Finance Department'},
        {'name': 'management', 'name_ar': 'الإدارة', 'name_en': 'Management', 'description': 'Management Department'},
    ]
    
    created_count = 0
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={
                'name_ar': dept_data['name_ar'],
                'name_en': dept_data['name_en'],
                'description': dept_data['description'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Created: {dept.name_ar} - {dept.name_en}")
            created_count += 1
        else:
            print(f"⏭️  Exists: {dept.name_ar} - {dept.name_en}")
    
    print(f"\n📊 Total Departments Created: {created_count}/{len(departments_data)}")
    return Department.objects.all()


def create_users(departments):
    """إنشاء المستخدمين - Create Users"""
    print("\n" + "="*80)
    print("👥 Creating Users...")
    print("="*80)
    
    # Get departments
    ops_dept = departments.get(name='operations')
    tech_dept = departments.get(name='technical')
    mkg_dept = departments.get(name='marketing')
    hr_dept = departments.get(name='hr')
    cs_dept = departments.get(name='customer_service')
    maint_dept = departments.get(name='maintenance')
    sec_dept = departments.get(name='security')
    tenant_dept = departments.get(name='tenants')
    finance_dept = departments.get(name='finance')
    mgmt_dept = departments.get(name='management')
    
    users_data = [
        # Management
        {'username': 'manager', 'email': 'manager@crm.com', 'first_name': 'Ahmed', 'last_name': 'Al-Mansour', 
         'department': mgmt_dept, 'job_title': 'General Manager', 'employee_id': 'MGR001', 'is_staff': True},
        
        # Operations (5 users)
        {'username': 'ops_manager', 'email': 'ops.manager@crm.com', 'first_name': 'Mohammed', 'last_name': 'Al-Otaibi',
         'department': ops_dept, 'job_title': 'Operations Manager', 'employee_id': 'OPS001', 'is_staff': True},
        {'username': 'ops_user1', 'email': 'ops1@crm.com', 'first_name': 'Fatima', 'last_name': 'Al-Harbi',
         'department': ops_dept, 'job_title': 'Operations Coordinator', 'employee_id': 'OPS002'},
        {'username': 'ops_user2', 'email': 'ops2@crm.com', 'first_name': 'Khalid', 'last_name': 'Al-Zahrani',
         'department': ops_dept, 'job_title': 'Operations Specialist', 'employee_id': 'OPS003'},
        
        # Technical (4 users)
        {'username': 'tech_manager', 'email': 'tech.manager@crm.com', 'first_name': 'Omar', 'last_name': 'Al-Qahtani',
         'department': tech_dept, 'job_title': 'Technical Manager', 'employee_id': 'TECH001', 'is_staff': True},
        {'username': 'tech_user1', 'email': 'tech1@crm.com', 'first_name': 'Sara', 'last_name': 'Al-Mutairi',
         'department': tech_dept, 'job_title': 'Technical Support', 'employee_id': 'TECH002'},
        
        # Marketing (3 users)
        {'username': 'mkg_manager', 'email': 'mkg.manager@crm.com', 'first_name': 'Nora', 'last_name': 'Al-Dosari',
         'department': mkg_dept, 'job_title': 'Marketing Manager', 'employee_id': 'MKG001', 'is_staff': True},
        {'username': 'mkg_user1', 'email': 'mkg1@crm.com', 'first_name': 'Abdullah', 'last_name': 'Al-Shammari',
         'department': mkg_dept, 'job_title': 'Marketing Specialist', 'employee_id': 'MKG002'},
        
        # HR (3 users)
        {'username': 'hr_manager', 'email': 'hr.manager@crm.com', 'first_name': 'Layla', 'last_name': 'Al-Ghamdi',
         'department': hr_dept, 'job_title': 'HR Manager', 'employee_id': 'HR001', 'is_staff': True},
        {'username': 'hr_user1', 'email': 'hr1@crm.com', 'first_name': 'Yousef', 'last_name': 'Al-Maliki',
         'department': hr_dept, 'job_title': 'HR Specialist', 'employee_id': 'HR002'},
        
        # Customer Service (7 users)
        {'username': 'cs_manager', 'email': 'cs.manager@crm.com', 'first_name': 'Huda', 'last_name': 'Al-Rashid',
         'department': cs_dept, 'job_title': 'CS Manager', 'employee_id': 'CS001', 'is_staff': True},
        {'username': 'cs_user1', 'email': 'cs1@crm.com', 'first_name': 'Saleh', 'last_name': 'Al-Harthy',
         'department': cs_dept, 'job_title': 'Customer Service Rep', 'employee_id': 'CS002'},
        {'username': 'cs_user2', 'email': 'cs2@crm.com', 'first_name': 'Maha', 'last_name': 'Al-Subaie',
         'department': cs_dept, 'job_title': 'Customer Service Rep', 'employee_id': 'CS003'},
        
        # Maintenance (4 users)
        {'username': 'maint_manager', 'email': 'maint.manager@crm.com', 'first_name': 'Faisal', 'last_name': 'Al-Juhani',
         'department': maint_dept, 'job_title': 'Maintenance Manager', 'employee_id': 'MAINT001', 'is_staff': True},
        {'username': 'maint_user1', 'email': 'maint1@crm.com', 'first_name': 'Reem', 'last_name': 'Al-Balawi',
         'department': maint_dept, 'job_title': 'Maintenance Technician', 'employee_id': 'MAINT002'},
        
        # Security (3 users)
        {'username': 'sec_manager', 'email': 'sec.manager@crm.com', 'first_name': 'Tariq', 'last_name': 'Al-Anazi',
         'department': sec_dept, 'job_title': 'Security Manager', 'employee_id': 'SEC001', 'is_staff': True},
        {'username': 'sec_user1', 'email': 'sec1@crm.com', 'first_name': 'Aisha', 'last_name': 'Al-Shahrani',
         'department': sec_dept, 'job_title': 'Security Officer', 'employee_id': 'SEC002'},
        
        # Finance (3 users)
        {'username': 'finance_manager', 'email': 'finance.manager@crm.com', 'first_name': 'Hassan', 'last_name': 'Al-Tamimi',
         'department': finance_dept, 'job_title': 'Finance Manager', 'employee_id': 'FIN001', 'is_staff': True},
        {'username': 'finance_user1', 'email': 'finance1@crm.com', 'first_name': 'Nouf', 'last_name': 'Al-Khaldi',
         'department': finance_dept, 'job_title': 'Accountant', 'employee_id': 'FIN002'},
    ]
    
    created_count = 0
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'department': user_data['department'],
                'job_title': user_data['job_title'],
                'employee_id': user_data['employee_id'],
                'is_staff': user_data.get('is_staff', False),
                'is_active': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Created: {user.username} - {user.get_full_name()} ({user.department.name_en})")
            created_count += 1
        else:
            print(f"⏭️  Exists: {user.username} - {user.get_full_name()}")
    
    print(f"\n📊 Total Users Created: {created_count}/{len(users_data)}")
    return User.objects.all()


def create_tenants(tenant_dept):
    """إنشاء المستأجرين - Create Tenants"""
    print("\n" + "="*80)
    print("🏢 Creating Tenants...")
    print("="*80)
    
    tenants_data = [
        {'username': 'tenant1', 'email': 'tenant1@example.com', 'first_name': 'Ali', 'last_name': 'Al-Saud',
         'company': 'Al-Saud Trading Co.', 'unit': 'A-101', 'floor': '1', 'building': 'Tower A'},
        {'username': 'tenant2', 'email': 'tenant2@example.com', 'first_name': 'Mariam', 'last_name': 'Al-Faisal',
         'company': 'Faisal Electronics', 'unit': 'A-205', 'floor': '2', 'building': 'Tower A'},
        {'username': 'tenant3', 'email': 'tenant3@example.com', 'first_name': 'Saad', 'last_name': 'Al-Rajhi',
         'company': 'Rajhi Fashion Store', 'unit': 'B-103', 'floor': '1', 'building': 'Tower B'},
        {'username': 'tenant4', 'email': 'tenant4@example.com', 'first_name': 'Lina', 'last_name': 'Al-Waleed',
         'company': 'Waleed Cafe', 'unit': 'B-201', 'floor': '2', 'building': 'Tower B'},
        {'username': 'tenant5', 'email': 'tenant5@example.com', 'first_name': 'Majed', 'last_name': 'Al-Olayan',
         'company': 'Olayan Bookstore', 'unit': 'C-105', 'floor': '1', 'building': 'Tower C'},
    ]
    
    created_count = 0
    for tenant_data in tenants_data:
        user, user_created = User.objects.get_or_create(
            username=tenant_data['username'],
            defaults={
                'email': tenant_data['email'],
                'first_name': tenant_data['first_name'],
                'last_name': tenant_data['last_name'],
                'department': tenant_dept,
                'is_active': True,
            }
        )
        if user_created:
            user.set_password('tenant123')
            user.save()
        
        # Create Tenant Profile
        profile, profile_created = TenantProfile.objects.get_or_create(
            user=user,
            defaults={
                'tenant_id': f'TNT{1000 + created_count}',
                'company_name': tenant_data['company'],
                'unit_number': tenant_data['unit'],
                'floor_number': tenant_data['floor'],
                'building_name': tenant_data['building'],
                'contract_number': f'CNT-2025-{1000 + created_count}',
                'contract_start_date': datetime.now().date(),
                'contract_end_date': (datetime.now() + timedelta(days=365)).date(),
                'is_active': True,
            }
        )
        
        if profile_created:
            print(f"✅ Created Tenant: {user.get_full_name()} - {tenant_data['company']} ({tenant_data['unit']})")
            created_count += 1
        else:
            print(f"⏭️  Exists: {user.get_full_name()} - {tenant_data['company']}")
    
    print(f"\n📊 Total Tenants Created: {created_count}/{len(tenants_data)}")
    return User.objects.filter(department=tenant_dept)


def create_system_settings():
    """إنشاء إعدادات النظام - Create System Settings"""
    print("\n" + "="*80)
    print("⚙️  Creating System Settings...")
    print("="*80)
    
    settings = SystemSettings.load()
    settings.currency = 'USD'
    settings.currency_symbol = '$'
    settings.date_format = 'en'
    settings.save()
    
    print(f"✅ System Settings Updated:")
    print(f"   Currency: {settings.currency} ({settings.currency_symbol})")
    print(f"   Date Format: {settings.date_format}")
    
    return settings


def main():
    """Main function"""
    print("\n" + "="*80)
    print("🚀 CRM SYSTEM - SAMPLE DATA CREATION")
    print("="*80)
    print("This script will create sample data for the CRM system")
    print("="*80)
    
    # Create Departments
    departments = create_departments()
    
    # Create Users
    users = create_users(departments)
    
    # Create Tenants
    tenant_dept = departments.get(name='tenants')
    tenants = create_tenants(tenant_dept)
    
    # Create System Settings
    settings = create_system_settings()
    
    print("\n" + "="*80)
    print("✅ SAMPLE DATA CREATION COMPLETED!")
    print("="*80)
    print(f"📊 Summary:")
    print(f"   Departments: {departments.count()}")
    print(f"   Users: {users.count()}")
    print(f"   Tenants: {tenants.count()}")
    print(f"   Currency: {settings.currency} ({settings.currency_symbol})")
    print("="*80)
    print("\n🔐 Login Credentials:")
    print("   Admin: admin / admin123")
    print("   Manager: manager / password123")
    print("   Tenant: tenant1 / tenant123")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()

