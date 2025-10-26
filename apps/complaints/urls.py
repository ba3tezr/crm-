"""
URLs for Complaints App
"""
from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # List
    path('', views.case_list, name='case_list'),
    
    # Detail
    path('<int:pk>/', views.case_detail, name='case_detail'),
    
    # Create
    path('create/', views.case_create, name='case_create'),
    
    # Update
    path('<int:pk>/update/', views.case_update, name='case_update'),

    # Delete
    path('<int:pk>/delete/', views.case_delete, name='case_delete'),

    # Export
    path('export/', views.case_export, name='case_export'),
]

