from django.contrib.auth.models import User
from rideShare.myRides.models import Users, TripPassengers

# checkForBadges will run though and find if there are any new badges to assign
# to a user
def checkForBadges:
    # Name              #Description
    #---------------------------------------------------
    # 1st Timer         Hosts first ride
    # Taxi              Host a ride with more then 3 passengers
    # Back seater       First time passenger
    # Ride bum          Be a passenger in over 50 rides
    # Journier          Host a ride whose distance is over 300 miles
    # 


    user = User.objects.get(username=request.session['username'])
    
    #See how many rides the person has been on as a passenger
    
