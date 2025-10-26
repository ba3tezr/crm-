from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from .models import Permit, PermitAttachment, PermitApproval

User = get_user_model()


class PermitResource(resources.ModelResource):
    """Resource class for Permit model to enable import/export"""
    
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    tenant = fields.Field(
        column_name='tenant',
        attribute='tenant',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Permit
        fields = (
            'id', 'permit_number', 'permit_type', 'direction',
            'title', 'description', 'company_name', 'contact_person',
            'contact_phone', 'requested_date', 'start_date', 'end_date',
            'notes', 'status', 'created_by', 'tenant', 'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['permit_number']
        skip_unchanged = True
        report_skipped = True


class PermitAttachmentResource(resources.ModelResource):
    """Resource class for PermitAttachment model"""
    
    permit = fields.Field(
        column_name='permit',
        attribute='permit',
        widget=ForeignKeyWidget(Permit, 'permit_number')
    )
    
    class Meta:
        model = PermitAttachment
        fields = ('id', 'permit', 'file', 'file_name', 'uploaded_at')
        export_order = fields


class PermitApprovalResource(resources.ModelResource):
    """Resource class for PermitApproval model"""
    
    permit = fields.Field(
        column_name='permit',
        attribute='permit',
        widget=ForeignKeyWidget(Permit, 'permit_number')
    )
    
    approved_by = fields.Field(
        column_name='approved_by',
        attribute='approved_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = PermitApproval
        fields = ('id', 'permit', 'approved_by', 'action', 'comments', 'created_at')
        export_order = fields

