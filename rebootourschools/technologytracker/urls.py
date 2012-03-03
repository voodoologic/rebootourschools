from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('technologytracker.views',
    url(r'^home/$', 'home'),
    url(r'^districtReporting/$', 'districtReporting'),
    url(r'^addDistrict/$', 'addDistrict'),
    url(r'^addSchool/$', 'addSchool'),
    url(r'^districts/$', 'districts'),
    url(r'^schools/$', 'schools'),
)
