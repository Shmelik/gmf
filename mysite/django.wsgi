import os, sys
sys.path.append('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler() 