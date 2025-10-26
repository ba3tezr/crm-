from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Department(models.Model):
    """
    الأقسام - Departments
    """
    DEPARTMENT_CHOICES = [
        ('operations', _('العمليات - Operations')),
        ('technical', _('الفني - Technical')),
        ('marketing', _('التسويق - Marketing')),
        ('finance', _('المالية - Finance')),
        ('hr', _('الموارد البشرية - HR')),
        ('customer_services', _('خدمة العملاء - Customer Services')),
        ('maintenance', _('الصيانة - Maintenance')),
        ('security', _('الأمن - Security')),
        ('tenant', _('المستأجر - Tenant')),
    ]

    name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        unique=True,
        verbose_name=_('اسم القسم')
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالعربية')
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالإنجليزية')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('الوصف')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        verbose_name = _('القسم')
        verbose_name_plural = _('الأقسام')
        db_table = 'accounts_department'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    """
    نموذج المستخدم المخصص - Custom User Model
    """
    # معلومات إضافية - Additional Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("رقم الهاتف يجب أن يكون بالصيغة: '+999999999'. حتى 15 رقم مسموح.")
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('رقم الهاتف')
    )
    mobile = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('رقم الجوال')
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name=_('القسم')
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('المسمى الوظيفي')
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_('رقم الموظف')
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name=_('صورة الملف الشخصي')
    )

    # معلومات إضافية - Additional Info
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('العنوان')
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ الميلاد')
    )

    hire_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ التعيين')
    )

    # الحالة - Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )

    # اللغة المفضلة - Preferred Language
    LANGUAGE_CHOICES = [
        ('ar', _('العربية')),
        ('en', _('English')),
    ]

    preferred_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ar',
        verbose_name=_('اللغة المفضلة')
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
        verbose_name = _('المستخدم')
        verbose_name_plural = _('المستخدمون')
        db_table = 'accounts_customuser'
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.username

    def get_full_name(self):
        """الحصول على الاسم الكامل"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class TenantProfile(models.Model):
    """
    ملف المستأجر - Tenant Profile
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tenant_profile',
        verbose_name=_('المستخدم')
    )

    # معلومات المستأجر - Tenant Information
    tenant_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم المستأجر')
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('اسم الشركة')
    )

    unit_number = models.CharField(
        max_length=50,
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

    # معلومات العقد - Contract Information
    contract_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('رقم العقد')
    )

    contract_start_date = models.DateField(
        verbose_name=_('تاريخ بداية العقد')
    )

    contract_end_date = models.DateField(
        verbose_name=_('تاريخ نهاية العقد')
    )

    # معلومات الاتصال - Contact Information
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('اسم جهة الاتصال للطوارئ')
    )

    emergency_contact_phone = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('هاتف جهة الاتصال للطوارئ')
    )

    # الحالة - Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )

    # ملاحظات - Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ملاحظات')
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
        verbose_name = _('ملف المستأجر')
        verbose_name_plural = _('ملفات المستأجرين')
        db_table = 'accounts_tenantprofile'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant_id} - {self.user.get_full_name()}"


class DepartmentPermission(models.Model):
    """
    صلاحيات الأقسام - Department Permissions
    تحديد المديولات التي يمكن لكل قسم الوصول إليها
    """
    MODULE_CHOICES = [
        ('permits', _('التصاريح - Permits')),
        ('maintenance', _('الصيانة - Maintenance')),
        ('complaints', _('الشكاوى - Complaints')),
        ('marketing', _('التسويق - Marketing')),
        ('hr', _('الموارد البشرية - HR')),
        ('finance', _('المالية - Finance')),
    ]

    PERMISSION_CHOICES = [
        ('view', _('عرض - View')),
        ('add', _('إضافة - Add')),
        ('change', _('تعديل - Change')),
        ('delete', _('حذف - Delete')),
        ('export', _('تصدير - Export')),
        ('approve', _('موافقة - Approve')),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='department_permissions',
        verbose_name=_('المستخدم')
    )

    module = models.CharField(
        max_length=50,
        choices=MODULE_CHOICES,
        verbose_name=_('المديول')
    )

    permissions = models.JSONField(
        default=list,
        verbose_name=_('الصلاحيات'),
        help_text=_('قائمة الصلاحيات: view, add, change, delete, export, approve')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        verbose_name = _('صلاحية القسم')
        verbose_name_plural = _('صلاحيات الأقسام')
        db_table = 'accounts_department_permission'
        unique_together = ['user', 'module']
        ordering = ['user', 'module']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_module_display()}"

    def has_permission(self, permission_type):
        """التحقق من وجود صلاحية معينة"""
        return permission_type in self.permissions if self.is_active else False

