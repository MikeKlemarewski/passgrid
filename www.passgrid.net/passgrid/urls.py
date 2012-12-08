from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("passgrid.views",
    url(r'^$', "home"),
    url(r'^mobile/$', "mobile"),

    url(r'^admin/', include(admin.site.urls)),
)