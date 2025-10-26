from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import FormActions

from .models import Ticket, TicketAttachment, TicketComment


class TicketForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل تذكرة الصيانة - Ticket Form
    """
    
    class Meta:
        model = Ticket
        fields = [
            'ticket_number',
            'title',
            'description',
            'category',
            'priority',
            'status',
            'assigned_to',
            'unit_number',
            'floor_number',
            'building_name',
            'due_date',
            'resolution_notes',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'resolution_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # استخراج معامل is_tenant لتحديد نوع النموذج
        is_tenant = kwargs.pop('is_tenant', False)
        super().__init__(*args, **kwargs)

        # إذا كان المستخدم مستأجر، نخفي ونثبت بعض الحقول
        if is_tenant:
            # إخفاء الحقول غير المطلوبة للمستأجر
            self.fields.pop('ticket_number', None)
            self.fields.pop('status', None)
            self.fields.pop('assigned_to', None)
            self.fields.pop('resolution_notes', None)
            self.fields.pop('due_date', None)

            # جعل بعض الحقول اختيارية للمستأجر
            self.fields['unit_number'].required = False
            self.fields['floor_number'].required = False
            self.fields['building_name'].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'

        # Make ticket_number readonly if editing (for staff only)
        if not is_tenant and self.instance.pk:
            self.fields['ticket_number'].widget.attrs['readonly'] = True
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Column('ticket_number', css_class='form-group col-md-6 mb-3'),
                        Column('category', css_class='form-group col-md-6 mb-3'),
                    ),
                    Row(
                        Column('priority', css_class='form-group col-md-6 mb-3'),
                        Column('status', css_class='form-group col-md-6 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    'title',
                    'description',
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),

            Div(
                Div(
                    Row(
                        Column('unit_number', css_class='form-group col-md-4 mb-3'),
                        Column('floor_number', css_class='form-group col-md-4 mb-3'),
                        Column('building_name', css_class='form-group col-md-4 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),

            Div(
                Div(
                    'assigned_to',
                    'due_date',
                    'resolution_notes',
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            FormActions(
                Submit('submit', _('حفظ'), css_class='btn btn-primary'),
                css_class='text-end'
            )
        )


class TicketAttachmentForm(forms.ModelForm):
    """
    نموذج رفع مرفق التذكرة - Ticket Attachment Form
    """
    
    class Meta:
        model = TicketAttachment
        fields = ['file', 'file_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        
        self.helper.layout = Layout(
            'file',
            'file_name',
            FormActions(
                Submit('submit', _('رفع الملف'), css_class='btn btn-primary'),
            )
        )


class TicketCommentForm(forms.ModelForm):
    """
    نموذج إضافة تعليق على التذكرة - Ticket Comment Form
    """
    
    class Meta:
        model = TicketComment
        fields = ['comment', 'is_internal']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': _('أضف تعليقك هنا...')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            'comment',
            'is_internal',
            FormActions(
                Submit('submit', _('إضافة تعليق'), css_class='btn btn-primary'),
            )
        )

