from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import FormActions

from .models import Case, CaseAttachment, CaseComment


class CaseForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل القضية - Case Form
    """
    
    class Meta:
        model = Case
        fields = [
            'case_number',
            'case_type',
            'title',
            'description',
            'priority',
            'status',
            'assigned_to',
            'department',
            'resolution_notes',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'resolution_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # استخراج معامل is_tenant لتحديد نوع النموذج
        is_tenant = kwargs.pop('is_tenant', False)
        super().__init__(*args, **kwargs)

        # إذا كان المستخدم مستأجر، نخفي ونثبت بعض الحقول
        if is_tenant:
            # إخفاء الحقول غير المطلوبة للمستأجر
            self.fields.pop('case_number', None)
            self.fields.pop('status', None)
            self.fields.pop('assigned_to', None)
            self.fields.pop('department', None)
            self.fields.pop('resolution_notes', None)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'

        # Make case_number readonly if editing (for staff only)
        if not is_tenant and self.instance.pk:
            self.fields['case_number'].widget.attrs['readonly'] = True

        # Different layouts for tenant vs staff
        if is_tenant:
            # Simplified layout for tenants
            self.helper.layout = Layout(
                Row(
                    Column('title', css_class='form-group col-md-12 mb-3'),
                ),
                Row(
                    Column('case_type', css_class='form-group col-md-6 mb-3'),
                    Column('priority', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('description', css_class='form-group col-md-12 mb-3'),
                ),
                FormActions(
                    Submit('submit', _('إرسال الشكوى'), css_class='btn btn-primary btn-lg'),
                    css_class='text-end mt-3'
                )
            )
        else:
            # Full layout for staff
            self.helper.layout = Layout(
                Div(
                    Div(
                        Row(
                            Column('case_number', css_class='form-group col-md-6 mb-3'),
                            Column('case_type', css_class='form-group col-md-6 mb-3'),
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
                            Column('assigned_to', css_class='form-group col-md-6 mb-3'),
                            Column('department', css_class='form-group col-md-6 mb-3'),
                        ),
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
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


class CaseAttachmentForm(forms.ModelForm):
    """
    نموذج رفع مرفق القضية - Case Attachment Form
    """
    
    class Meta:
        model = CaseAttachment
        fields = ['file', 'file_name']
        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
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


class CaseCommentForm(forms.ModelForm):
    """
    نموذج إضافة تعليق على القضية - Case Comment Form
    """
    
    class Meta:
        model = CaseComment
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

