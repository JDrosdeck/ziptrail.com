from django.http import HttpResponse
from rideShare.zip.models import ZipCode
import math

def search(request):
    zips = ZipCode.objects.filter()
    for zip in zips:
      dist =  getDistance(zips[0].longitude, zip.longitude, zips[0].latitude, zip.latitude)
      print dist

    return HttpResponse("Search finished")

def getDistance(long1, long2, lat1, lat2):

    diff_long = long2 - long1
    diff_lat = lat2 - lat1

    a = (math.sin(diff_lat / 2))**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_long / 2) ** 2
    
    c = 2 * math.asin(min(1, math.sqrt(a)))
    dist = 3956 * c
    return dist

             
