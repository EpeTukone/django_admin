import datetime
from django.core.management.base import BaseCommand, CommandError
import os
from adminka.models import Players, LogGameEvents


class Command(BaseCommand):
    help = 'Rename players, for run please insert: python manage.py players_rename <file_name.txt>' \
           'file_name.txt must have two columns and format: <player_email>,<new_nickname>'

    def add_arguments(self, parser):
        parser.add_argument('--file', dest='filename', default=False, type=str)

    def _log_game_generation(self, player, old_name, new_name):
        log = LogGameEvents()
        log.player = player
        log.event_type = 9
        log.event_data = {"old_name": old_name, "new_name": new_name}
        log.created = datetime.datetime.now()
        log.save()

    def _rename_players(self, email, nickname):
        player = Players.objects.get(email=email)
        old_name = player.nickname
        player.nickname = nickname
        player.updated = datetime.datetime.now()
        player.save()
        print "Player `{}` was successfully renamed from `{}` to `{}`".format(email, old_name, nickname)
        self._log_game_generation(player, old_name, nickname)

    def handle(self, *args, **options):
        if len(args) != 0 or len(options) == 0:
            print ("Rename players, for run please insert: python manage.py players_rename <file_name.txt>' \
           'file_name.txt must have two columns and format: <player_email>,<new_nickname>")
#        if len(options['filename']) == 0:
 #           print ("Rename players, for run please insert: python manage.py players_rename <file_name.txt>' \
  #         'file_name.txt must have two columns and format: <player_email>,<new_nickname>")
        elif not os.path.isfile(options['filename']):
            print ("File does not exist at the specified path.")
        else:
            _file = (open(options['filename'], 'r')).readlines()
            for i in xrange(len(_file)):
                string = _file[i].split(',')
                email = string[0]
                nickname = string[1]
                self._rename_players(email, nickname)




# if options['filename'] == None :
#     raise CommandError("Option `--file=...` must be specified.")
#
#
# if not os.path.isfile(options['filename']) :
#     raise CommandError("File does not exist at the specified path.")



