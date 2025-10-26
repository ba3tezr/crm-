from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import FormActions

from .models import Permit, PermitAttachment, PermitApproval


class PermitForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل التصريح - Permit Form
    يدعم وضعين: للموظفين (كامل) وللمستأجرين (مبسط)
    """

    class Meta:
        model = Permit
        fields = [
            'permit_number',
            'permit_type',
            'direction',
            'title',
            'description',
            'company_name',
            'contact_person',
            'contact_phone',
            'requested_date',
            'start_date',
            'end_date',
            'notes',
            'status',
        ]
        widgets = {
            'permit_type': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'requested_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # استخراج معامل is_tenant لتحديد نوع النموذج
        is_tenant = kwargs.pop('is_tenant', False)
        super().__init__(*args, **kwargs)

        # إذا كان المستخدم مستأجر، نخفي ونثبت بعض الحقول
        if is_tenant:
            # إخفاء الحقول غير المطلوبة للمستأجر
            self.fields.pop('permit_number', None)
            self.fields.pop('status', None)
            self.fields.pop('requested_date', None)

            # جعل بعض الحقول اختيارية للمستأجر
            self.fields['company_name'].required = False
            self.fields['contact_person'].required = False
            self.fields['contact_phone'].required = False
        else:
            # للموظفين: جعل permit_number للقراءة فقط عند التعديل
            if self.instance.pk:
                self.fields['permit_number'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'

        # تخطيط مختلف حسب نوع المستخدم
        if is_tenant:
            # تخطيط مبسط للمستأجرين
            self.helper.layout = Layout(
                Div(
                    Div(
                        Row(
                            Column('permit_type', css_class='form-group col-md-6 mb-3'),
                            Column('direction', css_class='form-group col-md-6 mb-3'),
                        ),
                        'title',
                        'description',
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
                        Row(
                            Column('start_date', css_class='form-group col-md-6 mb-3'),
                            Column('end_date', css_class='form-group col-md-6 mb-3'),
                        ),
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
                        'company_name',
                        Row(
                            Column('contact_person', css_class='form-group col-md-6 mb-3'),
                            Column('contact_phone', css_class='form-group col-md-6 mb-3'),
                        ),
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
                        'notes',
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                FormActions(
                    Submit('submit', _('إنشاء التصريح'), css_class='btn btn-primary'),
                    css_class='text-end'
                )
            )
        else:
            # تخطيط كامل للموظفين
            self.helper.layout = Layout(
                Div(
                    Div(
                        Row(
                            Column('permit_number', css_class='form-group col-md-6 mb-3'),
                            Column('permit_type', css_class='form-group col-md-6 mb-3'),
                        ),
                        Row(
                            Column('direction', css_class='form-group col-md-6 mb-3'),
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
                        'requested_date',
                        Row(
                            Column('start_date', css_class='form-group col-md-6 mb-3'),
                            Column('end_date', css_class='form-group col-md-6 mb-3'),
                        ),
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
                        'company_name',
                        Row(
                            Column('contact_person', css_class='form-group col-md-6 mb-3'),
                            Column('contact_phone', css_class='form-group col-md-6 mb-3'),
                        ),
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                Div(
                    Div(
                        'notes',
                        css_class='card-body'
                    ),
                    css_class='card mb-3'
                ),

                FormActions(
                    Submit('submit', _('حفظ'), css_class='btn btn-primary'),
                    css_class='text-end'
                )
            )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    _('تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء')
                )

        return cleaned_data


class PermitAttachmentForm(forms.ModelForm):
    """
    نموذج رفع مرفق التصريح - Permit Attachment Form
    """
    
    class Meta:
        model = PermitAttachment
        fields = ['file', 'file_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        
        self.helper.layout = Layout(
            'file',
            'file_name',
            'description',
            FormActions(
                Submit('submit', _('رفع الملف'), css_class='btn btn-primary'),
            )
        )


class PermitApprovalForm(forms.ModelForm):
    """
    نموذج الموافقة على التصريح - Permit Approval Form
    """

    class Meta:
        model = PermitApproval
        fields = ['action', 'comments', 'redirected_to']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'action',
            'comments',
            'redirected_to',
            FormActions(
                Submit('submit', _('حفظ القرار'), css_class='btn btn-primary'),
            )
        )

