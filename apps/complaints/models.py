from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from apps.core.utils import generate_code


class Case(models.Model):
    """
    الحالات (شكاوى، مجاملات، اقتراحات) - Cases
    """
    CASE_TYPE_CHOICES = [
        ('complaint', _('شكوى')),
        ('complement', _('مجاملة')),
        ('suggestion', _('اقتراح')),
    ]

    STATUS_CHOICES = [
        ('open', _('مفتوحة')),
        ('in_review', _('قيد المراجعة')),
        ('resolved', _('محلولة')),
        ('closed', _('مغلقة')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('منخفضة')),
        ('medium', _('متوسطة')),
        ('high', _('عالية')),
    ]

    case_number = models.CharField(max_length=50, unique=True, verbose_name=_('رقم الحالة'))
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, verbose_name=_('نوع الحالة'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    description = models.TextField(verbose_name=_('الوصف'))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name=_('الأولوية'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name=_('الحالة'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_cases', verbose_name=_('أنشئ بواسطة'))
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases', verbose_name=_('مسند إلى'))

    department = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('القسم المعني'))
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name=_('تاريخ الحل'))
    closed_at = models.DateTimeField(blank=True, null=True, verbose_name=_('تاريخ الإغلاق'))
    resolution_notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات الحل'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def save(self, *args, **kwargs):
        """Override save to auto-generate case_number"""
        if not self.case_number:
            self.case_number = generate_code(Case, 'case_number', 'CSE', 3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('الحالة')
        verbose_name_plural = _('الحالات')
        db_table = 'complaints_case'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.case_number} - {self.title}"


class CaseAttachment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='attachments', verbose_name=_('الحالة'))
    file = models.FileField(upload_to='complaints/attachments/%Y/%m/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])], verbose_name=_('الملف'))
    file_name = models.CharField(max_length=255, verbose_name=_('اسم الملف'))
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('رفع بواسطة'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الرفع'))

    class Meta:
        verbose_name = _('مرفق الحالة')
        verbose_name_plural = _('مرفقات الحالات')
        db_table = 'complaints_attachment'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.case.case_number} - {self.file_name}"


class CaseComment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='comments', verbose_name=_('الحالة'))
    comment = models.TextField(verbose_name=_('التعليق'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('أنشئ بواسطة'))
    is_internal = models.BooleanField(default=False, verbose_name=_('تعليق داخلي'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))

    class Meta:
        verbose_name = _('تعليق الحالة')
        verbose_name_plural = _('تعليقات الحالات')
        db_table = 'complaints_comment'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.case.case_number} - {self.created_by}"
