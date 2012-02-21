from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('technologytracker.views',
    url(r'^districtDetail/$', 'districtDetail'),
    url(r'^districtReporting/$', 'districtReporting'),
)
