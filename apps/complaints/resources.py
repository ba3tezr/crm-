from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from .models import Case, CaseAttachment, CaseComment

User = get_user_model()


class CaseResource(resources.ModelResource):
    """Resource class for Case model to enable import/export"""
    
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    assigned_to = fields.Field(
        column_name='assigned_to',
        attribute='assigned_to',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Case
        fields = (
            'id', 'case_number', 'case_type', 'title', 'description',
            'priority', 'status', 'department', 'created_by', 'assigned_to',
            'resolution_notes', 'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['case_number']
        skip_unchanged = True
        report_skipped = True


class CaseAttachmentResource(resources.ModelResource):
    """Resource class for CaseAttachment model"""
    
    case = fields.Field(
        column_name='case',
        attribute='case',
        widget=ForeignKeyWidget(Case, 'case_number')
    )
    
    class Meta:
        model = CaseAttachment
        fields = ('id', 'case', 'file', 'file_name', 'uploaded_at')
        export_order = fields


class CaseCommentResource(resources.ModelResource):
    """Resource class for CaseComment model"""
    
    case = fields.Field(
        column_name='case',
        attribute='case',
        widget=ForeignKeyWidget(Case, 'case_number')
    )
    
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = CaseComment
        fields = ('id', 'case', 'comment', 'created_by', 'created_at')
        export_order = fields

