from django.contrib.auth.models import User
from myRides.models import Users, Trip

# checkForBadges will run though and find if there are any new badges to assign
# to a user
def getBadges(request):

    # Name              #Description
    #---------------------------------------------------
    # 1st Timer         Hosts first ride
    # Taxi              Host a ride with more then 3 passengers
    # Back seater       First time passenger
    # Ride bum          Be a passenger in over 50 rides
    # Journier          Host a ride whose distance is over 300 miles
    # 


    badges = []
    user = User.objects.get(username=request.session['username'])
    user = Users.objects.get(user=user)

    #See how many rides the user has hosted
    hostedRides = Trip.objects.filter(host=user, active=False).count()


    badges.append('high flipper')
    badges.append('ride KING!')

    if hostedRides > 1:
        badges.append('1st Timer')
    if hostedRides > 5:
        badges.append('Amateur Hour')
    if hostedRides > 15:
        badges.append('Taxi Driver')
    if hostedRides > 25:
        badges.append('Chauffeur')
    if hostedRides > 50:
        badges.append('Transporter')


    #See how many Rides the user has been a passenger in
    participatedRides = Trip.objects.filter(acceptedPassengers__user__id__exact=user.id, active=False).count()
    
    if participatedRides > 1:
        badges.append('Moocher')
    if participatedRides > 5:
        badges.append('Backseat Driver')
    if participatedRides > 15:
        badges.append('Ride Bum')
    if participatedRides > 25:
        badges.append('Wagon Train')

    return badges
