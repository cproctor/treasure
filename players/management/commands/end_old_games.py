from django.core.management.base import BaseCommand, CommandError
from treasure import settings
from players.models import Game
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help="Drop all games in the database"

    def add_arguments(self, parser):
        #parser.add_argument('levelset', nargs=1)
        pass

    def handle(self, *args, **options):
        age_limit = now() - timedelta(seconds=settings.GAME_MAX_AGE_SECONDS)
        print(age_limit)
        for game in Game.objects.all():
            print(game, game.created_at)

        for game in Game.objects.filter(status=Game.WAITING, created_at__lt=age_limit):
            print("NEVER STARTED...", game)
            game.status = Game.CANCELLED
            game.save()

        for game in Game.objects.filter(status=Game.PLAYING, created_at__lt=age_limit):
            print("DID NOT COMPLETE...", game)
            game.status = Game.CANCELLED
            if game.turns.first().plays.count() == 2: # Someone played but the other didn't
                players_in_last_turn = [play.player.name for play in game.turns.first().plays.all()]
                game.loser = game.players.exclude(name=players_in_last_turn).first()
            game.save()
            


