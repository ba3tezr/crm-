from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from .models import Event, Activation

User = get_user_model()


class EventResource(resources.ModelResource):
    """Resource class for Event model to enable import/export"""
    
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    responsible_person = fields.Field(
        column_name='responsible_person',
        attribute='responsible_person',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Event
        fields = (
            'id', 'event_number', 'event_type', 'title', 'description',
            'start_date', 'end_date', 'location', 'budget', 'status',
            'created_by', 'responsible_person', 'notes',
            'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['event_number']
        skip_unchanged = True
        report_skipped = True


class ActivationResource(resources.ModelResource):
    """Resource class for Activation model"""
    
    event = fields.Field(
        column_name='event',
        attribute='event',
        widget=ForeignKeyWidget(Event, 'event_number')
    )
    
    class Meta:
        model = Activation
        fields = (
            'id', 'event', 'activation_type', 'title', 'description',
            'start_date', 'end_date', 'location', 'target_audience',
            'expected_participants', 'actual_participants', 'status',
            'notes', 'created_at', 'updated_at'
        )
        export_order = fields

