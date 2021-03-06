from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('adminka.urls')),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, name='logout'),
]
