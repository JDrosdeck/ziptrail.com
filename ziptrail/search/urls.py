from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.search.views',
                      ('^search/$', 'search'),
)
