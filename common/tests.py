
#Create some fake data
__test__ = {"doctest":"""

>>> from django.contrib.auth.models import User
>>> from django.contrib.auth import authenticate, login, logout
>>> from rideShare.myRides.models import *
>>> from rideShare.geo.models import *
>>> from rideShare.common.views import generateUniversityJson


#Create a fake school and email
>>> Pos = Position(latitude=0.0, longitude=0.0)
>>> Pos.save()
>>> zip = ZipCode(zip='06085', stateAbbrev='CT', stateName='Conneticut',globalPos=Pos)
>>> zip.save()
>>> studentEmail = StudentEmail(email='@gmail.com')
>>> studentEmail.save()
>>> DrosdeckU = University(name='Drosdeck U', address='42 high street', zip = zip, latLng= Pos)
>>> DrosdeckU.save()

#Create the car objects
>>> car = Car(seats=1)
>>> car.save()


>>> DrosdeckU.email.add(studentEmail)
>>> DrosdeckU.save()


>>> user1_email = 'jdrosdeck@gmail.com'
>>> user1_password = 'hoppy'
>>> user1_domain = user1_email[user1_email.find('@'):]
>>> user1_domain == '@gmail.com'
True

>>> emailDomain,created = StudentEmail.objects.get_or_create(email__iexact=user1_domain)
>>> created
False

>>> emailDomain.email
u'@gmail.com'

>>> user1 = User(username=user1_email, password=user1_password, is_staff=False)
>>> user1.save()
>>> user1 = Users(user=user1, university=DrosdeckU)
>>> user1.save()

#Do a quick sampling of data to make sure it's consistant
>>> user1.user
<User: jdrosdeck@gmail.com>
>>> user1.university
<University: Drosdeck U>
>>> user1.university.name
'Drosdeck U'
>>> user1.university.address
'42 high street'

>>> user2_email = 'what@gmail.com'
>>> user2_password = 'testPass'
>>> user2 = User(username=user2_email, password=user2_password, is_staff=False)
>>> user2.save()
>>> user2 = Users(user=user2, university=DrosdeckU)
>>> user2.save()



#Test out the genearateUniversityJson function for proper json encoding
>>> jsonUser = 'json@southwestern.edu'
>>> jsonEmail = StudentEmail(email='@southwestern.edu')
>>> jsonEmail.save()
>>> school1 = University(name='SouthWestern1', address='42 high street', zip = zip, latLng= Pos) 
>>> school1.save()
>>> school2 = University(name='SouthWestern2', address='45 high street', zip = zip, latLng= Pos) 
>>> school2.save()
>>> school1.email.add(jsonEmail)
>>> school1.save()
>>> school2.email.add(jsonEmail)
>>> school2.save()

>>> multipleEmails = StudentEmail.objects.get(email__iexact='@southwestern.edu')
>>> multipleSchools = University.objects.filter(email__id__exact = multipleEmails.id)
>>> multipleSchools.count()
2

>>> generateUniversityJson(multipleSchools.values())
'{"results": [{"zip_id": 1, "latLng_id": 1, "address": "42 high street", "id": 2, "name": "SouthWestern1"}, {"zip_id": 1, "latLng_id": 1, "address": "45 high street", "id": 3, "name": "SouthWestern2"}]}'


"""
}

