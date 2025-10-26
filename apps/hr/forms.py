from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import FormActions

from .models import LeaveRequest, Attendance


class LeaveRequestForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل طلب الإجازة - Leave Request Form
    """
    
    class Meta:
        model = LeaveRequest
        fields = [
            'request_number',
            'employee',
            'leave_type',
            'start_date',
            'end_date',
            'days_count',
            'reason',
            'status',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'days_count': forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        
        # Make request_number readonly if editing
        if self.instance.pk:
            self.fields['request_number'].widget.attrs['readonly'] = True
            self.fields['employee'].widget.attrs['disabled'] = True
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Column('request_number', css_class='form-group col-md-6 mb-3'),
                        Column('employee', css_class='form-group col-md-6 mb-3'),
                    ),
                    Row(
                        Column('leave_type', css_class='form-group col-md-6 mb-3'),
                        Column('status', css_class='form-group col-md-6 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    Row(
                        Column('start_date', css_class='form-group col-md-4 mb-3'),
                        Column('end_date', css_class='form-group col-md-4 mb-3'),
                        Column('days_count', css_class='form-group col-md-4 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    'reason',
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
            
            # Calculate days automatically
            days_diff = (end_date - start_date).days + 1
            cleaned_data['days_count'] = days_diff
        
        return cleaned_data


class LeaveRequestApprovalForm(forms.ModelForm):
    """
    نموذج الموافقة/الرفض على طلب الإجازة - Leave Request Approval Form
    """
    
    class Meta:
        model = LeaveRequest
        fields = ['status', 'rejection_reason']
        widgets = {
            'rejection_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Limit status choices to approved/rejected
        self.fields['status'].choices = [
            ('approved', _('موافق عليه - Approved')),
            ('rejected', _('مرفوض - Rejected')),
        ]
        
        self.helper.layout = Layout(
            'status',
            'rejection_reason',
            FormActions(
                Submit('submit', _('حفظ القرار'), css_class='btn btn-primary'),
            )
        )


class AttendanceForm(forms.ModelForm):
    """
    نموذج تسجيل الحضور - Attendance Form
    """
    
    class Meta:
        model = Attendance
        fields = [
            'employee',
            'date',
            'check_in',
            'check_out',
            'is_present',
            'is_late',
            'notes',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Column('employee', css_class='form-group col-md-6 mb-3'),
                        Column('date', css_class='form-group col-md-6 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    Row(
                        Column('check_in', css_class='form-group col-md-6 mb-3'),
                        Column('check_out', css_class='form-group col-md-6 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    Row(
                        Column('is_present', css_class='form-group col-md-6 mb-3'),
                        Column('is_late', css_class='form-group col-md-6 mb-3'),
                    ),
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

