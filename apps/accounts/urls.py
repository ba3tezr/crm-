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
    path('permits/', views.tenant_permits, name='tenant_permits'),
    path('invoices/', views.tenant_invoices, name='tenant_invoices'),
    path('invoices/<int:pk>/', views.tenant_invoice_detail, name='tenant_invoice_detail'),
    path('invoices/<int:pk>/print/', views.tenant_invoice_print, name='tenant_invoice_print'),
]

