from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('technologytrackerapi.views',
    url(r'^tasks/$', 'taskViewer'),
    url(r'^addTask/$', 'addTask'),
)
