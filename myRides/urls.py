from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.myRides.views',
                     (r'^home/$', 'home_View'),
                     (r'^removeRide/(?P<id>\d+)/$', 'removeFromRide'),
                    
)
