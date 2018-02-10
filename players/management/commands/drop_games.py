from django.core.management.base import BaseCommand, CommandError
from players.models import Game

class Command(BaseCommand):
    help="Drop all games in the database"

    def add_arguments(self, parser):
        #parser.add_argument('levelset', nargs=1)
        pass

    def handle(self, *args, **options):
        for game in Game.objects.all():
            game.delete()

