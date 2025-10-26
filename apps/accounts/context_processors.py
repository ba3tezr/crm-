"""
Context Processors for Accounts App
معالجات السياق لتطبيق الحسابات
"""
from .models import DepartmentPermission


def user_permissions(request):
    """
    إضافة صلاحيات المستخدم إلى السياق
    Add user permissions to context
    """
    if not request.user.is_authenticated:
        return {
            'user_modules': [],
            'user_permissions_dict': {},
        }
    
    # Superuser has access to everything
    if request.user.is_superuser:
        return {
            'user_modules': ['permits', 'maintenance', 'complaints', 'marketing', 'hr', 'finance'],
            'user_permissions_dict': {
                'permits': ['view', 'add', 'change', 'delete', 'export', 'approve'],
                'maintenance': ['view', 'add', 'change', 'delete', 'export'],
                'complaints': ['view', 'add', 'change', 'delete', 'export'],
                'marketing': ['view', 'add', 'change', 'delete', 'export'],
                'hr': ['view', 'add', 'change', 'delete', 'export'],
                'finance': ['view', 'add', 'change', 'delete', 'export'],
            },
        }
    
    # Get user's department permissions
    permissions = DepartmentPermission.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('user')
    
    # Build modules list and permissions dict
    user_modules = []
    user_permissions_dict = {}
    
    for perm in permissions:
        user_modules.append(perm.module)
        user_permissions_dict[perm.module] = perm.permissions
    
    return {
        'user_modules': user_modules,
        'user_permissions_dict': user_permissions_dict,
    }


def has_module_permission(user, module, permission_type='view'):
    """
    التحقق من صلاحية المستخدم لمديول معين
    Check if user has permission for a specific module
    
    Args:
        user: المستخدم
        module: اسم المديول (permits, maintenance, etc.)
        permission_type: نوع الصلاحية (view, add, change, delete, export, approve)
    
    Returns:
        bool: True إذا كان لديه الصلاحية
    """
    if not user.is_authenticated:
        return False
    
    # Superuser has all permissions
    if user.is_superuser:
        return True
    
    # Check department permission
    try:
        perm = DepartmentPermission.objects.get(
            user=user,
            module=module,
            is_active=True
        )
        return perm.has_permission(permission_type)
    except DepartmentPermission.DoesNotExist:
        return False

