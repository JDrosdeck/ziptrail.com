from django.conf.urls.defaults import *

urlpatterns = patterns('search.views',
                      ('^search/$', 'search'),
)
