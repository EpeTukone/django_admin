from django.contrib import admin
from . import models
from models import Player, PlayerStat, PlayerSession, LogGameEvent, PlayerAchievement, Achievement


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'xp', 'created', 'updated')
    list_filter = ['created']
    search_fields = ['nickname', 'email', 'xp', 'created', 'updated']


class PlayerSessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'created')
    search_fields = ['id', 'player', 'created']


class PlayerAchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'achievement', 'created')


admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStat)
admin.site.register(PlayerSession, PlayerSessionsAdmin)
admin.site.register(PlayerAchievement, PlayerAchievementAdmin)
admin.site.register(Achievement)
admin.site.register(LogGameEvent)
