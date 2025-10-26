"""
Views for Maintenance App
إدارة الصيانة
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.translation import gettext as _

from .models import Ticket, TicketAttachment, TicketComment
from .forms import TicketForm, TicketAttachmentForm, TicketCommentForm
from .resources import TicketResource
from apps.core.decorators import staff_required


@login_required
@staff_required
def ticket_list(request):
    """
    عرض قائمة طلبات الصيانة - Tickets List
    (Staff Only)
    """
    tickets = Ticket.objects.all().select_related(
        'created_by', 'assigned_to'
    ).order_by('-created_at')

    # Statistics
    urgent_count = tickets.filter(priority='urgent', status__in=['open', 'in_progress']).count()
    in_progress_count = tickets.filter(status='in_progress').count()
    completed_count = tickets.filter(status__in=['resolved', 'closed']).count()
    total_count = tickets.count()

    # Filters
    category = request.GET.get('category')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    search = request.GET.get('search')

    if category:
        tickets = tickets.filter(category=category)
    if priority:
        tickets = tickets.filter(priority=priority)
    if status:
        tickets = tickets.filter(status=status)
    if search:
        tickets = tickets.filter(
            Q(ticket_number__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Pagination
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'urgent_count': urgent_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'total_count': total_count,
    }

    return render(request, 'maintenance/ticket_list.html', context)


@login_required
@staff_required
def ticket_detail(request, pk):
    """
    عرض تفاصيل طلب الصيانة - Ticket Detail
    (Staff Only)
    """
    ticket = get_object_or_404(
        Ticket.objects.select_related('created_by', 'assigned_to'),
        pk=pk
    )

    attachments = ticket.attachments.all()
    comments = ticket.comments.all().select_related('user').order_by('created_at')

    context = {
        'ticket': ticket,
        'attachments': attachments,
        'comments': comments,
    }

    return render(request, 'maintenance/ticket_detail.html', context)


@login_required
def ticket_create(request):
    """
    إنشاء طلب صيانة جديد - Create Ticket
    (Available for both staff and tenants)
    """
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, _('تم إنشاء طلب الصيانة بنجاح'))

            # Redirect based on user type
            if hasattr(request.user, 'tenant_profile'):
                return redirect('accounts:tenant_dashboard')
            else:
                return redirect('maintenance:ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()

    context = {
        'form': form,
        'title': _('إنشاء طلب صيانة جديد'),
    }

    return render(request, 'maintenance/ticket_form.html', context)


@login_required
@staff_required
def ticket_update(request, pk):
    """
    تعديل طلب الصيانة - Update Ticket
    """
    ticket = get_object_or_404(Ticket, pk=pk)

    # Check permissions
    if ticket.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لتعديل هذا الطلب'))
        return redirect('maintenance:ticket_detail', pk=pk)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث طلب الصيانة بنجاح'))
            return redirect('maintenance:ticket_detail', pk=pk)
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'ticket': ticket,
        'title': _('تعديل طلب الصيانة'),
    }

    return render(request, 'maintenance/ticket_form.html', context)


@login_required
@staff_required
def ticket_delete(request, pk):
    """
    حذف طلب الصيانة - Delete Ticket
    """
    ticket = get_object_or_404(Ticket, pk=pk)

    # Check permissions
    if ticket.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لحذف هذا الطلب'))
        return redirect('maintenance:ticket_detail', pk=pk)

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, _('تم حذف طلب الصيانة بنجاح'))
        return redirect('maintenance:ticket_list')

    context = {
        'ticket': ticket,
    }

    return render(request, 'maintenance/ticket_confirm_delete.html', context)


@login_required
@staff_required
def ticket_export(request):
    """
    تصدير طلبات الصيانة إلى Excel - Export Tickets to Excel
    """
    queryset = Ticket.objects.select_related('created_by', 'assigned_to').all()

    # Apply filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    priority = request.GET.get('priority', '')

    if search:
        queryset = queryset.filter(
            Q(ticket_number__icontains=search) |
            Q(title__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if category:
        queryset = queryset.filter(category=category)

    if priority:
        queryset = queryset.filter(priority=priority)

    # Export to Excel
    resource = TicketResource()
    dataset = resource.export(queryset)

    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tickets_export.xlsx"'

    return response
