"""
URLs for HR App
"""
from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # List
    path('', views.leave_request_list, name='leave_request_list'),
    
    # Detail
    path('<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    
    # Create
    path('create/', views.leave_request_create, name='leave_request_create'),

    # Update
    path('<int:pk>/update/', views.leave_request_update, name='leave_request_update'),

    # Delete
    path('<int:pk>/delete/', views.leave_request_delete, name='leave_request_delete'),

    # Approve
    path('<int:pk>/approve/', views.leave_request_approve, name='leave_request_approve'),

    # Reject
    path('<int:pk>/reject/', views.leave_request_reject, name='leave_request_reject'),
    
    # Export
    path('export/', views.leave_request_export, name='leave_request_export'),
]

