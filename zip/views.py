import csv
import re
from django.http import HttpResponse
from rideShare.zip.models import ZipCode
from rideShare.myRides.models import University, StudentEmail

def loadZip(request):
    reader = csv.reader(open("/Users/jdrosdeck/Desktop/zip_codes.csv", "rb"), delimiter=",", quoting=csv.QUOTE_ALL)

    for row in reader:
        print row
        zip = re.sub("\"", "", row[0])
        abbrev = re.sub("\"", "", row[4])
        name = re.sub("\"", "", row[3])
        long = re.sub("\"", "", row[2])
        lat = re.sub("\"", "", row[1])

        zip = ZipCode(zip=zip, stateAbbrev=abbrev, stateName=name, longitude=long, latitude=lat)
        zip.save()

    return HttpResponse("Load complete")
    

def loadSchool(request):
    reader = csv.reader(open("/Users/jdrosdeck/Desktop/emails.csv", "rb"), delimiter=",", quoting=csv.QUOTE_ALL)
    
    for row in reader:
        name = re.sub("\"", "", row[0])
        zip = re.sub("\"", "", row[1])
        

    
            #make sure the zipcode exists
        zcode = ZipCode.objects.get(zip=zip)
            #Save the student email domain
        tempemail1 = re.sub('\"', '', row[2])
        
        #see if the email exists already
        try:
            email1 = StudentEmail.objects.get(email=tempemail1)
            
        except:
            email1 = StudentEmail(email=tempemail1)
            email1.save()
            

        email2 = None
        try:
            
            tempemail2 = re.sub('\"', '' , row[3])
            # see if the email aready exists
            try:
                email2 = StudentEmail.objects.get(email=tempemail2)
            except:
                email2 = StudentEmail(email=tempemail2)
                email2.save()
        except:
            pass

        newUniversity= University(name=name, zip=zcode)
        newUniversity.save()
        newUniversity.email.add(email1)
        try:
            newUniversity.email.add(email2)
        except:
            pass
            
        newUniversity.save()
            
            



    return HttpResponse("Load complete")
    
