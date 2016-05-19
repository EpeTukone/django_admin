import hashlib
import datetime
import random
from django.core.management.base import BaseCommand, CommandError
from adminka.models import Player, PlayerSession


class Command(BaseCommand):
    help = 'Fill up db with data'

    def add_arguments(self, parser):
        parser.add_argument('--player-count', default=5, type=int)
        parser.add_argument('--session-count-per-user', default=2, type=int)

    def _create_session(self, player_object, session_index):
        session = PlayerSession()
        session_unique_part = str(session_index) + str(datetime.datetime.now())
        session_uuid = hashlib.sha1(session_unique_part).hexdigest()
        session.player = player_object
        session.sid = session_uuid
        session.is_finished = bool(random.randint(0, 1))

        session_ttl = random.randint(10, 7200)
        session.created = datetime.datetime.now()
        session.updated = datetime.datetime.now() + datetime.timedelta(seconds=session_ttl)
        session.save()


    def _create_player(self, player_index, options):
        player = Player()
        nickname_unique_part = str(player_index) + str(datetime.datetime.now())
        nickname_unique_hash = hashlib.sha1(nickname_unique_part).hexdigest()[:10]
        player.nickname = "test_{}".format(nickname_unique_hash)
        player.email = "{}@mail.com".format(player.nickname)
        player.xp = 0
        player.created = datetime.datetime.now()
        player.updated = datetime.datetime.now()
        player.save()
        for session_index in xrange(options["session_count_per_user"]):
            self._create_session(player, session_index)

    def handle(self, *args, **options):
        for i in xrange(options["player_count"]):
            self._create_player(i, options)