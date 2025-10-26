from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from apps.core.utils import generate_code


class Permit(models.Model):
    """
    التصاريح - Permits
    """
    PERMIT_TYPE_CHOICES = [
        ('goods', _('بضائع')),
        ('maintenance', _('صيانة')),
        ('marketing', _('تسويق')),
        ('visitor', _('زائر')),
        ('vehicle', _('مركبة')),
        ('other', _('أخرى')),
    ]

    DIRECTION_CHOICES = [
        ('send', _('إرسال')),
        ('receive', _('استقبال')),
    ]

    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('approved', _('موافق عليه')),
        ('rejected', _('مرفوض')),
        ('cancelled', _('ملغي')),
    ]

    # معلومات أساسية - Basic Information
    permit_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم التصريح')
    )

    permit_type = models.CharField(
        max_length=20,
        choices=PERMIT_TYPE_CHOICES,
        verbose_name=_('نوع التصريح')
    )

    direction = models.CharField(
        max_length=10,
        choices=DIRECTION_CHOICES,
        verbose_name=_('الاتجاه')
    )

    # المستخدم والمستأجر - User and Tenant
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_permits',
        verbose_name=_('أنشئ بواسطة')
    )

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='permits',
        verbose_name=_('المستأجر')
    )

    # تفاصيل التصريح - Permit Details
    title = models.CharField(
        max_length=200,
        verbose_name=_('العنوان')
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('الوصف')
    )

    # معلومات إضافية - Additional Information
    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('اسم الشركة')
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('الشخص المسؤول')
    )

    contact_phone = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('هاتف الاتصال')
    )

    # التواريخ - Dates
    requested_date = models.DateField(
        verbose_name=_('تاريخ الطلب')
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ البداية')
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ النهاية')
    )

    # الحالة - Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )

    # ملاحظات - Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ملاحظات')
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('سبب الرفض')
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
        """Override save to auto-generate permit_number"""
        if not self.permit_number:
            self.permit_number = generate_code(Permit, 'permit_number', 'PRM', 3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('التصريح')
        verbose_name_plural = _('التصاريح')
        db_table = 'permits_permit'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['permit_number']),
            models.Index(fields=['status']),
            models.Index(fields=['tenant']),
        ]

    def __str__(self):
        return f"{self.permit_number} - {self.title}"


class PermitAttachment(models.Model):
    """
    مرفقات التصريح - Permit Attachments
    """
    permit = models.ForeignKey(
        Permit,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('التصريح')
    )

    file = models.FileField(
        upload_to='permits/attachments/%Y/%m/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        verbose_name=_('الملف')
    )

    file_name = models.CharField(
        max_length=255,
        verbose_name=_('اسم الملف')
    )

    file_size = models.IntegerField(
        verbose_name=_('حجم الملف (بايت)')
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('رفع بواسطة')
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('الوصف')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الرفع')
    )

    class Meta:
        verbose_name = _('مرفق تصريح')
        verbose_name_plural = _('مرفقات التصاريح')
        db_table = 'permits_attachment'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.permit.permit_number} - {self.file_name}"


class PermitApproval(models.Model):
    """
    موافقات التصريح - Permit Approvals
    """
    ACTION_CHOICES = [
        ('approved', _('موافق - Approved')),
        ('rejected', _('مرفوض - Rejected')),
        ('redirected', _('محول - Redirected')),
    ]

    permit = models.ForeignKey(
        Permit,
        on_delete=models.CASCADE,
        related_name='approvals',
        verbose_name=_('التصريح')
    )

    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='permit_approvals',
        verbose_name=_('الموافق')
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name=_('الإجراء')
    )

    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('التعليقات')
    )

    redirected_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redirected_permits',
        verbose_name=_('محول إلى')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإجراء')
    )

    class Meta:
        verbose_name = _('موافقة التصريح')
        verbose_name_plural = _('موافقات التصاريح')
        db_table = 'permits_approval'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.permit.permit_number} - {self.get_action_display()}"


class ApprovalWorkflow(models.Model):
    """
    سير عمل الموافقات - Approval Workflow
    يحدد من يستطيع الموافقة على أنواع معينة من الطلبات
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('اسم سير العمل')
    )

    permit_type = models.CharField(
        max_length=20,
        choices=Permit.PERMIT_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('نوع التصريح')
    )

    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='approval_workflows',
        verbose_name=_('المسؤول عن الموافقة')
    )

    backup_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backup_workflows',
        verbose_name=_('المسؤول البديل')
    )

    # المهلة الزمنية بالساعات
    deadline_hours = models.IntegerField(
        default=24,
        verbose_name=_('المهلة الزمنية (ساعات)')
    )

    # تحويل تلقائي عند تجاوز المهلة
    auto_redirect = models.BooleanField(
        default=True,
        verbose_name=_('تحويل تلقائي عند تجاوز المهلة')
    )

    # إشعار المدير عند التحويل
    notify_admin = models.BooleanField(
        default=True,
        verbose_name=_('إشعار المدير عند التحويل')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    class Meta:
        verbose_name = _('سير عمل الموافقة')
        verbose_name_plural = _('سير عمل الموافقات')
        db_table = 'permits_approval_workflow'
        ordering = ['permit_type', 'name']

    def __str__(self):
        return f"{self.name} - {self.approver.get_full_name()}"


class PendingApproval(models.Model):
    """
    الموافقات المعلقة - Pending Approvals
    تتبع الطلبات المعلقة والمهل الزمنية
    """
    permit = models.ForeignKey(
        Permit,
        on_delete=models.CASCADE,
        related_name='pending_approvals',
        verbose_name=_('التصريح')
    )

    workflow = models.ForeignKey(
        ApprovalWorkflow,
        on_delete=models.CASCADE,
        related_name='pending_approvals',
        verbose_name=_('سير العمل')
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pending_approvals',
        verbose_name=_('مسند إلى')
    )

    deadline = models.DateTimeField(
        verbose_name=_('الموعد النهائي')
    )

    is_overdue = models.BooleanField(
        default=False,
        verbose_name=_('متأخر')
    )

    redirected = models.BooleanField(
        default=False,
        verbose_name=_('تم التحويل')
    )

    redirected_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ التحويل')
    )

    redirected_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redirected_approvals',
        verbose_name=_('محول إلى')
    )

    admin_notified = models.BooleanField(
        default=False,
        verbose_name=_('تم إشعار المدير')
    )

    completed = models.BooleanField(
        default=False,
        verbose_name=_('مكتمل')
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الإكمال')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    class Meta:
        verbose_name = _('موافقة معلقة')
        verbose_name_plural = _('موافقات معلقة')
        db_table = 'permits_pending_approval'
        ordering = ['deadline', '-created_at']

    def __str__(self):
        return f"{self.permit.permit_number} - {self.assigned_to.get_full_name()}"

    def check_deadline(self):
        """فحص المهلة الزمنية وتحويل تلقائي إذا لزم الأمر"""
        from django.utils import timezone
        from apps.core.models import Notification

        if self.completed or self.redirected:
            return

        now = timezone.now()

        if now > self.deadline:
            self.is_overdue = True

            # تحويل تلقائي إذا كان مفعل
            if self.workflow.auto_redirect and self.workflow.backup_approver:
                self.redirected = True
                self.redirected_at = now
                self.redirected_to = self.workflow.backup_approver
                self.assigned_to = self.workflow.backup_approver

                # إنشاء إشعار للمسؤول البديل
                Notification.create_notification(
                    user=self.workflow.backup_approver,
                    title=_('طلب محول إليك'),
                    message=_('تم تحويل التصريح %(number)s إليك بسبب تجاوز المهلة الزمنية') % {
                        'number': self.permit.permit_number
                    },
                    notification_type='permit',
                    link=f'/permits/{self.permit.pk}/'
                )

                # إشعار المدير إذا كان مفعل
                if self.workflow.notify_admin and not self.admin_notified:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    admins = User.objects.filter(is_superuser=True)

                    for admin in admins:
                        Notification.create_notification(
                            user=admin,
                            title=_('تحويل تلقائي بسبب تجاوز المهلة'),
                            message=_('تم تحويل التصريح %(number)s من %(from_user)s إلى %(to_user)s بسبب تجاوز المهلة الزمنية') % {
                                'number': self.permit.permit_number,
                                'from_user': self.workflow.approver.get_full_name(),
                                'to_user': self.workflow.backup_approver.get_full_name()
                            },
                            notification_type='warning',
                            link=f'/permits/{self.permit.pk}/'
                        )

                    self.admin_notified = True

            self.save()


class Task(models.Model):
    """
    المهام - Tasks
    مهام مسندة للمستخدمين مرتبطة بالتصاريح
    """
    STATUS_CHOICES = [
        ('pending', _('معلقة')),
        ('in_progress', _('قيد التنفيذ')),
        ('completed', _('مكتملة')),
        ('cancelled', _('ملغاة')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('منخفضة')),
        ('medium', _('متوسطة')),
        ('high', _('عالية')),
        ('urgent', _('عاجلة')),
    ]

    permit = models.ForeignKey(
        Permit,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('التصريح')
    )

    title = models.CharField(
        max_length=200,
        verbose_name=_('عنوان المهمة')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('الوصف')
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        verbose_name=_('مسند إلى')
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
        verbose_name=_('أسند بواسطة')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name=_('الأولوية')
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الاستحقاق')
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الإكمال')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
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
        verbose_name = _('مهمة')
        verbose_name_plural = _('المهام')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.assigned_to.get_full_name()}"

