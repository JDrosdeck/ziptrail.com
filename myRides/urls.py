from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.myRides.views',
                     (r'^home/$', 'home_View'),
                     (r'^remove/(?P<tripId>\d+)/(?P<riderId>\d+)/$', 'removePassengerFromRide'),
                     (r'^add/(?P<tripId>\d+)/(?P<riderId>\d+)/$', 'addPassengerToRide'),
                     (r'^view/(?P<id>\d+)/$', 'viewRide'),
                     (r'^requestPassenger/$', 'askToJoinRide'),
                     (r'^removeRider/$', 'removeRiderFromRide'),
                     ('^addRider/$', 'addPendingRiderToRide'),
                    
)
