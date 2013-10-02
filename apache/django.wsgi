import os, sys
sys.path.append('/home/alterab/')
sys.path.append('/home/alterab/alterab/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alterab.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
