"""
Finance Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Sum
from .models import Invoice, InvoiceItem, Payment
from .forms import InvoiceForm, PaymentForm, InvoiceItemFormSet
from apps.core.decorators import staff_required


@login_required
@staff_required
def invoice_list(request):
    """قائمة الفواتير - Invoice List"""
    invoices = Invoice.objects.all().select_related('tenant', 'created_by').order_by('-created_at')

    # Filters
    status = request.GET.get('status')
    invoice_type = request.GET.get('invoice_type')
    search = request.GET.get('search')

    if status:
        invoices = invoices.filter(status=status)
    if invoice_type:
        invoices = invoices.filter(invoice_type=invoice_type)
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) |
            Q(tenant__username__icontains=search) |
            Q(tenant__tenant_profile__company_name__icontains=search)
        )

    # Statistics
    stats = {
        'total_invoices': Invoice.objects.count(),
        'pending_invoices': Invoice.objects.filter(status='pending').count(),
        'paid_invoices': Invoice.objects.filter(status='paid').count(),
        'overdue_invoices': Invoice.objects.filter(status='overdue').count(),
        'total_amount': Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'paid_amount': Invoice.objects.filter(status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }

    context = {
        'invoices': invoices,
        'stats': stats,
    }
    return render(request, 'finance/invoice_list.html', context)


@login_required
@staff_required
def invoice_detail(request, pk):
    """تفاصيل الفاتورة - Invoice Detail"""
    invoice = get_object_or_404(Invoice.objects.select_related('tenant', 'created_by'), pk=pk)
    items = invoice.items.all()
    payments = invoice.payments.all().order_by('-payment_date')

    context = {
        'invoice': invoice,
        'items': items,
        'payments': payments,
    }
    return render(request, 'finance/invoice_detail.html', context)


@login_required
@staff_required
def invoice_create(request):
    """إنشاء فاتورة جديدة - Create Invoice"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()

            # Save invoice items
            formset.instance = invoice
            formset.save()

            # Recalculate totals
            invoice.calculate_totals()

            messages.success(request, _('تم إنشاء الفاتورة بنجاح'))
            return redirect('finance:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'finance/invoice_form.html', context)


@login_required
@staff_required
def invoice_edit(request, pk):
    """تعديل الفاتورة - Edit Invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            # Recalculate totals
            invoice.calculate_totals()

            messages.success(request, _('تم تحديث الفاتورة بنجاح'))
            return redirect('finance:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)

    context = {
        'form': form,
        'formset': formset,
        'invoice': invoice,
    }
    return render(request, 'finance/invoice_form.html', context)


@login_required
@staff_required
def invoice_delete(request, pk):
    """حذف الفاتورة - Delete Invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        messages.success(request, _('تم حذف الفاتورة بنجاح'))
        return redirect('finance:invoice_list')

    context = {'invoice': invoice}
    return render(request, 'finance/invoice_confirm_delete.html', context)


@login_required
@staff_required
def payment_list(request):
    """قائمة المدفوعات - Payment List"""
    payments = Payment.objects.all().select_related('invoice', 'created_by').order_by('-payment_date')

    # Filters
    payment_method = request.GET.get('payment_method')
    search = request.GET.get('search')

    if payment_method:
        payments = payments.filter(payment_method=payment_method)
    if search:
        payments = payments.filter(
            Q(payment_number__icontains=search) |
            Q(invoice__invoice_number__icontains=search) |
            Q(reference_number__icontains=search)
        )

    # Statistics
    stats = {
        'total_payments': Payment.objects.count(),
        'total_amount': Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    context = {
        'payments': payments,
        'stats': stats,
    }
    return render(request, 'finance/payment_list.html', context)


@login_required
@staff_required
def payment_create(request):
    """إنشاء دفعة جديدة - Create Payment"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.created_by = request.user
            payment.save()
            messages.success(request, _('تم تسجيل الدفعة بنجاح'))
            return redirect('finance:invoice_detail', pk=payment.invoice.pk)
    else:
        # Pre-fill invoice if provided in URL
        invoice_id = request.GET.get('invoice')
        initial = {}
        if invoice_id:
            initial['invoice'] = invoice_id
        form = PaymentForm(initial=initial)

    context = {'form': form}
    return render(request, 'finance/payment_form.html', context)
