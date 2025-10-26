from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/read/', views.notification_mark_read, name='notification_mark_read'),
    path('notifications/mark-all-read/', views.notification_mark_all_read, name='notification_mark_all_read'),
    path('notifications/unread/', views.notification_get_unread, name='notification_get_unread'),

    # Switch User (Development/Testing)
    path('switch-user/<int:user_id>/', views.switch_user, name='switch_user'),
    path('switch-back/', views.switch_back, name='switch_back'),
]

