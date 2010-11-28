import urllib2
import simplejson as json

def getLatLng(Address, Zip):
    response = urllib2.urlopen('http://www.mapquestapi.com/geocoding/v1/address?key=Dmjtd|luu72002lu,ba%3Do5-5z2lh&location=40%20hillside%20ave%2006085')
    html = response.read()
    print html
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

getLatLng(None,None)
