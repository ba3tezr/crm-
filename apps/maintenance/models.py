from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from apps.core.utils import generate_code


class Ticket(models.Model):
    """
    تذاكر الصيانة - Maintenance Tickets
    """
    PRIORITY_CHOICES = [
        ('low', _('منخفضة')),
        ('medium', _('متوسطة')),
        ('high', _('عالية')),
        ('urgent', _('عاجلة')),
    ]

    STATUS_CHOICES = [
        ('open', _('مفتوحة')),
        ('in_progress', _('قيد التنفيذ')),
        ('pending', _('معلقة')),
        ('resolved', _('محلولة')),
        ('closed', _('مغلقة')),
    ]

    CATEGORY_CHOICES = [
        ('electrical', _('كهرباء')),
        ('plumbing', _('سباكة')),
        ('hvac', _('تكييف')),
        ('carpentry', _('نجارة')),
        ('painting', _('دهان')),
        ('cleaning', _('نظافة')),
        ('other', _('أخرى')),
    ]

    # معلومات أساسية - Basic Information
    ticket_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم التذكرة')
    )

    title = models.CharField(
        max_length=200,
        verbose_name=_('العنوان')
    )

    description = models.TextField(
        verbose_name=_('الوصف')
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name=_('الفئة')
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name=_('الأولوية')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name=_('الحالة')
    )

    # المستخدمون - Users
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tickets',
        verbose_name=_('أنشئ بواسطة')
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        verbose_name=_('مسند إلى')
    )

    # معلومات الموقع - Location Information
    unit_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('رقم الوحدة')
    )

    floor_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('رقم الطابق')
    )

    building_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('اسم المبنى')
    )

    # التواريخ - Dates
    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ الاستحقاق')
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ الحل')
    )

    closed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ الإغلاق')
    )

    # ملاحظات - Notes
    resolution_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ملاحظات الحل')
    )

    # تواريخ النظام - System Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    def save(self, *args, **kwargs):
        """Override save to auto-generate ticket_number"""
        if not self.ticket_number:
            self.ticket_number = generate_code(Ticket, 'ticket_number', 'TKT', 3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'تذكرة الصيانة'
        verbose_name_plural = 'تذاكر الصيانة'
        db_table = 'maintenance_ticket'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"


class TicketAttachment(models.Model):
    """
    مرفقات تذكرة الصيانة - Ticket Attachments
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='التذكرة'
    )

    file = models.FileField(
        upload_to='maintenance/attachments/%Y/%m/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        verbose_name='الملف'
    )

    file_name = models.CharField(
        max_length=255,
        verbose_name='اسم الملف'
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='رفع بواسطة'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الرفع'
    )

    class Meta:
        verbose_name = 'مرفق التذكرة'
        verbose_name_plural = 'مرفقات التذاكر'
        db_table = 'maintenance_attachment'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.file_name}"


class TicketComment(models.Model):
    """
    تعليقات تذكرة الصيانة - Ticket Comments
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='التذكرة'
    )

    comment = models.TextField(
        verbose_name='التعليق'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='أنشئ بواسطة'
    )

    is_internal = models.BooleanField(
        default=False,
        verbose_name='تعليق داخلي'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )

    class Meta:
        verbose_name = 'تعليق التذكرة'
        verbose_name_plural = 'تعليقات التذاكر'
        db_table = 'maintenance_comment'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.created_by}"

