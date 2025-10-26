"""
Core Utilities - أدوات مساعدة
"""
from django.db.models import Max


def generate_code(model_class, field_name, prefix, length=3):
    """
    توليد رمز تلقائي - Generate automatic code
    
    Args:
        model_class: Model class (e.g., Permit, Invoice)
        field_name: Field name (e.g., 'permit_number', 'invoice_number')
        prefix: Prefix (e.g., 'PRM', 'INV')
        length: Number length (default: 3)
    
    Returns:
        str: Generated code (e.g., 'PRM-001', 'INV-042')
    
    Example:
        >>> generate_code(Permit, 'permit_number', 'PRM', 3)
        'PRM-001'
    """
    # Get the last number
    last_obj = model_class.objects.aggregate(Max(field_name))
    last_value = last_obj[f'{field_name}__max']
    
    if last_value:
        # Extract number from last code (e.g., 'PRM-042' -> 42)
        try:
            last_number = int(last_value.split('-')[-1])
            new_number = last_number + 1
        except (ValueError, IndexError):
            new_number = 1
    else:
        new_number = 1
    
    # Format with leading zeros
    formatted_number = str(new_number).zfill(length)
    
    return f"{prefix}-{formatted_number}"

