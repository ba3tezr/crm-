from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from .models import Invoice, InvoiceItem, Payment, InvoiceSettings


class InvoiceItemInline(admin.TabularInline):
    """
    بنود الفاتورة - Invoice Items Inline
    """
    model = InvoiceItem
    extra = 1
    fields = ('description', 'quantity', 'unit_price', 'total')
    readonly_fields = ('total',)


class PaymentInline(admin.TabularInline):
    """
    الدفعات - Payments Inline
    """
    model = Payment
    extra = 0
    fields = ('payment_number', 'amount', 'payment_method', 'payment_date', 'reference_number')
    readonly_fields = ('payment_number',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    لوحة تحكم الفواتير
    """
    list_display = ('invoice_number', 'tenant', 'invoice_type', 'total_amount', 'paid_amount', 'balance_due', 'status', 'due_date', 'print_button')
    list_filter = ('invoice_type', 'status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'tenant__username', 'tenant__first_name', 'tenant__last_name', 'notes')
    ordering = ('-created_at',)
    date_hierarchy = 'issue_date'
    actions = ['print_selected_invoices']

    fieldsets = (
        (_('معلومات أساسية'), {
            'fields': ('invoice_number', 'invoice_type', 'tenant', 'status')
        }),
        (_('التواريخ'), {
            'fields': ('issue_date', 'due_date')
        }),
        (_('المبالغ (USD)'), {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount')
        }),
        (_('ملاحظات'), {
            'fields': ('notes',)
        }),
        (_('التتبع'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('tax_amount', 'total_amount', 'created_at', 'updated_at')
    inlines = [InvoiceItemInline, PaymentInline]

    def balance_due(self, obj):
        return f"${obj.balance_due:,.2f}"
    balance_due.short_description = _('المبلغ المتبقي')

    def print_button(self, obj):
        """زر طباعة الفاتورة"""
        url = reverse('accounts:tenant_invoice_print', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" class="button" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">'
            '<i class="fas fa-print"></i> {}</a>',
            url,
            _('طباعة')
        )
    print_button.short_description = _('طباعة')

    def print_selected_invoices(self, request, queryset):
        """طباعة الفواتير المحددة"""
        if queryset.count() == 1:
            invoice = queryset.first()
            url = reverse('accounts:tenant_invoice_print', args=[invoice.pk])
            return format_html(
                '<script>window.open("{}", "_blank");</script>',
                url
            )
        else:
            self.message_user(request, _('يرجى اختيار فاتورة واحدة فقط للطباعة'))
    print_selected_invoices.short_description = _('طباعة الفواتير المحددة')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    لوحة تحكم الدفعات
    """
    list_display = ('payment_number', 'invoice', 'amount', 'payment_method', 'payment_date', 'created_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('payment_number', 'invoice__invoice_number', 'reference_number', 'notes')
    ordering = ('-payment_date',)
    date_hierarchy = 'payment_date'

    fieldsets = (
        (_('معلومات أساسية'), {
            'fields': ('payment_number', 'invoice', 'amount')
        }),
        (_('تفاصيل الدفع'), {
            'fields': ('payment_method', 'payment_date', 'reference_number')
        }),
        (_('ملاحظات'), {
            'fields': ('notes',)
        }),
        (_('التتبع'), {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)


@admin.register(InvoiceSettings)
class InvoiceSettingsAdmin(admin.ModelAdmin):
    """
    إعدادات الفاتورة - Invoice Settings Admin
    """
    fieldsets = (
        (_('معلومات الشركة'), {
            'fields': ('company_name_ar', 'company_name_en', 'logo')
        }),
        (_('معلومات الاتصال'), {
            'fields': ('address_ar', 'address_en', 'phone', 'email', 'website')
        }),
        (_('معلومات ضريبية'), {
            'fields': ('tax_number', 'commercial_register')
        }),
        (_('ألوان القالب'), {
            'fields': ('primary_color', 'secondary_color')
        }),
        (_('نصوص الفاتورة'), {
            'fields': ('footer_text_ar', 'footer_text_en', 'terms_ar', 'terms_en')
        }),
    )

    def has_add_permission(self, request):
        """Prevent adding more than one instance"""
        return not InvoiceSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion"""
        return False
