from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.zip.views',
                       (r'loadFile/$', 'load'),
)
