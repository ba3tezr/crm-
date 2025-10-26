from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.utils import generate_code


class LeaveRequest(models.Model):
    """
    طلبات الإجازات - Leave Requests
    """
    LEAVE_TYPE_CHOICES = [
        ('annual', _('سنوية')),
        ('sick', _('مرضية')),
        ('emergency', _('طارئة')),
        ('unpaid', _('بدون راتب')),
        ('maternity', _('أمومة')),
        ('paternity', _('أبوة')),
        ('other', _('أخرى')),
    ]

    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('approved', _('موافق عليه')),
        ('rejected', _('مرفوض')),
        ('cancelled', _('ملغي')),
    ]

    request_number = models.CharField(max_length=50, unique=True, verbose_name=_('رقم الطلب'))
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests', verbose_name=_('الموظف'))
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, verbose_name=_('نوع الإجازة'))

    start_date = models.DateField(verbose_name=_('تاريخ البداية'))
    end_date = models.DateField(verbose_name=_('تاريخ النهاية'))
    days_count = models.IntegerField(verbose_name=_('عدد الأيام'))
    reason = models.TextField(verbose_name=_('السبب'))

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('الحالة'))
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves', verbose_name=_('وافق عليه'))
    approval_date = models.DateTimeField(blank=True, null=True, verbose_name=_('تاريخ الموافقة'))
    rejection_reason = models.TextField(blank=True, null=True, verbose_name=_('سبب الرفض'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def save(self, *args, **kwargs):
        """Override save to auto-generate request_number"""
        if not self.request_number:
            self.request_number = generate_code(LeaveRequest, 'request_number', 'LVE', 3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('طلب إجازة')
        verbose_name_plural = _('طلبات الإجازات')
        db_table = 'hr_leaverequest'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_number} - {self.employee.get_full_name()}"


class Attendance(models.Model):
    """
    الحضور - Attendance
    """
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('الموظف'))
    date = models.DateField(verbose_name=_('التاريخ'))
    check_in = models.TimeField(blank=True, null=True, verbose_name=_('وقت الدخول'))
    check_out = models.TimeField(blank=True, null=True, verbose_name=_('وقت الخروج'))

    is_present = models.BooleanField(default=True, verbose_name=_('حاضر'))
    is_late = models.BooleanField(default=False, verbose_name=_('متأخر'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('الحضور')
        verbose_name_plural = _('سجلات الحضور')
        db_table = 'hr_attendance'
        ordering = ['-date']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date}"
