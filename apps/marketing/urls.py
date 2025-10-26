"""
URLs for Marketing App
"""
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    # List
    path('', views.event_list, name='event_list'),
    
    # Detail
    path('<int:pk>/', views.event_detail, name='event_detail'),
    
    # Create
    path('create/', views.event_create, name='event_create'),
    
    # Update
    path('<int:pk>/update/', views.event_update, name='event_update'),
    
    # Delete
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    
    # Export
    path('export/', views.event_export, name='event_export'),

    # Tenant Events
    path('tenant/events/', views.tenant_events_list, name='tenant_events_list'),
]

