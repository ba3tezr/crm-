"""
Views for Permits App
إدارة التصاريح
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import timedelta

from .models import Permit, PermitAttachment, PermitApproval, PendingApproval, ApprovalWorkflow
from .forms import PermitForm, PermitAttachmentForm, PermitApprovalForm
from .resources import PermitResource
from apps.core.models import Notification
from apps.core.decorators import staff_required


@login_required
@staff_required
def permit_list(request):
    """
    عرض قائمة التصاريح - Permits List
    (Staff Only - المستأجرين يستخدمون tenant_permits)
    """
    permits = Permit.objects.all().select_related(
        'created_by', 'tenant'
    ).order_by('-created_at')

    # Filters
    permit_type = request.GET.get('permit_type')
    status = request.GET.get('status')
    direction = request.GET.get('direction')
    search = request.GET.get('search')

    if permit_type:
        permits = permits.filter(permit_type=permit_type)
    if status:
        permits = permits.filter(status=status)
    if direction:
        permits = permits.filter(direction=direction)
    if search:
        permits = permits.filter(
            Q(permit_number__icontains=search) |
            Q(applicant__first_name__icontains=search) |
            Q(applicant__last_name__icontains=search) |
            Q(purpose__icontains=search)
        )

    # Pagination
    paginator = Paginator(permits, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'permits': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'permits/permit_list.html', context)


@login_required
def permit_detail(request, pk):
    """
    عرض تفاصيل التصريح - Permit Detail
    """
    permit = get_object_or_404(
        Permit.objects.select_related('created_by', 'tenant'),
        pk=pk
    )

    # Check access permission
    # Tenants can only view their own permits
    if hasattr(request.user, 'tenant_profile'):
        if permit.tenant != request.user:
            messages.error(request, _('ليس لديك صلاحية الوصول لهذا التصريح'))
            return redirect('accounts:tenant_permits')
    # Staff can view all permits (no restriction)

    attachments = permit.attachments.all()
    approvals = permit.approvals.all().select_related('approved_by').order_by('-created_at')

    context = {
        'permit': permit,
        'attachments': attachments,
        'approvals': approvals,
    }

    return render(request, 'permits/permit_detail.html', context)


@login_required
@staff_required
def permit_create(request):
    """
    إنشاء تصريح جديد - Create Permit
    (Staff Only)
    """
    if request.method == 'POST':
        form = PermitForm(request.POST)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.created_by = request.user
            permit.tenant = request.user
            permit.save()
            messages.success(request, _('تم إنشاء التصريح بنجاح'))
            return redirect('permits:permit_detail', pk=permit.pk)
    else:
        form = PermitForm()

    context = {
        'form': form,
        'title': _('إنشاء تصريح جديد'),
    }

    return render(request, 'permits/permit_form.html', context)


@login_required
@staff_required
def permit_update(request, pk):
    """
    تعديل التصريح - Update Permit
    (Staff Only)
    """
    permit = get_object_or_404(Permit, pk=pk)

    # Check permissions
    if permit.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لتعديل هذا التصريح'))
        return redirect('permits:permit_detail', pk=pk)

    if request.method == 'POST':
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث التصريح بنجاح'))
            return redirect('permits:permit_detail', pk=pk)
    else:
        form = PermitForm(instance=permit)

    context = {
        'form': form,
        'permit': permit,
        'title': _('تعديل التصريح'),
    }

    return render(request, 'permits/permit_form.html', context)


@login_required
@staff_required
def permit_delete(request, pk):
    """
    حذف التصريح - Delete Permit
    (Staff Only)
    """
    permit = get_object_or_404(Permit, pk=pk)

    # Check permissions
    if permit.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لحذف هذا التصريح'))
        return redirect('permits:permit_detail', pk=pk)

    if request.method == 'POST':
        permit.delete()
        messages.success(request, _('تم حذف التصريح بنجاح'))
        return redirect('permits:permit_list')

    context = {
        'permit': permit,
    }

    return render(request, 'permits/permit_confirm_delete.html', context)


@login_required
@staff_required
def permit_export(request):
    """
    تصدير التصاريح إلى Excel - Export Permits to Excel
    (Staff Only)
    """
    queryset = Permit.objects.select_related('created_by', 'tenant').all()

    # Apply filters if provided
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    permit_type = request.GET.get('permit_type', '')

    if search:
        queryset = queryset.filter(
            Q(permit_number__icontains=search) |
            Q(title__icontains=search) |
            Q(company_name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if permit_type:
        queryset = queryset.filter(permit_type=permit_type)

    # Export to Excel
    resource = PermitResource()
    dataset = resource.export(queryset)

    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="permits_export.xlsx"'

    return response


@login_required
def attachment_upload(request, pk):
    """
    رفع مرفق للتصريح - Upload Permit Attachment
    """
    permit = get_object_or_404(Permit, pk=pk)

    if request.method == 'POST':
        file = request.FILES.get('file')
        file_name = request.POST.get('file_name')
        description = request.POST.get('description')

        if file:
            # Use original filename if no custom name provided
            if not file_name:
                file_name = file.name

            attachment = PermitAttachment.objects.create(
                permit=permit,
                file=file,
                file_name=file_name,
                description=description,
                uploaded_by=request.user
            )

            messages.success(request, _('تم رفع الملف بنجاح'))
        else:
            messages.error(request, _('الرجاء اختيار ملف'))

    return redirect('permits:permit_detail', pk=pk)


@login_required
def attachment_delete(request, pk):
    """
    حذف مرفق - Delete Attachment
    """
    attachment = get_object_or_404(PermitAttachment, pk=pk)
    permit_pk = attachment.permit.pk

    # Delete file from storage
    if attachment.file:
        attachment.file.delete()

    attachment.delete()
    messages.success(request, _('تم حذف الملف بنجاح'))

    return redirect('permits:permit_detail', pk=permit_pk)


@login_required
def permit_approve(request, pk):
    """الموافقة على التصريح أو رفضه"""
    permit = get_object_or_404(Permit, pk=pk)

    # Check if user has permission to approve
    pending_approval = PendingApproval.objects.filter(
        permit=permit,
        assigned_to=request.user,
        completed=False
    ).first()

    if not pending_approval and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية الموافقة على هذا التصريح'))
        return redirect('permits:permit_detail', pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')  # 'approved' or 'rejected'
        comments = request.POST.get('comments', '')

        # Create approval record
        approval = PermitApproval.objects.create(
            permit=permit,
            approver=request.user,
            action=action,
            comments=comments
        )

        # Update permit status
        if action == 'approved':
            permit.status = 'approved'
            permit.save()
            messages.success(request, _('تمت الموافقة على التصريح بنجاح'))

            # Notify tenant
            Notification.create_notification(
                user=permit.tenant,
                title=_('تمت الموافقة على تصريحك'),
                message=_('تمت الموافقة على التصريح %(number)s') % {'number': permit.permit_number},
                notification_type='success',
                link=f'/permits/{permit.pk}/'
            )
        elif action == 'rejected':
            permit.status = 'rejected'
            permit.save()
            messages.warning(request, _('تم رفض التصريح'))

            # Notify tenant
            Notification.create_notification(
                user=permit.tenant,
                title=_('تم رفض تصريحك'),
                message=_('تم رفض التصريح %(number)s. السبب: %(reason)s') % {
                    'number': permit.permit_number,
                    'reason': comments or _('غير محدد')
                },
                notification_type='error',
                link=f'/permits/{permit.pk}/'
            )

        # Mark pending approval as completed
        if pending_approval:
            pending_approval.completed = True
            pending_approval.completed_at = timezone.now()
            pending_approval.save()

        return redirect('permits:permit_detail', pk=pk)

    context = {
        'permit': permit,
        'pending_approval': pending_approval,
    }

    return render(request, 'permits/permit_approve.html', context)


@login_required
def my_pending_approvals(request):
    """قائمة الموافقات المعلقة للمستخدم الحالي"""
    pending_approvals = PendingApproval.objects.filter(
        assigned_to=request.user,
        completed=False
    ).select_related('permit', 'workflow').order_by('deadline')

    # Check deadlines
    for approval in pending_approvals:
        approval.check_deadline()

    context = {
        'pending_approvals': pending_approvals,
    }

    return render(request, 'permits/my_pending_approvals.html', context)
