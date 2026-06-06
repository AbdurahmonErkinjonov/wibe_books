"""
PythonAnywhere WSGI konfiguratsiya fayli.

Bu faylni PythonAnywhere dashboard'da "WSGI configuration file" maydoniga ko'rsating.
Yo'l: /home/YOUR_USERNAME/kitobdunyo/pythonanywhere_wsgi.py

MUHIM: 'YOUR_USERNAME' o'rniga o'zingizning PythonAnywhere username'ingizni kiriting!
"""

import sys
import os

# Loyiha papkasini sys.path ga qo'shamiz
# 'YOUR_USERNAME' ni o'zgartiring!
path = '/home/YOUR_USERNAME/kitobdunyo'
if path not in sys.path:
    sys.path.insert(0, path)

# Django sozlamalari
os.environ['DJANGO_SETTINGS_MODULE'] = 'bookstore.settings'
os.environ['DJANGO_DEBUG'] = 'False'

# Muhim: Production uchun SECRET_KEY ni almashtiring!
# os.environ['DJANGO_SECRET_KEY'] = 'your-very-secret-key-here'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
