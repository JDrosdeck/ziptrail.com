from django.conf.urls.defaults import *

urlpatterns = patterns('rideShare.common.views',
                       (r'register/$', 'register'),
                       (r'login/$', 'login_View'),
                       (r'logout/$', 'logout_View'),
                       ('checkEmail/$', 'isEmailDomainValid'),
                       )
