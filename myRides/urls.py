from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.myRides.views',
                     (r'^home/$', 'home_View'),
                     (r'^remove/(?P<id>\d+)/$', 'removePassengerFromRide'),
                     (r'^add/(?P<id>\d+)/$', 'addPassengerToRide'),
                    
)
