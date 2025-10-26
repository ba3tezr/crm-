from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from apps.permits.models import Permit
from apps.maintenance.models import Ticket
from apps.complaints.models import Case
from apps.marketing.models import Event
from .models import Notification

User = get_user_model()


@login_required
def dashboard(request):
    """
    لوحة التحكم الرئيسية - Main Dashboard
    Redirects tenants to their dashboard
    """
    # Redirect tenants to their own dashboard
    if hasattr(request.user, 'tenant_profile'):
        return redirect('accounts:tenant_dashboard')

    # Get statistics for staff/admin
    permits_count = Permit.objects.count()
    permits_pending = Permit.objects.filter(status='pending').count()

    tickets_count = Ticket.objects.count()
    tickets_urgent = Ticket.objects.filter(priority='urgent', status__in=['open', 'in_progress']).count()

    cases_count = Case.objects.count()
    cases_review = Case.objects.filter(status='in_review').count()

    events_count = Event.objects.count()
    events_active = Event.objects.filter(status='active').count()

    # Get recent activities
    recent_permits = Permit.objects.select_related('tenant').order_by('-created_at')[:5]
    recent_tickets = Ticket.objects.select_related('created_by').order_by('-created_at')[:5]
    recent_cases = Case.objects.select_related('created_by').order_by('-created_at')[:5]

    # Combine and sort all activities by date
    activities = []
    
    for permit in recent_permits:
        activities.append({
            'type': 'permit',
            'type_display': _('تصريح'),
            'title': permit.permit_number,
            'status': permit.status,
            'status_display': permit.get_status_display(),
            'date': permit.created_at,
            'url': f'/permits/detail/{permit.pk}/',
        })
    
    for ticket in recent_tickets:
        activities.append({
            'type': 'ticket',
            'type_display': _('صيانة'),
            'title': ticket.ticket_number,
            'status': ticket.status,
            'status_display': ticket.get_status_display(),
            'date': ticket.created_at,
            'url': f'/maintenance/ticket/{ticket.pk}/',
        })
    
    for case in recent_cases:
        activities.append({
            'type': 'case',
            'type_display': _('شكوى'),
            'title': case.case_number,
            'status': case.status,
            'status_display': case.get_status_display(),
            'date': case.created_at,
            'url': f'/complaints/case/{case.pk}/',
        })
    
    # Sort by date (newest first) and limit to 10
    activities = sorted(activities, key=lambda x: x['date'], reverse=True)[:10]

    context = {
        'permits_count': permits_count,
        'permits_pending': permits_pending,
        'tickets_count': tickets_count,
        'tickets_urgent': tickets_urgent,
        'cases_count': cases_count,
        'cases_review': cases_review,
        'events_count': events_count,
        'events_active': events_active,
        'recent_activities': activities,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def notification_list(request):
    """
    قائمة الإشعارات - Notifications List
    """
    notifications = Notification.objects.filter(user=request.user)[:50]
    unread_count = Notification.get_unread_count(request.user)

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }

    return render(request, 'core/notification_list.html', context)


@login_required
def notification_mark_read(request, pk):
    """
    تعليم الإشعار كمقروء - Mark notification as read
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    if notification.link:
        return redirect(notification.link)
    return redirect('core:notification_list')


@login_required
def notification_mark_all_read(request):
    """
    تعليم جميع الإشعارات كمقروءة - Mark all notifications as read
    """
    Notification.mark_all_as_read(request.user)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.success(request, _('تم تعليم جميع الإشعارات كمقروءة'))
    return redirect('core:notification_list')


@login_required
def notification_get_unread(request):
    """
    الحصول على الإشعارات غير المقروءة - Get unread notifications (AJAX)
    """
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:10]

    data = {
        'count': notifications.count(),
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.notification_type,
                'link': n.link,
                'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
            }
            for n in notifications
        ]
    }

    return JsonResponse(data)


@login_required
def switch_user(request, user_id):
    """
    التبديل إلى مستخدم آخر (للمدراء فقط)
    Switch to another user (superusers only)
    """
    # Only superusers can switch users
    if not request.user.is_superuser:
        messages.error(request, _('غير مصرح لك بهذا الإجراء'))
        return redirect('core:dashboard')

    # Get target user
    target_user = get_object_or_404(User, id=user_id)

    # Store original user ID in session (if not already switching)
    if 'original_user_id' not in request.session:
        request.session['original_user_id'] = request.user.id

    # Switch to target user
    target_user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, target_user)

    messages.warning(
        request,
        _('تم التبديل إلى المستخدم: %(username)s') % {'username': target_user.username}
    )

    # Redirect to appropriate dashboard
    if hasattr(target_user, 'tenant_profile'):
        return redirect('accounts:tenant_dashboard')
    else:
        return redirect('core:dashboard')


@login_required
def switch_back(request):
    """
    العودة إلى المستخدم الأصلي
    Switch back to original user
    """
    original_user_id = request.session.get('original_user_id')

    if not original_user_id:
        messages.error(request, _('لا يوجد مستخدم أصلي للعودة إليه'))
        return redirect('core:dashboard')

    # Get original user
    original_user = get_object_or_404(User, id=original_user_id)

    # Clear session
    del request.session['original_user_id']

    # Switch back
    original_user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, original_user)

    messages.success(request, _('تم العودة إلى حسابك الأصلي'))

    return redirect('core:dashboard')
