import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Add the path to your Django project
sys.path.append("C:\\Users\\XN09542\\Documents\\Portal\\Portal\\core")

application = get_wsgi_application()
