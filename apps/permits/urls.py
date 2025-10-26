"""
URLs for Permits App
"""
from django.urls import path
from . import views

app_name = 'permits'

urlpatterns = [
    # List
    path('', views.permit_list, name='permit_list'),
    
    # Detail
    path('<int:pk>/', views.permit_detail, name='permit_detail'),
    
    # Create
    path('create/', views.permit_create, name='permit_create'),
    
    # Update
    path('<int:pk>/update/', views.permit_update, name='permit_update'),
    
    # Delete
    path('<int:pk>/delete/', views.permit_delete, name='permit_delete'),
    
    # Export
    path('export/', views.permit_export, name='permit_export'),

    # Attachments
    path('<int:pk>/upload/', views.attachment_upload, name='attachment_upload'),
    path('attachment/<int:pk>/delete/', views.attachment_delete, name='attachment_delete'),

    # Approvals
    path('<int:pk>/approve/', views.permit_approve, name='permit_approve'),
    path('my-approvals/', views.my_pending_approvals, name='my_pending_approvals'),

    # Tasks
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
]

