from django.conf.urls.defaults import *

urlpatterns = patterns('',
                     (r'^profiles/$', 'loadProfile'),
                     (r'^login/$', 'login'),


)
