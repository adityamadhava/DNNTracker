"""
Vercel serverless entry: routes all requests to Django WSGI app.
Expose as `app` for Vercel Python runtime.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnn_tracker.settings')
app = get_wsgi_application()
