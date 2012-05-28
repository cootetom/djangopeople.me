from django.conf.urls import patterns, include, url
from django.contrib import admin

from generic.views import HomePageView, ProfileView

admin.autodiscover()

urlpatterns = patterns('',
    (r'', include("social_auth.urls")),
    (r"^messages/", include("postman.urls")),

    url(r"^$", HomePageView.as_view(), name="home"),
    url(r"^profile/$", ProfileView.as_view(), name="profile"),
    url(r"^admin/", include(admin.site.urls)),
)
