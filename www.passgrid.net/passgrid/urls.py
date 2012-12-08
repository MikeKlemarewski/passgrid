from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("passgrid.views",
    url(r'^$', "home"),
    url(r'^verify/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'verify', {}, 'verify'),
    url(r'^admin/', include(admin.site.urls)),
)