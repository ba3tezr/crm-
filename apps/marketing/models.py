from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from apps.core.utils import generate_code


class Event(models.Model):
    """
    الفعاليات التسويقية - Marketing Events
    """
    EVENT_TYPE_CHOICES = [
        ('activation', _('تفعيل')),
        ('campaign', _('حملة')),
        ('promotion', _('عرض ترويجي')),
        ('exhibition', _('معرض')),
        ('seminar', _('ندوة')),
        ('workshop', _('ورشة عمل')),
        ('conference', _('مؤتمر')),
        ('other', _('أخرى')),
    ]

    STATUS_CHOICES = [
        ('planned', _('مخطط')),
        ('active', _('نشط')),
        ('completed', _('مكتمل')),
        ('cancelled', _('ملغي')),
    ]

    event_number = models.CharField(max_length=50, unique=True, verbose_name=_('رقم الفعالية'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    description = models.TextField(verbose_name=_('الوصف'))
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, verbose_name=_('نوع الفعالية'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name=_('الحالة'))

    start_date = models.DateField(verbose_name=_('تاريخ البداية'))
    end_date = models.DateField(verbose_name=_('تاريخ النهاية'))
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('الموقع'))
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('الميزانية'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_events', verbose_name=_('أنشئ بواسطة'))
    responsible_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_events', verbose_name=_('الشخص المسؤول'))

    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def save(self, *args, **kwargs):
        """Override save to auto-generate event_number"""
        if not self.event_number:
            self.event_number = generate_code(Event, 'event_number', 'EVT', 3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('الفعالية التسويقية')
        verbose_name_plural = _('الفعاليات التسويقية')
        db_table = 'marketing_event'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.event_number} - {self.title}"


class Activation(models.Model):
    """
    التفعيلات - Activations
    """
    activation_number = models.CharField(max_length=50, unique=True, verbose_name=_('رقم التفعيل'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activations', verbose_name=_('الفعالية'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    description = models.TextField(blank=True, null=True, verbose_name=_('الوصف'))

    activation_date = models.DateField(verbose_name=_('تاريخ التفعيل'))
    participants_count = models.IntegerField(default=0, verbose_name=_('عدد المشاركين'))
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('نسبة النجاح %'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('أنشئ بواسطة'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('التفعيل')
        verbose_name_plural = _('التفعيلات')
        db_table = 'marketing_activation'
        ordering = ['-activation_date']

    def __str__(self):
        return f"{self.activation_number} - {self.title}"
