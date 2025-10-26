"""
Views for Marketing App
إدارة التسويق والفعاليات
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.translation import gettext as _

from .models import Event, Activation
from .forms import EventForm, ActivationForm
from .resources import EventResource
from apps.core.decorators import staff_required


@login_required
@staff_required
def event_list(request):
    """
    عرض قائمة الفعاليات - Events List
    """
    events = Event.objects.all().select_related(
        'created_by', 'responsible_person'
    ).order_by('-start_date')

    # Statistics
    active_count = events.filter(status='active').count()
    upcoming_count = events.filter(status='draft').count()
    completed_count = events.filter(status='completed').count()
    total_count = events.count()

    # Filters
    event_type = request.GET.get('event_type')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    search = request.GET.get('search')

    if event_type:
        events = events.filter(event_type=event_type)
    if status:
        events = events.filter(status=status)
    if start_date:
        events = events.filter(start_date__gte=start_date)
    if search:
        events = events.filter(
            Q(event_number__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    # Pagination
    paginator = Paginator(events, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'active_count': active_count,
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'total_count': total_count,
    }

    return render(request, 'marketing/event_list.html', context)


@login_required
@staff_required
def event_detail(request, pk):
    """
    عرض تفاصيل الفعالية - Event Detail
    """
    event = get_object_or_404(
        Event.objects.select_related('created_by', 'responsible_person'),
        pk=pk
    )

    activations = event.activations.all().select_related('created_by')

    context = {
        'event': event,
        'activations': activations,
    }

    return render(request, 'marketing/event_detail.html', context)


@login_required
@staff_required
def event_create(request):
    """
    إنشاء فعالية جديدة - Create Event
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, _('تم إنشاء الفعالية بنجاح'))
            return redirect('marketing:event_detail', pk=event.pk)
    else:
        form = EventForm()

    context = {
        'form': form,
        'title': _('إنشاء فعالية جديدة'),
    }

    return render(request, 'marketing/event_form.html', context)


@login_required
@staff_required
def event_update(request, pk):
    """
    تعديل الفعالية - Update Event
    """
    event = get_object_or_404(Event, pk=pk)

    # Check permissions
    if event.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لتعديل هذه الفعالية'))
        return redirect('marketing:event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث الفعالية بنجاح'))
            return redirect('marketing:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'title': _('تعديل الفعالية'),
    }

    return render(request, 'marketing/event_form.html', context)


@login_required
@staff_required
def event_delete(request, pk):
    """
    حذف الفعالية - Delete Event
    """
    event = get_object_or_404(Event, pk=pk)

    # Check permissions
    if event.created_by != request.user and not request.user.is_staff:
        messages.error(request, _('ليس لديك صلاحية لحذف هذه الفعالية'))
        return redirect('marketing:event_detail', pk=pk)

    if request.method == 'POST':
        event.delete()
        messages.success(request, _('تم حذف الفعالية بنجاح'))
        return redirect('marketing:event_list')

    context = {
        'event': event,
    }

    return render(request, 'marketing/event_confirm_delete.html', context)


@login_required
@staff_required
def event_export(request):
    """
    تصدير الفعاليات إلى Excel - Export Events to Excel
    """
    queryset = Event.objects.select_related('created_by', 'responsible_person').all()

    # Apply filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    event_type = request.GET.get('event_type', '')

    if search:
        queryset = queryset.filter(
            Q(event_number__icontains=search) |
            Q(title__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if event_type:
        queryset = queryset.filter(event_type=event_type)

    # Export to Excel
    resource = EventResource()
    dataset = resource.export(queryset)

    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="events_export.xlsx"'

    return response
