"""
Finance App Models
نماذج القسم المالي
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.utils import generate_code

User = get_user_model()


class Invoice(models.Model):
    """
    فاتورة - Invoice
    """
    INVOICE_TYPE_CHOICES = [
        ('sales', _('مبيعات')),
        ('purchase', _('مشتريات')),
        ('service', _('خدمة')),
        ('rental', _('إيجار')),
        ('penalty', _('غرامة')),
    ]

    STATUS_CHOICES = [
        ('draft', _('مسودة')),
        ('pending', _('قيد الانتظار')),
        ('paid', _('مدفوعة')),
        ('partially_paid', _('مدفوعة جزئياً')),
        ('overdue', _('متأخرة')),
        ('cancelled', _('ملغاة')),
    ]

    # معلومات أساسية - Basic Information
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم الفاتورة')
    )

    invoice_type = models.CharField(
        max_length=20,
        choices=INVOICE_TYPE_CHOICES,
        verbose_name=_('نوع الفاتورة')
    )

    # العميل/المستأجر - Customer/Tenant
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name=_('المستأجر')
    )

    # التواريخ - Dates
    issue_date = models.DateField(
        verbose_name=_('تاريخ الإصدار')
    )

    due_date = models.DateField(
        verbose_name=_('تاريخ الاستحقاق')
    )

    # المبالغ - Amounts (Always in USD)
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('المجموع الفرعي'),
        help_text='USD'
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('نسبة الضريبة'),
        help_text='%'
    )

    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('مبلغ الضريبة'),
        help_text='USD'
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('مبلغ الخصم'),
        help_text='USD'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('المبلغ الإجمالي'),
        help_text='USD'
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('المبلغ المدفوع'),
        help_text='USD'
    )

    # الحالة - Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('الحالة')
    )

    # ملاحظات - Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ملاحظات')
    )

    # التتبع - Tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_invoices',
        verbose_name=_('أنشئ بواسطة')
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
        verbose_name = _('فاتورة')
        verbose_name_plural = _('الفواتير')
        db_table = 'finance_invoice'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.invoice_number} - {self.tenant.get_full_name()}"

    @property
    def balance_due(self):
        """المبلغ المتبقي"""
        return self.total_amount - self.paid_amount

    def calculate_totals(self):
        """حساب المجاميع من عناصر الفاتورة - Calculate totals from invoice items"""
        items = self.items.all()
        self.subtotal = sum(item.total for item in items)
        self.tax_amount = (self.subtotal * self.tax_rate) / 100
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.save()

    def get_total_paid(self):
        """حساب إجمالي المبالغ المدفوعة - Calculate total paid amount"""
        from django.db.models import Sum
        total = self.payments.aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')

    def update_payment_status(self):
        """تحديث حالة الدفع بناءً على المبالغ المدفوعة - Update payment status based on paid amounts"""
        total_paid = self.get_total_paid()

        if total_paid >= self.total_amount:
            self.status = 'paid'
            self.paid_amount = self.total_amount
        elif total_paid > 0:
            self.status = 'partially_paid'
            self.paid_amount = total_paid
        elif self.status not in ['draft', 'cancelled']:
            self.status = 'pending'
            self.paid_amount = Decimal('0.00')

        self.save()

    def save(self, *args, **kwargs):
        # توليد رقم الفاتورة تلقائياً
        if not self.invoice_number:
            self.invoice_number = generate_code(Invoice, 'invoice_number', 'INV', 3)

        # حساب المبلغ الإجمالي تلقائياً إذا لم يكن هناك عناصر
        if not self.pk:  # فقط عند الإنشاء
            self.tax_amount = (self.subtotal * self.tax_rate) / 100
            self.total_amount = self.subtotal + self.tax_amount - self.discount_amount

        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    """
    بند الفاتورة - Invoice Item
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('الفاتورة')
    )

    description = models.CharField(
        max_length=200,
        verbose_name=_('الوصف')
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('الكمية')
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('سعر الوحدة'),
        help_text='USD'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('المجموع'),
        help_text='USD'
    )

    class Meta:
        verbose_name = _('بند الفاتورة')
        verbose_name_plural = _('بنود الفاتورة')
        db_table = 'finance_invoiceitem'

    def __str__(self):
        return f"{self.description} - {self.total} USD"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    دفعة - Payment
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', _('نقداً')),
        ('credit_card', _('بطاقة ائتمان')),
        ('debit_card', _('بطاقة خصم')),
        ('bank_transfer', _('تحويل بنكي')),
        ('cheque', _('شيك')),
        ('online', _('دفع إلكتروني')),
    ]

    # معلومات أساسية - Basic Information
    payment_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم الدفعة')
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('الفاتورة')
    )

    # المبلغ - Amount (Always in USD)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('المبلغ'),
        help_text='USD'
    )

    # طريقة الدفع - Payment Method
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name=_('طريقة الدفع')
    )

    # التاريخ - Date
    payment_date = models.DateField(
        verbose_name=_('تاريخ الدفع')
    )

    # مرجع - Reference
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('رقم المرجع')
    )

    # ملاحظات - Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ملاحظات')
    )

    # التتبع - Tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_payments',
        verbose_name=_('أنشئ بواسطة')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    def save(self, *args, **kwargs):
        """Override save to auto-generate payment_number and update invoice status"""
        if not self.payment_number:
            self.payment_number = generate_code(Payment, 'payment_number', 'PAY', 3)
        super().save(*args, **kwargs)

        # تحديث حالة الفاتورة بعد حفظ الدفعة
        # Update invoice status after saving payment
        if self.invoice:
            self.invoice.update_payment_status()

    def delete(self, *args, **kwargs):
        """Override delete to update invoice status after deletion"""
        invoice = self.invoice
        super().delete(*args, **kwargs)

        # تحديث حالة الفاتورة بعد حذف الدفعة
        # Update invoice status after deleting payment
        if invoice:
            invoice.update_payment_status()

    class Meta:
        verbose_name = _('دفعة')
        verbose_name_plural = _('الدفعات')
        db_table = 'finance_payment'
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.payment_number} - {self.amount} USD"
