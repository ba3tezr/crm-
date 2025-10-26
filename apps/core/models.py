from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class SystemSettings(models.Model):
    """
    إعدادات النظام العامة - Singleton Model
    System Settings - Only one record allowed
    """
    # معلومات النظام - System Information
    site_name_ar = models.CharField(
        max_length=100,
        default='نظام CRM',
        verbose_name=_('اسم الموقع (عربي)')
    )
    site_name_en = models.CharField(
        max_length=100,
        default='CRM System',
        verbose_name=_('اسم الموقع (إنجليزي)')
    )

    # شعار النظام - System Logo
    logo_ar = models.ImageField(
        upload_to='system/logos/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        null=True,
        blank=True,
        verbose_name=_('شعار النظام (عربي)'),
        help_text=_('شعار النظام للعربية - PNG, JPG, JPEG, SVG')
    )
    logo_en = models.ImageField(
        upload_to='system/logos/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        null=True,
        blank=True,
        verbose_name=_('شعار النظام (إنجليزي)'),
        help_text=_('شعار النظام للإنجليزية - PNG, JPG, JPEG, SVG')
    )

    # خلفية شاشة تسجيل الدخول - Login Background
    login_background_image = models.ImageField(
        upload_to='system/backgrounds/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        null=True,
        blank=True,
        verbose_name=_('صورة خلفية تسجيل الدخول'),
        help_text=_('صورة خلفية شاشة تسجيل الدخول - PNG, JPG, JPEG')
    )
    login_background_color = models.CharField(
        max_length=7,
        default='#0d6efd',
        verbose_name=_('لون خلفية تسجيل الدخول'),
        help_text=_('لون الخلفية (Hex Color) - يُستخدم إذا لم تكن هناك صورة')
    )
    use_background_image = models.BooleanField(
        default=True,
        verbose_name=_('استخدام صورة الخلفية'),
        help_text=_('استخدام صورة الخلفية بدلاً من اللون')
    )

    # نصوص شاشة تسجيل الدخول - Login Page Text
    login_page_title_ar = models.CharField(
        max_length=200,
        default='مرحباً بك',
        verbose_name=_('عنوان صفحة الدخول (عربي)')
    )
    login_page_title_en = models.CharField(
        max_length=200,
        default='Welcome',
        verbose_name=_('عنوان صفحة الدخول (إنجليزي)')
    )
    login_page_subtitle_ar = models.TextField(
        default='الرجاء تسجيل الدخول للمتابعة',
        verbose_name=_('عنوان فرعي (عربي)')
    )
    login_page_subtitle_en = models.TextField(
        default='Please login to continue',
        verbose_name=_('عنوان فرعي (إنجليزي)')
    )

    # Footer
    footer_text_ar = models.CharField(
        max_length=200,
        default='جميع الحقوق محفوظة © 2025',
        verbose_name=_('نص الفوتر (عربي)')
    )
    footer_text_en = models.CharField(
        max_length=200,
        default='All Rights Reserved © 2025',
        verbose_name=_('نص الفوتر (إنجليزي)')
    )

    # إعدادات العملة - Currency Settings
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('SAR', 'Saudi Riyal (﷼)'),
        ('AED', 'UAE Dirham (د.إ)'),
        ('EGP', 'Egyptian Pound (E£)'),
        ('KWD', 'Kuwaiti Dinar (د.ك)'),
        ('QAR', 'Qatari Riyal (ر.ق)'),
        ('OMR', 'Omani Rial (ر.ع)'),
        ('BHD', 'Bahraini Dinar (د.ب)'),
        ('JOD', 'Jordanian Dinar (د.أ)'),
    ]

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='EGP',
        verbose_name=_('العملة'),
        help_text=_('العملة المستخدمة في جميع أنحاء النظام - Currency symbol always in English')
    )

    currency_symbol = models.CharField(
        max_length=10,
        default='E£',
        verbose_name=_('رمز العملة'),
        help_text=_('Currency symbol (e.g., $, €, £, E£) - Always in English')
    )

    # إعدادات التاريخ - Date Settings
    DATE_FORMAT_CHOICES = [
        ('en', 'English (MM/DD/YYYY)'),
        ('en-gb', 'English UK (DD/MM/YYYY)'),
        ('iso', 'ISO (YYYY-MM-DD)'),
    ]

    date_format = models.CharField(
        max_length=10,
        choices=DATE_FORMAT_CHOICES,
        default='en',
        verbose_name=_('تنسيق التاريخ'),
        help_text=_('Date format - Always Gregorian calendar in English')
    )

    # تواريخ - Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        verbose_name = _('إعدادات النظام')
        verbose_name_plural = _('إعدادات النظام')
        db_table = 'core_system_settings'

    def save(self, *args, **kwargs):
        """Singleton Pattern - سجل واحد فقط"""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """منع الحذف - Prevent deletion"""
        pass

    @classmethod
    def load(cls):
        """تحميل الإعدادات - Load settings"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'إعدادات النظام - System Settings'


class Notification(models.Model):
    """
    الإشعارات - Notifications
    System notifications for users
    """
    NOTIFICATION_TYPES = [
        ('info', _('معلومات')),
        ('success', _('نجاح')),
        ('warning', _('تحذير')),
        ('error', _('خطأ')),
        ('permit', _('تصريح')),
        ('invoice', _('فاتورة')),
        ('payment', _('دفعة')),
        ('maintenance', _('صيانة')),
        ('complaint', _('شكوى')),
        ('event', _('فعالية')),
        ('leave', _('إجازة')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('المستخدم')
    )

    title = models.CharField(
        max_length=200,
        verbose_name=_('العنوان')
    )

    message = models.TextField(
        verbose_name=_('الرسالة')
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name=_('نوع الإشعار')
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name=_('مقروء')
    )

    link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('الرابط'),
        help_text=_('رابط للصفحة المتعلقة بالإشعار')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    class Meta:
        verbose_name = _('الإشعار')
        verbose_name_plural = _('الإشعارات')
        db_table = 'core_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @classmethod
    def create_notification(cls, user, title, message, notification_type='info', link=None):
        """
        إنشاء إشعار جديد - Create new notification
        """
        return cls.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )

    @classmethod
    def get_unread_count(cls, user):
        """
        عدد الإشعارات غير المقروءة - Get unread notifications count
        """
        return cls.objects.filter(user=user, is_read=False).count()

    @classmethod
    def mark_all_as_read(cls, user):
        """
        تعليم جميع الإشعارات كمقروءة - Mark all notifications as read
        """
        cls.objects.filter(user=user, is_read=False).update(is_read=True)
