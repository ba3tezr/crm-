"""
Custom Middleware for CRM System
"""
from django.utils import translation
from django.conf import settings


class LanguageMiddleware:
    """
    Middleware to persist language selection across sessions
    يحفظ اللغة المختارة في session ويطبقها على جميع الصفحات
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from various sources (in order of priority)
        language = None

        # 1. HIGHEST PRIORITY: Check if language is being changed via POST (set_language or login)
        if request.method == 'POST' and 'language' in request.POST:
            post_language = request.POST.get('language')
            if post_language and post_language in [lang[0] for lang in settings.LANGUAGES]:
                language = post_language
                # Save language to session
                request.session['django_language'] = language

        # 2. Check if language is already set in session (from previous login or selection)
        if not language and 'django_language' in request.session:
            language = request.session['django_language']

        # 3. Check URL prefix (e.g., /en/ or /ar/) - only if no session language
        if not language:
            path = request.path_info
            for lang_code, lang_name in settings.LANGUAGES:
                if path.startswith(f'/{lang_code}/'):
                    language = lang_code
                    # Save to session for consistency
                    request.session['django_language'] = language
                    break

        # 4. LOWEST PRIORITY: Use default language from settings
        if not language:
            language = settings.LANGUAGE_CODE
            # Save default to session
            request.session['django_language'] = language

        # Activate the language
        translation.activate(language)
        request.LANGUAGE_CODE = language

        response = self.get_response(request)

        # Set language cookie
        if hasattr(response, 'set_cookie'):
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                language,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )

        return response

