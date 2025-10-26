from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import SystemSettings


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """
    لوحة تحكم إعدادات النظام
    System Settings Admin Panel
    """
    fieldsets = (
        (_('معلومات النظام'), {
            'fields': ('site_name_ar', 'site_name_en')
        }),
        (_('الشعارات'), {
            'fields': ('logo_ar', 'logo_en', 'logo_preview')
        }),
        (_('خلفية شاشة تسجيل الدخول'), {
            'fields': (
                'use_background_image',
                'login_background_image',
                'login_background_color',
                'background_preview'
            ),
            'description': _('يمكنك اختيار صورة خلفية أو لون خلفية لشاشة تسجيل الدخول')
        }),
        (_('نصوص شاشة تسجيل الدخول'), {
            'fields': (
                'login_page_title_ar',
                'login_page_title_en',
                'login_page_subtitle_ar',
                'login_page_subtitle_en',
            )
        }),
        (_('الفوتر'), {
            'fields': ('footer_text_ar', 'footer_text_en')
        }),
        (_('معلومات التحديث'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('logo_preview', 'background_preview', 'created_at', 'updated_at')

    def logo_preview(self, obj):
        """معاينة الشعارات"""
        html = '<div style="display: flex; gap: 20px;">'
        if obj.logo_ar:
            html += f'''
                <div>
                    <p><strong>{_("الشعار العربي")}:</strong></p>
                    <img src="{obj.logo_ar.url}" style="max-width: 200px; max-height: 100px;" />
                </div>
            '''
        if obj.logo_en:
            html += f'''
                <div>
                    <p><strong>{_("الشعار الإنجليزي")}:</strong></p>
                    <img src="{obj.logo_en.url}" style="max-width: 200px; max-height: 100px;" />
                </div>
            '''
        html += '</div>'
        return format_html(html) if (obj.logo_ar or obj.logo_en) else '-'
    logo_preview.short_description = _('معاينة الشعارات')

    def background_preview(self, obj):
        """معاينة الخلفية"""
        if obj.use_background_image and obj.login_background_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />',
                obj.login_background_image.url
            )
        else:
            return format_html(
                '<div style="width: 300px; height: 100px; background: {}; border-radius: 8px;"></div>',
                obj.login_background_color
            )
    background_preview.short_description = _('معاينة الخلفية')

    def has_add_permission(self, request):
        """منع إضافة سجلات جديدة (Singleton)"""
        return not SystemSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """منع الحذف"""
        return False

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
