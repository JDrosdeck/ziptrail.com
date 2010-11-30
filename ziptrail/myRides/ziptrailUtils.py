from urllib2 import Request, urlopen, URLError
import simplejson as json
import random
import re

def getGeocode(Address, Zip):
    
    rand = random.randrange(0,2)
    if rand == 0:
        lat, lng, valid = googleGeocode(Address, Zip)
    else:
        lat, lng, valid = mapquestGeocode(Address,Zip)

    return (lat,lng)

#This will get the geoEncoded data through to google maps REST api.
#It will return a tuple with the Lat, Lng, and a valid Flag which 
#is set to true if the geoencoded data could be found
def googleGeocode(Address, Zip):
    lat = None
    lng = None
    valid = False
    Address = re.sub(' ', '%20', Address)
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + Address + "%20" + Zip +"&sensor=false"
    req = Request(url)
    try:
       response = urlopen(req) 
    except URLError, e:
        if hassattr(e, 'reason'):
            print e.reason
        elif hassattr(e, 'code'):
            print e.code
    else:
        html = response.read()
        locationJson = json.loads(html)
        if 'results' in locationJson:
            locationJson = locationJson['results']
            
            #The json will return a paramater named types. This can be a multitude of
            #different things, but if it returns 'political' then that means we were 
            #only able to get a general lat/lng for a state. So that means we didn't find anything
            print locationJson
            if 'types' in locationJson[0]:
                type =  locationJson[0]['types']
                if 'political' not in type:
                    if 'geometry' in locationJson[0]:
                        locationJson =  locationJson[0]['geometry']
                        if 'location' in locationJson:
                            locationJson = locationJson['location']
                            if 'lat' in locationJson:
                                lat = locationJson['lat']
                            if 'lng' in locationJson:
                                lng =  locationJson['lng']
                            if lat != None and lng !=None:
                                valid = True
    return (lat,lng, valid)

#mapquestGeocode will use the mapquest API in order to get the geocoded data.
#it will return a tuple with the lat, lng, and valid flag which is set to 
#true if the address could be geocoded.
def mapquestGeocode(Address, Zip):

    lat = None
    lng = None
    valid = False
    Address = re.sub(' ', '%20', Address)
    req = Request('http://www.mapquestapi.com/geocoding/v1/address?key=Dmjtd|luu72002lu,ba%3Do5-5z2lh&location=' + Address + '%20'+ Zip)
    try:
       response = urlopen(req)
    except URLError, e:
        if hassattr(e, 'reason'):
            print e.reason
        elif hassattr(e, 'code'):
            print e.code
    else:

        html = response.read()
        locationJson = json.loads(html)
        if 'results' in locationJson:
            locationJson = locationJson['results']
            if 'locations' in locationJson[0]:
                locationJson = locationJson[0]['locations']
                if 'street' in locationJson[0]:
                    street = locationJson[0]['street']
                    if street != "":
                        if 'latLng' in locationJson[0]:
                            locationJson = locationJson[0]['latLng']
                            if 'lat' in locationJson:
                                lat = locationJson['lat']
                            if 'lng' in locationJson:
                                lng = locationJson['lng']
                            if lat != None and lng != None:
                                valid = True
    return (lat,lng,valid)
