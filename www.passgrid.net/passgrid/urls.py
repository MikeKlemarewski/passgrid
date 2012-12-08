from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("passgrid.views",
    url(r'^home/$', "home"),

     # Example gmail logins.
    url(r'^$', "login"),
    url(r'^accounts/login/$', "login"),

    # Passgrid login.
    url(r'^passgrid/$', "passgrid"),
    url(r'^protected/$', "protected"),
    url(r'^mobile/$', "mobile"),
    url(r'^signup/$', "signup"),
    url(r'^verify/(?P<uidb36>[0-9A-Za-z]+)-(?P<verification_token>.+)/$', 'verify', {}, 'verify'),
    url(r'^admin/', include(admin.site.urls)),
)