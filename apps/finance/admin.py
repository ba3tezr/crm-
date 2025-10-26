from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Invoice, InvoiceItem, Payment


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
    list_display = ('invoice_number', 'tenant', 'invoice_type', 'total_amount', 'paid_amount', 'balance_due', 'status', 'due_date')
    list_filter = ('invoice_type', 'status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'tenant__username', 'tenant__first_name', 'tenant__last_name', 'notes')
    ordering = ('-created_at',)
    date_hierarchy = 'issue_date'

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
