"""
Middleware to allow any Vercel host (Host header can omit .vercel.app).
Must run first so the host is allowed before CommonMiddleware checks it.
"""
import os


class VercelHostMiddleware:
    """When on Vercel, add the request Host to ALLOWED_HOSTS before any host check."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if os.environ.get('VERCEL') == '1':
                raw = request.META.get('HTTP_HOST', '')
                host = raw.split(':')[0].strip()
                if host:
                    from django.conf import settings
                    if host not in settings.ALLOWED_HOSTS:
                        settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + [host]
        except Exception:
            pass
        return self.get_response(request)
