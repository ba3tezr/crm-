"""
URLs for Accounts App
مسارات تطبيق الحسابات
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Tenant URLs
    path('dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('profile/', views.tenant_profile, name='tenant_profile'),

    # Permits
    path('permits/', views.tenant_permits, name='tenant_permits'),
    path('permits/create/', views.tenant_permit_create, name='tenant_permit_create'),
    path('permits/<int:pk>/', views.tenant_permit_detail, name='tenant_permit_detail'),
    path('permits/<int:pk>/delete/', views.tenant_permit_delete, name='tenant_permit_delete'),

    # Maintenance Tickets
    path('tickets/', views.tenant_tickets, name='tenant_tickets'),
    path('tickets/create/', views.tenant_ticket_create, name='tenant_ticket_create'),
    path('tickets/<int:pk>/', views.tenant_ticket_detail, name='tenant_ticket_detail'),

    # Cases/Complaints
    path('cases/', views.tenant_cases, name='tenant_cases'),
    path('cases/create/', views.tenant_case_create, name='tenant_case_create'),
    path('cases/<int:pk>/', views.tenant_case_detail, name='tenant_case_detail'),

    # Invoices
    path('invoices/', views.tenant_invoices, name='tenant_invoices'),
    path('invoices/<int:pk>/', views.tenant_invoice_detail, name='tenant_invoice_detail'),
    path('invoices/<int:pk>/print/', views.tenant_invoice_print, name='tenant_invoice_print'),
]

