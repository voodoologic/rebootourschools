from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from technologytracker.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^techtracker/', include('technologytracker.urls')),
    url(r'^techtrackerapi/', include('technologytrackerapi.urls')),
    
    (r'^$', splash),
    (r'^home/$', home),
    (r'^districtReporting/$', districtReporting),
    (r'^addDistrict/$', addDistrict),
    (r'^addSchool/$', addSchool),
    (r'^addComputer/$', addComputer),
    (r'^districts/$', districts),
    (r'^schools/$', schools),
    (r'^schooljson/(?P<school_id>\d+)/$', schooljson),
    (r'^computerjson/(?P<computer_pk>\d+)/$', computerjson),
    (r'^school/(?P<school_id>\d+)/$', schoolDetail),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
