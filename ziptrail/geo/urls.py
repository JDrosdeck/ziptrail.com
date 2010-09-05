from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.geo.views',
                       (r'loadZip/$', 'loadZip'),
                       (r'loadSchool/$', 'loadSchool'),
)
