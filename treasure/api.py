import requests

URLS = {
    'new_player': 'players/new/{name}',
    'show_player': 'players/{pid}',
    'new_game': 'players/{pid}/games/new',
    'join_game': 'players/{pid}/games/{gid}/join',
    'resume_game': 'players/{pid}/games/resume',
    'join_any_game': 'players/{pid}/games/join',
    'show_game': 'players/{pid}/games/{gid}',
    'set_autoplay': 'players/{pid}/games/{gid}/autoplay',
    'play_move': 'players/{pid}/games/{gid}/play/{play}'
}

class TreasureApi():
    def __init__(self, url, pid=None, name=None):
        "Initialized with either an existing pid or a name to add"
        if not url.endswith('/'):
            url = url + '/'
        self.url = url

        if (pid and name) or not (pid or name):
            raise ValueError("Must provide either a pid (for existing user) or a name (for new user)")
        if pid:
            self.get_player(pid)
        else:
            self.new_player(name)

    def __str__(self):
        if not hasattr(self, 'player'):
            return "API"
        if not hasattr(self, 'game'):
            return "API player:{} ({})".format(self.player['name'], self.player['pid'])
        return  "API player:{} ({}) game: {}".format(self.player['name'], self.player['pid'], self.game['gid'])

    def __repr__(self):
        return "<{}>".format(self)

    def get_url(self, url, **kwargs):
        return self.url + URLS[url].format(**kwargs)

    def save_player(self, response):
        if response.ok:
            self.player = response.json()
            return self.player
        else:
            self.error = response.json()

    def save_game(self, response):
        if response.ok:
            self.game = response.json()
            return self.game
        else:
            self.error = response.json()

    def new_player(self, name):
        return self.save_player(requests.get(self.get_url('new_player', 
            name=name
        )))

    def get_player(self, pid=None):
        return self.save_player(requests.get(self.get_url('show_player', 
            pid=pid or self.player['pid']
        )))

    def new_game(self, pid=None):
        return self.save_game(requests.get(self.get_url('new_game', 
            pid=pid or self.player['pid']
        )))

    def join_game(self, pid=None, gid=None):
        return self.save_game(requests.get(self.get_url('join_game', 
            pid=pid or self.player['pid'], 
            gid=gid or self.game['gid']
        )))

    def resume_game(self, pid=None):
        return self.save_game(requests.get(self.get_url('resume_game', 
            pid=pid or self.player['pid']
        )))

    def join_any_game(self, pid=None):
        return self.save_game(requests.get(self.get_url('join_any_game', 
            pid=pid or self.player['pid']
        )))

    def get_game(self, pid=None, gid=None):
        return self.save_game(requests.get(self.get_url('show_game', 
            pid=pid or self.player['pid'], 
            gid=gid or self.game['gid']
        )))

    def can_play(self):
        if not self.player and self.game:
            raise ValueError("There is no current game")
        return self.game['status'] == 'playing' and self.player['name'] not in self.game['turns'][0].keys()

    def set_autoplay(self, pid=None, gid=None):
        return self.save_game(requests.get(self.get_url('set_autoplay', 
            pid=pid or self.player['pid'], 
            gid=gid or self.game['gid']
        )))

    def play_move(self, play, pid=None, gid=None):
        return self.save_game(requests.get(self.get_url('play_move', 
            play=play,
            pid=pid or self.player['pid'], 
            gid=gid or self.game['gid']
        )))

    def opponent_name(self):
        if not self.player and self.game:
            raise ValueError("There is no current game")
        for p in self.game['players'].keys():
            if p not in [self.player['name'], 'treasure']:
                return p

    def last_complete_turn(self):
        if not self.player and self.game:
            raise ValueError("There is no current game")
        for turn in self.game['turns']:
            if len(turn.items()) == 3:
                return turn

    def last_turn_result(self):
        turn = self.last_complete_turn()
        myPlay = turn[self.player['name']]
        theirPlay = turn[self.opponent_name()]
        if myPlay == theirPlay:
            return 0
        if myPlay == 13 and theirPlay == 1:
            return -1
        if myPlay == 1 and theirPlay == 13:
            return 1
        if myPlay > theirPlay:
            return 1
        else:
            return -1

if __name__ == '__main__':
    api = TreasureApi('http://localhost:8000', pid=633311)
    api2 = TreasureApi('http://localhost:8000', pid=211166)

