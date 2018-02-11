from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.views.generic.base import View
from players.models import Player, Game, GameTurn, GameTurnPlay
from django.db import IntegrityError

class JsonErrorResponse(JsonResponse):
    "Like a regular JsonResponse, but with an error status code"
    status_code = 404

class PlayerView(View):
    "A view which automatically looks up the player"
    def get(self, request, *args, **kwargs):
        self.get_player(kwargs['player'])
        return self.handle(*args, **kwargs)

    def get_player(self, pid):
        "Looks up the player, if a valid player ID was provided."
        try:
            self.player = Player.objects.get(pid=pid)
        except Player.DoesNotExist:
            raise Http404({'error': 'Invalid player ID'})

    def handle(self, player):
        "Does the view's work. Override this in subclasses."
        return JsonResponse(self.player.to_json(full=True))

class GameView(PlayerView):
    def get(self, request, *args, **kwargs):
        self.get_player(kwargs['player'])
        self.get_game(kwargs['game'])
        return self.handle(*args, **kwargs)

    def get_game(self, gid):
        "Looks up the game, if a valid game ID was provided."
        try:
            self.game = Game.objects.get(gid=gid)
        except Game.DoesNotExist:
            raise Http404({'error': 'Invalid game ID'})

    def handle(self, player, game):
        "Does the view's work. Override this in subclasses."
        return JsonResponse(self.game.to_json(mask_for_player=self.player))

def create_player(request, player):
    "Creates a new player"
    try:
        p = Player(pid=Player.generate_pid(), name=player)
        p.save()
        return JsonResponse(p.to_json())
    except IntegrityError:
        return JsonErrorResponse({'error': 'invalid name for new player'})

class NewGameView(PlayerView):
    def handle(self, player):
        game = Game(gid=Game.generate_gid(), status=Game.WAITING)
        game.save()
        game.players.add(self.player, Player.treasure_player())
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
        return redirect('show_game', self.player.pid, game.gid) 

class JoinGameView(GameView):
    def handle(self, player, game):
        if self.game.status is not Game.WAITING or self.player in self.game.players.all():
            return JsonErrorResponse({'error': 'cannot join game'})
        self.game.players.add(self.player)
        self.game.status = Game.PLAYING
        self.game.add_turn()
        self.game.save()
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
        if turn.is_complete():
            if self.game.is_complete():
                self.game.finalize()
                self.game.save()
            else:
                self.game.add_turn()
        return redirect('show_game', self.player.pid, self.game.gid) 
    






