from django.conf.urls.defaults import *

urlpatterns = patterns('geo.views',
                       (r'loadZip/$', 'loadZip'),
                       (r'loadSchool/$', 'loadSchool'),
)
