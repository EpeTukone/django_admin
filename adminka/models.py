from django.db import models


class LogGameEvent(models.Model):
    player = models.ForeignKey('Player', db_column='player')
    event_type = models.IntegerField()
    event_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_game_events'
        verbose_name_plural = "LogGameEvents"


class Player(models.Model):
    nickname = models.CharField(unique=True, max_length=50)
    xp = models.IntegerField()
    email = models.CharField(unique=True, max_length=200)
    password_hash = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.email)

    class Meta:
        db_table = 'player'


class PlayerAchievement(models.Model):
    player = models.ForeignKey(Player, db_column='player')
    achievement = models.ForeignKey("adminka.Achievement")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'player_achievements'
        verbose_name_plural = "Player Achievements"

    def __unicode__(self):
        return unicode(self.player)


class Achievement(models.Model):
    name = models.CharField(max_length=200)
    xp = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'achievement'

    def __unicode__(self):
        return unicode(self.name)


class PlayerSession(models.Model):
    player = models.ForeignKey(Player, db_column='player', related_name='sessions')
    sid = models.CharField(unique=True, max_length=40)
    ip_addr = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.player)

    class Meta:
        db_table = 'player_sessions'
        verbose_name_plural = "PlayerSessions"


class PlayerStat(models.Model):
    player = models.ForeignKey(Player, db_column='player')
    stat_id = models.IntegerField()
    value = models.IntegerField()

    class Meta:
        db_table = 'player_stats'
        verbose_name_plural = "PlayerStats"