"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from apps.core.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching
    path('', RedirectView.as_view(url='/en/', permanent=False)),  # Redirect to English by default
]

# Add i18n patterns for language-specific URLs
urlpatterns += i18n_patterns(
    path('', dashboard, name='home'),
    path('accounts/', include('allauth.urls')),

    # Apps URLs
    path('dashboard/', include('apps.core.urls')),
    path('tenant/', include('apps.accounts.urls')),  # Tenant URLs
    path('permits/', include('apps.permits.urls')),
    path('maintenance/', include('apps.maintenance.urls')),
    path('complaints/', include('apps.complaints.urls')),
    path('marketing/', include('apps.marketing.urls')),
    path('hr/', include('apps.hr.urls')),
    path('finance/', include('apps.finance.urls')),  # Finance URLs
    prefix_default_language=True,  # Always add language prefix (en/ or ar/)
)

# Debug Toolbar URLs (only in DEBUG mode)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
