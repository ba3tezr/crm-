from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from .models import Ticket, TicketAttachment, TicketComment

User = get_user_model()


class TicketResource(resources.ModelResource):
    """Resource class for Ticket model to enable import/export"""
    
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
        model = Ticket
        fields = (
            'id', 'ticket_number', 'title', 'description', 'category',
            'priority', 'status', 'created_by', 'assigned_to',
            'unit_number', 'floor_number', 'building_name',
            'due_date', 'resolved_at', 'resolution_notes',
            'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['ticket_number']
        skip_unchanged = True
        report_skipped = True


class TicketAttachmentResource(resources.ModelResource):
    """Resource class for TicketAttachment model"""
    
    ticket = fields.Field(
        column_name='ticket',
        attribute='ticket',
        widget=ForeignKeyWidget(Ticket, 'ticket_number')
    )
    
    class Meta:
        model = TicketAttachment
        fields = ('id', 'ticket', 'file', 'file_name', 'uploaded_at')
        export_order = fields


class TicketCommentResource(resources.ModelResource):
    """Resource class for TicketComment model"""
    
    ticket = fields.Field(
        column_name='ticket',
        attribute='ticket',
        widget=ForeignKeyWidget(Ticket, 'ticket_number')
    )
    
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = TicketComment
        fields = ('id', 'ticket', 'comment', 'created_by', 'created_at')
        export_order = fields

