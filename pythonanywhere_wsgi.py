# PythonAnywhere WSGI configuration file
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/kisan-connect/ec'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'ec.settings'

# Load Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
