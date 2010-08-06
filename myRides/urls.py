from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.myRides.views',
                     (r'^home/$', 'home_View'),
                     (r'^view/(?P<id>\d+)/$', 'viewRide'),
                     (r'^requestPassenger/$', 'askToJoinRide'),
                     (r'^removeRider/$', 'removeRiderFromRide'),
                     ('^addRider/$', 'addPendingRiderToRide'),
                     ('^addWaypoint/$', 'CreateNewWaypoint'),
                    
)
