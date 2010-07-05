import csv
import re
from django.http import HttpResponse
from rideShare.zip.models import ZipCode

def load(request):
    reader = csv.reader(open("/Users/jdrosdeck/Desktop/zips.txt", "rb"), delimiter=",", quoting=csv.QUOTE_NONE)

    for row in reader:
        print row
        zip = re.sub("\"", "", row[1])
        abbrev = re.sub("\"", "", row[2])
        name = re.sub("\"", "", row[3])
        long = re.sub("\"", "", row[4])
        lat = re.sub("\"", "", row[5])

        zip = ZipCode(zip=zip, stateAbbrev=abbrev, stateName=name, longitude=long, latitude=lat)
        zip.save()

    return HttpResponse("Load complete")
    
