from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Department, CustomUser, TenantProfile, DepartmentPermission
from .forms import DepartmentPermissionForm


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    لوحة تحكم الأقسام
    """
    list_display = ('name', 'name_ar', 'name_en', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_ar', 'name_en', 'description')
    ordering = ('name',)

    fieldsets = (
        (_('معلومات القسم'), {
            'fields': ('name', 'name_ar', 'name_en', 'description')
        }),
        (_('الحالة'), {
            'fields': ('is_active',)
        }),
        (_('التواريخ'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


class DepartmentPermissionInline(admin.TabularInline):
    """
    صلاحيات الأقسام كـ Inline في صفحة المستخدم
    """
    model = DepartmentPermission
    form = DepartmentPermissionForm
    extra = 1
    fields = ('module', 'permissions', 'is_active')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    لوحة تحكم المستخدمين
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'department', 'preferred_language')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'employee_id')
    ordering = ('-date_joined',)
    inlines = [DepartmentPermissionInline]

    fieldsets = (
        (_('معلومات تسجيل الدخول'), {
            'fields': ('username', 'password')
        }),
        (_('المعلومات الشخصية'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile', 'profile_image')
        }),
        (_('معلومات العمل'), {
            'fields': ('department', 'job_title', 'employee_id', 'hire_date')
        }),
        (_('معلومات إضافية'), {
            'fields': ('address', 'date_of_birth', 'preferred_language')
        }),
        (_('الصلاحيات'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('التواريخ'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'department', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    """
    لوحة تحكم ملفات المستأجرين
    """
    list_display = ('tenant_id', 'user', 'unit_number', 'contract_number', 'contract_start_date', 'contract_end_date', 'is_active')
    list_filter = ('is_active', 'contract_start_date', 'contract_end_date', 'building_name')
    search_fields = ('tenant_id', 'user__username', 'user__first_name', 'user__last_name', 'company_name', 'unit_number', 'contract_number')
    ordering = ('-created_at',)

    fieldsets = (
        (_('المستخدم'), {
            'fields': ('user',)
        }),
        (_('معلومات المستأجر'), {
            'fields': ('tenant_id', 'company_name', 'unit_number', 'floor_number', 'building_name')
        }),
        (_('معلومات العقد'), {
            'fields': ('contract_number', 'contract_start_date', 'contract_end_date')
        }),
        (_('معلومات الاتصال للطوارئ'), {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        (_('الحالة والملاحظات'), {
            'fields': ('is_active', 'notes')
        }),
        (_('التواريخ'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(DepartmentPermission)
class DepartmentPermissionAdmin(admin.ModelAdmin):
    """
    لوحة تحكم صلاحيات الأقسام
    """
    form = DepartmentPermissionForm
    list_display = ('user', 'module', 'get_permissions_display', 'is_active', 'created_at')
    list_filter = ('module', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('user', 'module')

    fieldsets = (
        (_('المستخدم والمديول'), {
            'fields': ('user', 'module')
        }),
        (_('الصلاحيات'), {
            'fields': ('permissions', 'is_active'),
            'description': _('اختر الصلاحيات المطلوبة')
        }),
        (_('التواريخ'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def get_permissions_display(self, obj):
        """عرض الصلاحيات بشكل مقروء"""
        if not obj.permissions:
            return '-'

        permission_map = {
            'view': _('عرض'),
            'add': _('إضافة'),
            'change': _('تعديل'),
            'delete': _('حذف'),
            'export': _('تصدير'),
            'approve': _('موافقة'),
        }

        perms = [str(permission_map.get(p, p)) for p in obj.permissions]
        return ', '.join(perms)

    get_permissions_display.short_description = _('الصلاحيات')
