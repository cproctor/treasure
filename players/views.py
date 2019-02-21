from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.views.generic.base import View
from players.models import Player, Game, GameTurn, GameTurnPlay
from django.db import IntegrityError
from players.bots import strategies
from treasure import settings
import logging

log = logging.getLogger(__name__)

class JsonErrorResponse(JsonResponse):
    "Like a regular JsonResponse, but with an error status code"
    status_code = 404

class PlayerView(View):
    "A view which automatically looks up the player"
    def get(self, request, *args, **kwargs):
        try: 
            self.player = Player.objects.exclude(pid=0).get(pid=kwargs['player'])
            return self.handle(*args, **kwargs)
        except Player.DoesNotExist:
            return JsonErrorResponse({'error': 'invalid player id'})

    def handle(self, player):
        "Does the view's work. Override this in subclasses."
        return JsonResponse(self.player.to_json(full=True))

class GameView(View):
    def get(self, request, *args, **kwargs):
        try:
            self.player = Player.objects.exclude(pid=0).get(pid=kwargs['player'])
            self.game = Game.objects.get(gid=kwargs['game'])
            return self.handle(*args, **kwargs)
        except Player.DoesNotExist:
            return JsonErrorResponse({'error': 'invalid player id'})
        except Game.DoesNotExist:
            return JsonErrorResponse({'error': 'invalid game id'})

    def handle(self, player, game):
        "Does the view's work. Override this in subclasses."
        if self.game.status == Game.PLAYING:
            return JsonResponse(self.game.to_json(mask_for_player=self.player))
        else:
            return JsonResponse(self.game.to_json())

def create_player(request, player):
    "Creates a new player"
    try:
        p = Player(pid=Player.generate_pid(), name=player)
        p.save()
        log.info("Created player {}".format(p))
        return JsonResponse(p.to_json())
    except IntegrityError:
        return JsonErrorResponse({'error': 'invalid name for new player'})

class NewGameView(PlayerView):
    def handle(self, player):
        game = Game(gid=Game.generate_gid(), status=Game.WAITING)
        game.save()
        game.players.add(self.player, Player.treasure_player())
        log.info("{} created new game {}".format(player, game))
        return redirect('show_game', self.player.pid, game.gid)

class JoinAnyGameView(PlayerView):
    "Selects a game waiting for players and joins it"
    def handle(self, player):
        if not Game.objects.exclude(players=self.player).filter(status=Game.WAITING).exists():
            return JsonErrorResponse({'error': 'no open games'})
        game = Game.objects.exclude(players=self.player).filter(status=Game.WAITING).first()
        game.players.add(self.player)
        game.status = Game.PLAYING
        game.add_turn()
        game.save()
        log.info("{} requested to join any game and was assigned to {}".format(player, game))
        return redirect('show_game', self.player.pid, game.gid) 

class ResumeGameView(PlayerView):
    "Resumes an active game"
    def handle(self, player):
        if not Game.objects.filter(status=Game.PLAYING, players=self.player).exists():
            return JsonErrorResponse({'error': 'no game to resume'})
        game = Game.objects.filter(status=Game.PLAYING, players=self.player).first()
        log.info("{} resumed {}".format(player, game))
        return redirect('show_game', self.player.pid, game.gid)

class JoinGameView(GameView):
    def handle(self, player, game):
        if self.game.status is not Game.WAITING or self.player in self.game.players.all():
            return JsonErrorResponse({'error': 'cannot join game'})
        self.game.players.add(self.player)
        self.game.status = Game.PLAYING
        self.game.add_turn()
        self.game.save()
        log.info("{} joined {}".format(player, self.game))
        return redirect('show_game', self.player.pid, self.game.gid)

class PlayMoveView(GameView):
    def handle(self, player, game, play):
        if self.game.status is Game.WAITING:
            return JsonErrorResponse({'error': 'game has not started'})
        if self.game.status is Game.COMPLETE:
            return JsonErrorResponse({'error': 'game has ended'})
        if self.player not in self.game.players.all():
            return JsonErrorResponse({'error': 'player is not in game'})
        if self.game.status is Game.STATUS[2]: 
            return JsonErrorResponse({'error': 'game is over'})
        if play not in self.game.hand(self.player):
            return JsonErrorResponse({'error': 'illegal play'})

        turn = self.game.turns.all()[0]
        if turn.plays.filter(player=self.player).exists():
            return JsonErrorResponse({'error': 'already played this turn'})

        turn.plays.create(player=self.player, play=play)

        if self.game.autoplay:
            bot = Player.bot_player()
            strategy = strategies[settings.BOT_STRATEGY]
            turn.plays.create(player=bot, play=strategy(self.game.to_json(mask_for_player=bot)))

        if turn.is_complete():
            if self.game.is_complete():
                self.game.finalize()
                self.game.save()
            else:
                self.game.add_turn()

        log.info("{} played {} in {}".format(player, play, self.game))

        return redirect('show_game', self.player.pid, self.game.gid) 

class SetAutoPlayView(GameView):
    def handle(self, player, game):
        if self.game.status == Game.WAITING:
            self.game.autoplay = True
            self.game.players.add(Player.bot_player())
            self.game.status = Game.PLAYING
            self.game.add_turn()
            self.game.save()
            log.info("{} set {} to autoplay".format(player, self.game))
            return redirect('show_game', self.player.pid, self.game.gid) 
        else:
            return JsonErrorResponse({'error': 'game already started'})
        
    






