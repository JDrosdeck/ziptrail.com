import urllib2
import simplejson as json


def googleGeocode(Address, Zip):
    response = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=40+hillside+ave+unionville+ct&sensor=false")
    html = response.read()
    locationJson = json.loads(html)
    if 'results' in locationJson:
        locationJson = locationJson['results']
        #The json will return a paramater named types. This can be a multitude of
        #different things, but if it returns 'political' then that means we were 
        #only able to get a general lat/lng for a state. So that means we didn't find anything
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
                        print lat
                        print lng

def mapquestGeocode(Address, Zip):
    response = urllib2.urlopen('http://www.mapquestapi.com/geocoding/v1/address?key=Dmjtd|luu72002lu,ba%3Do5-5z2lh&location=40%20hillside%20ave%2006085')
    html = response.read()
    locationJson =  json.loads(html)
    if 'results' in locationJson:
        locationJson = locationJson['results']
        if 'locations' in locationJson[0]:
            locationJson = locationJson[0]['locations']
            if 'street' in locationJson[0]:
                street = locationJson[0]['street']
                print 'street ' + street
                if street != "":
                    if 'latLng' in locationJson[0]:
                        locationJson = locationJson[0]['latLng']
                        if 'lat' in locationJson:
                            lat = locationJson['lat']
                        if 'lng' in locationJson:
                            lng = locationJson['lng']

                            print lat
                            print lng

googleGeocode(None,None)
mapquestGeocode(None,None)
