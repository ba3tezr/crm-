"""
Custom Allauth Adapters
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to save language preference on login
    """
    def login(self, request, user):
        """
        Save selected language to session on login
        """
        # Check if language was selected in login form
        if 'language' in request.POST:
            language = request.POST.get('language')
            if language and language in [lang[0] for lang in settings.LANGUAGES]:
                request.session['django_language'] = language
        
        # Call parent login method
        return super().login(request, user)

