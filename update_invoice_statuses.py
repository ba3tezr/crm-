#!/usr/bin/env python
"""
Script to update all invoice payment statuses
سكريبت لتحديث حالات الدفع لجميع الفواتير
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.finance.models import Invoice

def update_all_invoices():
    """تحديث حالات جميع الفواتير"""
    invoices = Invoice.objects.all()
    updated_count = 0
    
    print(f"Found {invoices.count()} invoices to check...")
    
    for invoice in invoices:
        old_status = invoice.status
        old_paid = invoice.paid_amount
        
        # تحديث حالة الدفع
        invoice.update_payment_status()
        
        # إعادة تحميل الفاتورة للحصول على القيم المحدثة
        invoice.refresh_from_db()
        
        if old_status != invoice.status or old_paid != invoice.paid_amount:
            print(f"✅ Updated {invoice.invoice_number}:")
            print(f"   Status: {old_status} → {invoice.status}")
            print(f"   Paid: {old_paid} → {invoice.paid_amount}")
            print(f"   Total: {invoice.total_amount}")
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count} invoices")
    print(f"✅ {invoices.count() - updated_count} invoices were already correct")

if __name__ == '__main__':
    update_all_invoices()

