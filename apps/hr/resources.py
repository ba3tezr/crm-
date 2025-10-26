from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from .models import LeaveRequest, LeaveRequestApproval, Attendance, Payroll, PayrollItem

User = get_user_model()


class LeaveRequestResource(resources.ModelResource):
    """Resource class for LeaveRequest model to enable import/export"""
    
    employee = fields.Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    approved_by = fields.Field(
        column_name='approved_by',
        attribute='approved_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = LeaveRequest
        fields = (
            'id', 'request_number', 'employee', 'leave_type',
            'start_date', 'end_date', 'days_count', 'reason',
            'status', 'approved_by', 'approval_date', 'rejection_reason',
            'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['request_number']
        skip_unchanged = True
        report_skipped = True


class AttendanceResource(resources.ModelResource):
    """Resource class for Attendance model"""
    
    employee = fields.Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Attendance
        fields = (
            'id', 'employee', 'date', 'check_in', 'check_out',
            'status', 'notes', 'created_at', 'updated_at'
        )
        export_order = fields


class PayrollResource(resources.ModelResource):
    """Resource class for Payroll model"""
    
    employee = fields.Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Payroll
        fields = (
            'id', 'employee', 'month', 'year', 'basic_salary',
            'total_allowances', 'total_deductions', 'net_salary',
            'status', 'payment_date', 'notes',
            'created_at', 'updated_at'
        )
        export_order = fields

