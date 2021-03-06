import csv
import re
from django.http import HttpResponse
from geo.models import ZipCode, Position
from myRides.models import University

def loadZip(request):
    reader = csv.reader(open("/Users/jdrosdeck/Desktop/zip_codes.csv", "rb"), delimiter=",", quoting=csv.QUOTE_ALL)

    for row in reader:

        zip = re.sub('\"', "", row[0])
        abbrev = re.sub('\"', "", row[4])
        name = re.sub('\"', "", row[3])
        long = re.sub('\"', "", row[2])
        lat = re.sub('\"', "", row[1])
        pos = Position(latitude=lat, longitude=long)
        pos.save()
        zip = ZipCode(zip=zip, stateAbbrev=abbrev, stateName=name, globalPos=pos)
        zip.save()

    return HttpResponse("Load complete")
    

def loadSchool(request):
    reader = csv.reader(open("/Users/jdrosdeck/Desktop/schools.csv", "rb"), delimiter=",", quoting=csv.QUOTE_ALL)
    
    for row in reader:
        name = re.sub("\"", "", row[0])
        address = re.sub('\"',"", row[1])
        zip = re.sub("\"", "", row[2])
        
    
        #make sure the zipcode exists
        zcode = ZipCode.objects.get(zip=zip)
        #Save the student email domain
        email = re.sub('\"', '', row[3])
        
        
        tempemail2 = row[4]
        if tempemail2.startswith('@'):
            tempemail2 = re.sub('\"', '' , row[4])
                # see if the email aready exists
            try:
                pass
                #email2 = StudentEmail.objects.get(email=tempemail2)
            except:
                #email2 = StudentEmail(email=tempemail2)
                #email2.save()
                pass
                
            lat = re.sub('\"', '', row[5])
            lng = re.sub('\"', '', row[6])

        else:
            lat = re.sub('\"', '', row[4])
            lng = re.sub('\"', '', row[5])

        pos = Position(latitude=lat, longitude=lng)
        pos.save()
        newUniversity= University(name=name, address=address, email=email, zip=zcode, latLng=pos)
        newUniversity.save()
    
    return HttpResponse("Load complete")
    
