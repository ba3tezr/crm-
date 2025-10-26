"""
Custom Decorators for Access Control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _


def staff_required(view_func):
    """
    Decorator to restrict access to staff only (not tenants)
    المستأجرين لا يمكنهم الوصول - فقط الموظفين
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('account_login')
        
        # Check if user is a tenant
        if hasattr(request.user, 'tenant_profile'):
            messages.error(request, _('ليس لديك صلاحية الوصول لهذه الصفحة'))
            return redirect('accounts:tenant_dashboard')
        
        # User is staff, allow access
        return view_func(request, *args, **kwargs)
    
    return wrapper


def tenant_or_staff_required(view_func):
    """
    Decorator to allow access to both tenants and staff
    but restrict data based on user type
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('account_login')
        
        # Allow access to both tenants and staff
        return view_func(request, *args, **kwargs)
    
    return wrapper

