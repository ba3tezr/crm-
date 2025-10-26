"""
Views for Accounts App
إدارة المستخدمين والمستأجرين
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .models import TenantProfile
from apps.permits.models import Permit
from apps.permits.forms import PermitForm
from apps.maintenance.models import Ticket
from apps.complaints.models import Case
from apps.finance.models import Invoice


@login_required
def tenant_dashboard(request):
    """
    لوحة تحكم المستأجر - Tenant Dashboard
    """
    # Check if user is a tenant
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    # Get tenant's data
    permits = Permit.objects.filter(tenant=request.user).order_by('-created_at')[:5]
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    cases = Case.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    invoices = Invoice.objects.filter(tenant=request.user).order_by('-created_at')[:5]

    # Statistics
    stats = {
        'total_permits': Permit.objects.filter(tenant=request.user).count(),
        'pending_permits': Permit.objects.filter(tenant=request.user, status='pending').count(),
        'approved_permits': Permit.objects.filter(tenant=request.user, status='approved').count(),
        'total_tickets': Ticket.objects.filter(created_by=request.user).count(),
        'open_tickets': Ticket.objects.filter(created_by=request.user, status='open').count(),
        'total_invoices': Invoice.objects.filter(tenant=request.user).count(),
        'paid_invoices': Invoice.objects.filter(
            tenant=request.user,
            status='paid'
        ).count(),
        'unpaid_invoices': Invoice.objects.filter(
            tenant=request.user
        ).exclude(
            status__in=['paid', 'cancelled']
        ).count(),
        'total_cases': Case.objects.filter(created_by=request.user).count(),
    }

    context = {
        'tenant_profile': tenant_profile,
        'permits': permits,
        'tickets': tickets,
        'cases': cases,
        'invoices': invoices,
        'stats': stats,
    }

    return render(request, 'tenants/tenant_dashboard.html', context)


@login_required
def tenant_profile(request):
    """
    ملف المستأجر - Tenant Profile
    """
    # Check if user is a tenant
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    context = {
        'tenant_profile': tenant_profile,
    }

    return render(request, 'tenants/tenant_profile.html', context)


@login_required
def tenant_permits(request):
    """
    تصاريح المستأجر - Tenant Permits
    """
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    permits = Permit.objects.filter(tenant=request.user).order_by('-created_at')

    # Filters
    status = request.GET.get('status')
    permit_type = request.GET.get('permit_type')

    if status:
        permits = permits.filter(status=status)
    if permit_type:
        permits = permits.filter(permit_type=permit_type)

    context = {
        'tenant_profile': tenant_profile,
        'permits': permits,
    }

    return render(request, 'tenants/tenant_permits.html', context)


@login_required
def tenant_invoices(request):
    """
    فواتير المستأجر - Tenant Invoices
    """
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    invoices = Invoice.objects.filter(tenant=request.user).order_by('-created_at')

    # Filters
    status = request.GET.get('status')

    if status:
        invoices = invoices.filter(status=status)

    # Calculate totals
    total_amount = sum(inv.total_amount for inv in invoices)
    paid_amount = sum(inv.paid_amount for inv in invoices)
    balance_due = total_amount - paid_amount

    context = {
        'tenant_profile': tenant_profile,
        'invoices': invoices,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'balance_due': balance_due,
    }

    return render(request, 'tenants/tenant_invoices.html', context)


@login_required
def tenant_invoice_detail(request, pk):
    """
    تفاصيل الفاتورة للمستأجر - Tenant Invoice Detail
    (Read-only - no payment creation allowed)
    """
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    # Get invoice and check ownership
    invoice = get_object_or_404(Invoice, pk=pk, tenant=request.user)

    items = invoice.items.all()
    payments = invoice.payments.all().order_by('-payment_date')

    context = {
        'invoice': invoice,
        'items': items,
        'payments': payments,
    }

    return render(request, 'tenants/tenant_invoice_detail.html', context)


@login_required
def tenant_invoice_print(request, pk):
    """
    طباعة الفاتورة للمستأجر - Tenant Invoice Print
    """
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    # Get invoice and check ownership
    invoice = get_object_or_404(Invoice, pk=pk, tenant=request.user)

    # Load invoice settings
    from apps.finance.models import InvoiceSettings
    settings = InvoiceSettings.load()

    context = {
        'invoice': invoice,
        'settings': settings,
    }

    return render(request, 'finance/invoice_print.html', context)


@login_required
def tenant_permit_create(request):
    """
    إنشاء تصريح جديد للمستأجر - Create Permit for Tenant
    """
    # Check if user is a tenant
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = PermitForm(request.POST, request.FILES, is_tenant=True)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.tenant = request.user
            permit.status = 'pending'  # Always pending for tenant-created permits
            permit.save()
            messages.success(request, _('تم إنشاء التصريح بنجاح'))
            return redirect('accounts:tenant_permits')
    else:
        form = PermitForm(is_tenant=True)

    context = {
        'form': form,
        'tenant_profile': tenant_profile,
    }

    return render(request, 'tenants/tenant_permit_create.html', context)


@login_required
def tenant_permit_detail(request, pk):
    """
    تفاصيل التصريح للمستأجر - Tenant Permit Detail
    """
    # Check if user is a tenant
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    # Get permit and ensure it belongs to this tenant
    permit = get_object_or_404(Permit, pk=pk, tenant=request.user)

    context = {
        'permit': permit,
        'tenant_profile': tenant_profile,
    }

    return render(request, 'tenants/tenant_permit_detail.html', context)


@login_required
def tenant_permit_delete(request, pk):
    """
    حذف التصريح للمستأجر - Tenant Permit Delete
    يمكن للمستأجر حذف التصاريح التي في حالة pending فقط
    """
    # Check if user is a tenant
    try:
        tenant_profile = request.user.tenant_profile
    except:
        messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
        return redirect('core:dashboard')

    # Get permit and ensure it belongs to this tenant
    permit = get_object_or_404(Permit, pk=pk, tenant=request.user)

    # Only allow deletion of pending permits
    if permit.status != 'pending':
        messages.error(request, _('لا يمكن حذف التصريح بعد بدء المراجعة'))
        return redirect('accounts:tenant_permit_detail', pk=pk)

    if request.method == 'POST':
        permit.delete()
        messages.success(request, _('تم حذف التصريح بنجاح'))
        return redirect('accounts:tenant_permits')

    context = {
        'permit': permit,
        'tenant_profile': tenant_profile,
    }

    return render(request, 'tenants/tenant_permit_delete.html', context)
