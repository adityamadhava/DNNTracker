"""
WSGI config for dnn_tracker project.
Used by Gunicorn and Vercel serverless.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnn_tracker.settings')
application = get_wsgi_application()
