"""
Views for Complaints App
إدارة الشكاوى والقضايا
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.translation import gettext as _

from .models import Case, CaseAttachment, CaseComment
from .forms import CaseForm, CaseAttachmentForm, CaseCommentForm
from .resources import CaseResource
from apps.core.decorators import staff_required


@login_required
@staff_required
def case_list(request):
    """
    عرض قائمة الشكاوى والقضايا - Cases List
    """
    cases = Case.objects.all().select_related(
        'created_by', 'assigned_to'
    ).order_by('-created_at')

    # Statistics
    in_review_count = cases.filter(status='in_review').count()
    resolved_count = cases.filter(status='resolved').count()
    total_count = cases.count()

    # Filters
    case_type = request.GET.get('case_type')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    search = request.GET.get('search')

    if case_type:
        cases = cases.filter(case_type=case_type)
    if priority:
        cases = cases.filter(priority=priority)
    if status:
        cases = cases.filter(status=status)
    if search:
        cases = cases.filter(
            Q(case_number__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Pagination
    paginator = Paginator(cases, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cases': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'in_review_count': in_review_count,
        'resolved_count': resolved_count,
        'total_count': total_count,
    }

    return render(request, 'complaints/case_list.html', context)


@login_required
@staff_required
def case_detail(request, pk):
    """
    عرض تفاصيل القضية - Case Detail
    """
    case = get_object_or_404(
        Case.objects.select_related('created_by', 'assigned_to'),
        pk=pk
    )

    attachments = case.attachments.all()
    comments = case.comments.all().select_related('user').order_by('created_at')

    context = {
        'case': case,
        'attachments': attachments,
        'comments': comments,
    }

    return render(request, 'complaints/case_detail.html', context)


@login_required
@staff_required
def case_create(request):
    """
    إنشاء شكوى جديدة - Create Case
    """
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user
            case.save()
            messages.success(request, _('تم إنشاء القضية بنجاح'))
            return redirect('complaints:case_detail', pk=case.pk)
    else:
        form = CaseForm()

    context = {
        'form': form,
        'title': _('إنشاء قضية جديدة'),
    }

    return render(request, 'complaints/case_form.html', context)


@login_required
@staff_required
def case_update(request, pk):
    """
    تعديل القضية - Update Case
    """
    case = get_object_or_404(Case, pk=pk)

    # Check permissions
    if case.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لتعديل هذه القضية'))
        return redirect('complaints:case_detail', pk=pk)

    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث القضية بنجاح'))
            return redirect('complaints:case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)

    context = {
        'form': form,
        'case': case,
        'title': _('تعديل القضية'),
    }

    return render(request, 'complaints/case_form.html', context)


@login_required
@staff_required
def case_delete(request, pk):
    """
    حذف القضية - Delete Case
    """
    case = get_object_or_404(Case, pk=pk)

    # Check permissions
    if case.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لحذف هذه القضية'))
        return redirect('complaints:case_detail', pk=pk)

    if request.method == 'POST':
        case.delete()
        messages.success(request, _('تم حذف القضية بنجاح'))
        return redirect('complaints:case_list')

    context = {
        'case': case,
    }

    return render(request, 'complaints/case_confirm_delete.html', context)


@login_required
@staff_required
def case_export(request):
    """
    تصدير الشكاوى إلى Excel - Export Cases to Excel
    """
    queryset = Case.objects.select_related('created_by', 'assigned_to').all()

    # Apply filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    case_type = request.GET.get('case_type', '')
    priority = request.GET.get('priority', '')

    if search:
        queryset = queryset.filter(
            Q(case_number__icontains=search) |
            Q(title__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if case_type:
        queryset = queryset.filter(case_type=case_type)

    if priority:
        queryset = queryset.filter(priority=priority)

    # Export to Excel
    resource = CaseResource()
    dataset = resource.export(queryset)

    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="cases_export.xlsx"'

    return response
