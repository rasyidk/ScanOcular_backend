import os
import pymysql  # import pymysql

pymysql.install_as_MySQLdb()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scanocular_backend.settings")

app = get_wsgi_application()
