from django.db import models
from random import randint, choice
from django.db.models import Count

class Player(models.Model):
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True)

    @classmethod
    def generate_pid(cls):
        while True:
            id = int("".join(str(randint(1, 6)) for _ in range(5)))
            if cls.objects.filter(pid=id).count() == 0:
                return id

    @classmethod
    def treasure_player(cls):
        "returns the treasure player"
        return cls.objects.get(name='treasure')

    def __str__(self):
        return "{} ({})".format(self.name, self.pid)


    def to_json(self, full=False):
        if not full:
            return {
                'pid': self.pid, 
                'name': self.name
            }
        else:
            return {
                'pid': self.pid, 
                'name': self.name,
                'games_waiting': [g.gid for g in self.games.filter(status=Game.WAITING).all()],
                'games_playing': [g.gid for g in self.games.filter(status=Game.PLAYING).all()],
                'games_complete': [g.gid for g in self.games.filter(status=Game.COMPLETE).all()],
                'stats': {
                    'wins': self.games_won.count(),
                    'losses': self.games_lost.count(),
                    'incomplete': self.games.filter(status=Game.PLAYING).count()
                }
            }

class Game(models.Model):
    CARDS = range(1, 14)
    WAITING = 0
    PLAYING = 1
    COMPLETE = 2
    STATUS = (
        (WAITING, "waiting for players"),
        (PLAYING, "playing"), 
        (COMPLETE, "complete")
    )
    gid = models.IntegerField(unique=True)
    status = models.IntegerField(choices=STATUS)
    winner = models.ForeignKey(Player, blank=True, null=True, related_name="games_won", on_delete=models.SET_NULL)
    loser = models.ForeignKey(Player, blank=True, null=True, related_name="games_lost", on_delete=models.SET_NULL)
    players = models.ManyToManyField(Player, related_name="games")

    @classmethod
    def generate_gid(cls):
        while True:
            id = int("".join(str(randint(1, 6)) for _ in range(6)))
            if cls.objects.filter(gid=id).count() == 0:
                return id

    def __str__(self):
        return "Game {} turns:{} status:{} players:{}".format(self.gid, self.turns.count(), 
                self.get_status_display(), ", ".join(str(p) for p in self.players.all()))

    def to_json(self, mask_for_player=None):
        return {
            'gid': self.gid,
            'status': self.get_status_display(),
            'players': [{
                'name': p.name, 
                'hand': self.hand(p, mask_for_player=mask_for_player), 
                'score': self.score(p)
            } for p in self.players.exclude(name='treasure')],
            'turns': [t.to_json(mask_for_player=mask_for_player) for t in self.turns.all()]
        }

    def add_turn(self):
        "Adds another turn to the game"
        turn = self.turns.create(index=self.next_turn_index())
        t = Player.treasure_player()
        turn.plays.create(player=t, play=choice(self.hand(t)))

    def next_turn_index(self):
        if self.turns.count() is 0:
            return 0
        else:
            return self.turns.all()[0].index + 1

    def played_cards(self, player, mask_for_player=None):
        plays = []
        if mask_for_player:
            turns = self.turns.filter(plays__player=mask_for_player)
            print(turns)
        else:
            turns = self.turns.all()
        for turn in turns:
            for play in turn.plays.all():
                if play.player == player:
                    plays.append(play.play)
        return plays
            
    def hand(self, player, mask_for_player=None):
        played = self.played_cards(player, mask_for_player=mask_for_player)
        return [card for card in Game.CARDS if card not in played]

    def is_complete(self):
        return self.turns.annotate(play_count=Count('plays')).filter(play_count=3).count() == 13

    def score(self, player):
        complete_turns = self.turns.annotate(play_count=Count('plays')).filter(play_count=3)
        return sum([t.treasure() for t in complete_turns if t.winning_play().player == player])
                
    def finalize(self):
        self.status = Game.COMPLETE
        real_players = self.players.exclude(name='treasure')
        scores = sorted([(self.score(p), p) for p in self.players.exclude(name='treasure')])
        if scores[0][0] != scores[1][0]:
            self.loser = scores[0][1]
            self.winner = scores[1][1]

class GameTurn(models.Model):
    game = models.ForeignKey(Game, related_name="turns", on_delete=models.CASCADE)
    index = models.IntegerField()

    class Meta:
        ordering = ['-index']

    def to_json(self, mask_for_player=None):
        if mask_for_player and not self.is_complete():
            return {p.player.name : p.play for p in self.plays.filter(player__in=[mask_for_player, Player.treasure_player()])}
        else:
            return {p.player.name : p.play for p in self.plays.all()}

    def is_complete(self):
        return self.plays.count() == 3

    def winning_play(self):
        if self.is_complete():
            low, high = self.plays.exclude(player=Player.treasure_player()).order_by('play').all()
            if low.play == high.play:
                return self.plays.filter(player=Player.treasure_player()).first()
            if low.play == 1 and high.play == 13:
                return low
            else: 
                return high

    def treasure(self):
        tPlay = self.plays.filter(player=Player.treasure_player())
        if tPlay.exists():
            return tPlay.all()[0].play

class GameTurnPlay(models.Model):
    turn = models.ForeignKey(GameTurn, on_delete=models.CASCADE, related_name="plays")
    player = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL)
    play = models.IntegerField()

    def __str__(self):
        return "{} played {}".format(self.player, self.play)
