"""
Context Processors for Core App
معالجات السياق لتطبيق Core
"""
from django.contrib.auth import get_user_model
from .models import SystemSettings, Notification

User = get_user_model()


def system_settings(request):
    """
    إضافة إعدادات النظام لجميع القوالب
    Add system settings to all templates
    """
    settings = SystemSettings.load()
    return {
        'settings': settings,
        'CURRENCY': settings.currency,
        'CURRENCY_SYMBOL': settings.currency_symbol,
        'DATE_FORMAT': settings.date_format,
    }


def notifications(request):
    """
    إضافة الإشعارات لجميع القوالب
    Add notifications to all templates
    """
    if request.user.is_authenticated:
        unread_count = Notification.get_unread_count(request.user)
        recent_notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': recent_notifications,
        }

    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }


def switch_user_context(request):
    """
    إضافة قوائم المستخدمين للتبديل السريع (للمدراء فقط)
    Add user lists for quick switching (superusers only)
    """
    if request.user.is_authenticated and request.user.is_superuser:
        # Get tenant users (users with tenant profile)
        from apps.accounts.models import TenantProfile
        tenant_user_ids = TenantProfile.objects.values_list('user_id', flat=True)
        tenant_users = User.objects.filter(id__in=tenant_user_ids).exclude(id=request.user.id)[:10]

        # Get department managers (staff users with specific permissions)
        department_managers = User.objects.filter(
            is_staff=True,
            is_superuser=False
        ).exclude(id=request.user.id).exclude(id__in=tenant_user_ids)[:10]

        # Get regular staff (non-superuser, non-manager staff)
        staff_users = User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False
        ).exclude(id__in=tenant_user_ids)[:10]

        return {
            'tenant_users': tenant_users,
            'department_managers': department_managers,
            'staff_users': staff_users,
        }

    return {
        'tenant_users': [],
        'department_managers': [],
        'staff_users': [],
    }

