"""
URLs for Maintenance App
"""
from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    # List
    path('', views.ticket_list, name='ticket_list'),
    
    # Detail
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    
    # Create
    path('create/', views.ticket_create, name='ticket_create'),
    
    # Update
    path('<int:pk>/update/', views.ticket_update, name='ticket_update'),

    # Delete
    path('<int:pk>/delete/', views.ticket_delete, name='ticket_delete'),

    # Export
    path('export/', views.ticket_export, name='ticket_export'),
]

