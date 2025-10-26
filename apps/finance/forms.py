"""
Finance Forms
"""
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button
from .models import Invoice, InvoiceItem, Payment


class InvoiceForm(forms.ModelForm):
    """نموذج الفاتورة - Invoice Form"""
    
    class Meta:
        model = Invoice
        fields = [
            'tenant', 'invoice_type', 'issue_date', 'due_date',
            'subtotal', 'tax_rate', 'discount_amount', 'notes'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('tenant', css_class='col-md-6'),
                Column('invoice_type', css_class='col-md-6'),
            ),
            Row(
                Column('issue_date', css_class='col-md-6'),
                Column('due_date', css_class='col-md-6'),
            ),
            Row(
                Column('subtotal', css_class='col-md-4'),
                Column('tax_rate', css_class='col-md-4'),
                Column('discount_amount', css_class='col-md-4'),
            ),
            'notes',
            Row(
                Column(Submit('submit', _('حفظ'), css_class='btn btn-primary'), css_class='col-md-6'),
                Column(Button('cancel', _('إلغاء'), css_class='btn btn-secondary', onclick='history.back()'), css_class='col-md-6'),
            ),
        )


class InvoiceItemForm(forms.ModelForm):
    """نموذج عنصر الفاتورة - Invoice Item Form"""

    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': _('الوصف')}),
            'quantity': forms.NumberInput(attrs={'placeholder': _('الكمية'), 'min': '1', 'step': '1'}),
            'unit_price': forms.NumberInput(attrs={'placeholder': _('السعر'), 'min': '0', 'step': '0.01'}),
        }


# InvoiceItem Inline Formset
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=3,  # عدد النماذج الفارغة
    can_delete=True,
    min_num=1,  # الحد الأدنى
    validate_min=True,
)


class PaymentForm(forms.ModelForm):
    """نموذج الدفعة - Payment Form"""
    
    class Meta:
        model = Payment
        fields = [
            'invoice', 'amount', 'payment_method', 'payment_date',
            'reference_number', 'notes'
        ]
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('invoice', css_class='col-md-6'),
                Column('amount', css_class='col-md-6'),
            ),
            Row(
                Column('payment_method', css_class='col-md-6'),
                Column('payment_date', css_class='col-md-6'),
            ),
            'reference_number',
            'notes',
            Row(
                Column(Submit('submit', _('حفظ'), css_class='btn btn-primary'), css_class='col-md-6'),
                Column(Button('cancel', _('إلغاء'), css_class='btn btn-secondary', onclick='history.back()'), css_class='col-md-6'),
            ),
        )

