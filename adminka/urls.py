from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='player_home')),
    url(r'^home/$', 'adminka.views.player_home', name="player_home"),
    url(r'^all/$', 'adminka.views.player_all', name="player_all"),
    url(r'^filter/$', 'adminka.views.player_filter', name="player_filter"),
    url(r'^achievement/(?P<player_id>\d+)/$', 'adminka.views.player_achievement', name="player_achievement"),
    url(r'^achievement/achievement_list/(?P<player_id>\d+)/$', 'adminka.views.player_achievement_list', name="player_achievement_list"),
    url(r'^xp/(?P<player_id>\d+)/$', 'adminka.views.change_xp', name="change_xp"),


]
