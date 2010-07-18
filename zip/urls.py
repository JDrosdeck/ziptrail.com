from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.zip.views',
                       (r'loadZip/$', 'loadZip'),
                       (r'loadSchool/$', 'loadSchool'),
)
