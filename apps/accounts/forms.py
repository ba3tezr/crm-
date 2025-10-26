"""
Forms for Accounts App
نماذج تطبيق الحسابات
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import DepartmentPermission


class DepartmentPermissionForm(forms.ModelForm):
    """
    نموذج صلاحيات الأقسام - Department Permission Form
    """
    
    # Module choices
    MODULE_CHOICES = [
        ('permits', _('التصاريح')),
        ('maintenance', _('الصيانة')),
        ('complaints', _('الشكاوى')),
        ('marketing', _('التسويق')),
        ('hr', _('الموارد البشرية')),
        ('finance', _('المالية')),
    ]
    
    # Permission choices
    PERMISSION_CHOICES = [
        ('view', _('عرض')),
        ('add', _('إضافة')),
        ('change', _('تعديل')),
        ('delete', _('حذف')),
        ('export', _('تصدير')),
        ('approve', _('موافقة')),
    ]
    
    module = forms.ChoiceField(
        choices=MODULE_CHOICES,
        label=_('المديول'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    permissions = forms.MultipleChoiceField(
        choices=PERMISSION_CHOICES,
        label=_('الصلاحيات'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = DepartmentPermission
        fields = ['user', 'module', 'permissions', 'is_active']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing permission, convert JSON to list
        if self.instance and self.instance.pk and self.instance.permissions:
            self.initial['permissions'] = self.instance.permissions
    
    def clean_permissions(self):
        """Convert selected permissions to list"""
        permissions = self.cleaned_data.get('permissions', [])
        return list(permissions) if permissions else []

