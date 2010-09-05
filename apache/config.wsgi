import os
import sys

sys.path.append('/home/twosprout/public_html/rideshare.com')
sys.path.append('/home/twosprout/public_html/rideshare.com/rideShare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rideShare.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/twosprout/.python-eggs'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

