from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import FormActions

from .models import Event, Activation


class EventForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل الفعالية - Event Form
    """
    
    class Meta:
        model = Event
        fields = [
            'event_number',
            'title',
            'description',
            'event_type',
            'status',
            'start_date',
            'end_date',
            'location',
            'budget',
            'responsible_person',
            'notes',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        
        # Make event_number readonly if editing
        if self.instance.pk:
            self.fields['event_number'].widget.attrs['readonly'] = True
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Column('event_number', css_class='form-group col-md-6 mb-3'),
                        Column('event_type', css_class='form-group col-md-6 mb-3'),
                    ),
                    Row(
                        Column('status', css_class='form-group col-md-6 mb-3'),
                        Column('responsible_person', css_class='form-group col-md-6 mb-3'),
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
                        Column('start_date', css_class='form-group col-md-6 mb-3'),
                        Column('end_date', css_class='form-group col-md-6 mb-3'),
                    ),
                    Row(
                        Column('location', css_class='form-group col-md-6 mb-3'),
                        Column('budget', css_class='form-group col-md-6 mb-3'),
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


class ActivationForm(forms.ModelForm):
    """
    نموذج إنشاء/تعديل التفعيل - Activation Form
    """
    
    class Meta:
        model = Activation
        fields = [
            'activation_number',
            'event',
            'title',
            'description',
            'activation_date',
            'participants_count',
            'success_rate',
            'notes',
        ]
        widgets = {
            'activation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'participants_count': forms.NumberInput(attrs={'min': '0', 'class': 'form-control'}),
            'success_rate': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Make activation_number readonly if editing
        if self.instance.pk:
            self.fields['activation_number'].widget.attrs['readonly'] = True
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(
                        Column('activation_number', css_class='form-group col-md-6 mb-3'),
                        Column('event', css_class='form-group col-md-6 mb-3'),
                    ),
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    'title',
                    'description',
                    'activation_date',
                    css_class='card-body'
                ),
                css_class='card mb-3'
            ),
            
            Div(
                Div(
                    Row(
                        Column('participants_count', css_class='form-group col-md-6 mb-3'),
                        Column('success_rate', css_class='form-group col-md-6 mb-3'),
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

