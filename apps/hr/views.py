"""
Views for HR App
إدارة الموارد البشرية
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils import timezone

from .models import LeaveRequest, Attendance
from .forms import LeaveRequestForm, LeaveRequestApprovalForm, AttendanceForm
from apps.core.decorators import staff_required


@login_required
@staff_required
def leave_request_list(request):
    """
    عرض قائمة طلبات الإجازات - Leave Requests List
    """
    leave_requests = LeaveRequest.objects.all().select_related(
        'employee', 'approved_by'
    ).order_by('-created_at')

    # Statistics
    pending_count = leave_requests.filter(status='pending').count()
    approved_count = leave_requests.filter(status='approved').count()
    rejected_count = leave_requests.filter(status='rejected').count()
    total_count = leave_requests.count()

    # Filters
    leave_type = request.GET.get('leave_type')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    search = request.GET.get('search')

    if leave_type:
        leave_requests = leave_requests.filter(leave_type=leave_type)
    if status:
        leave_requests = leave_requests.filter(status=status)
    if start_date:
        leave_requests = leave_requests.filter(start_date__gte=start_date)
    if search:
        leave_requests = leave_requests.filter(
            Q(request_number__icontains=search) |
            Q(employee__first_name__icontains=search) |
            Q(employee__last_name__icontains=search) |
            Q(reason__icontains=search)
        )

    # Pagination
    paginator = Paginator(leave_requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'leave_requests': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'total_count': total_count,
    }

    return render(request, 'hr/leave_request_list.html', context)


@login_required
@staff_required
def leave_request_detail(request, pk):
    """
    عرض تفاصيل طلب الإجازة - Leave Request Detail
    """
    leave_request = get_object_or_404(
        LeaveRequest.objects.select_related('employee', 'approved_by'),
        pk=pk
    )

    context = {
        'leave_request': leave_request,
    }

    return render(request, 'hr/leave_request_detail.html', context)


@login_required
@staff_required
def leave_request_create(request):
    """
    إنشاء طلب إجازة جديد - Create Leave Request
    """
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            if not leave_request.employee:
                leave_request.employee = request.user
            leave_request.save()
            messages.success(request, _('تم إنشاء طلب الإجازة بنجاح'))
            return redirect('hr:leave_request_detail', pk=leave_request.pk)
    else:
        form = LeaveRequestForm(initial={'employee': request.user})

    context = {
        'form': form,
        'title': _('إنشاء طلب إجازة جديد'),
    }

    return render(request, 'hr/leave_request_form.html', context)


@login_required
@staff_required
def leave_request_update(request, pk):
    """
    تعديل طلب الإجازة - Update Leave Request
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Check permissions
    if leave_request.employee != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لتعديل هذا الطلب'))
        return redirect('hr:leave_request_detail', pk=pk)

    # Can only edit pending requests
    if leave_request.status != 'pending':
        messages.error(request, _('لا يمكن تعديل طلب تمت الموافقة عليه أو رفضه'))
        return redirect('hr:leave_request_detail', pk=pk)

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث طلب الإجازة بنجاح'))
            return redirect('hr:leave_request_detail', pk=pk)
    else:
        form = LeaveRequestForm(instance=leave_request)

    context = {
        'form': form,
        'leave_request': leave_request,
        'title': _('تعديل طلب الإجازة'),
    }

    return render(request, 'hr/leave_request_form.html', context)


@login_required
@staff_required
def leave_request_delete(request, pk):
    """
    حذف طلب الإجازة - Delete Leave Request
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Check permissions
    if leave_request.employee != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لحذف هذا الطلب'))
        return redirect('hr:leave_request_detail', pk=pk)

    # Can only delete pending requests
    if leave_request.status != 'pending':
        messages.error(request, _('لا يمكن حذف طلب تمت الموافقة عليه أو رفضه'))
        return redirect('hr:leave_request_detail', pk=pk)

    if request.method == 'POST':
        leave_request.delete()
        messages.success(request, _('تم حذف طلب الإجازة بنجاح'))
        return redirect('hr:leave_request_list')

    context = {
        'leave_request': leave_request,
    }

    return render(request, 'hr/leave_request_confirm_delete.html', context)


@login_required
@staff_required
def leave_request_approve(request, pk):
    """
    الموافقة على طلب الإجازة - Approve Leave Request
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية للموافقة على طلبات الإجازات'))
        return redirect('hr:leave_request_detail', pk=pk)

    if leave_request.status == 'pending':
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.save()

        messages.success(request, _('تمت الموافقة على طلب الإجازة بنجاح'))
    else:
        messages.warning(request, _('الطلب ليس في حالة الانتظار'))

    return redirect('hr:leave_request_detail', pk=pk)


@login_required
@staff_required
def leave_request_reject(request, pk):
    """
    رفض طلب الإجازة - Reject Leave Request
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لرفض طلبات الإجازات'))
        return redirect('hr:leave_request_detail', pk=pk)

    if leave_request.status == 'pending':
        leave_request.status = 'rejected'
        leave_request.save()

        messages.success(request, _('تم رفض طلب الإجازة'))
    else:
        messages.warning(request, _('الطلب ليس في حالة الانتظار'))

    return redirect('hr:leave_request_detail', pk=pk)


@login_required
@staff_required
def leave_request_export(request):
    """
    تصدير طلبات الإجازات إلى Excel - Export Leave Requests to Excel
    """
    # سيتم تنفيذها في المرحلة القادمة
    messages.info(request, _('سيتم تنفيذ هذه الميزة قريباً'))
    return redirect('hr:leave_request_list')
