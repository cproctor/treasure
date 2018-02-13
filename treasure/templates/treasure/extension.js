
var noPlayer = {pid:0};
var noGame = {gid:0, turns:[{treasure:0}], players:{}};
var hand = [1,2,3,4,5,6,7,8,9,10,11,12,13];

var has_cards_yes_no = function(cards) {
    var has_card = function(card) { return cards.includes(card); }
    var yes_no = function(bool) { return bool ? 'Y' : 'N'; }
    return hand.map(has_card).map(yes_no).join('');
}

function TreasureApi(url) {
    this.base_url = url;
};

TreasureApi.prototype = {
    urls: {
        'new_player': 'players/new/{name}',
        'show_player': 'players/{pid}',
        'new_game': 'players/{pid}/games/new',
        'join_game': 'players/{pid}/games/{gid}/join',
        'resume_game': 'players/{pid}/games/resume',
        'join_any_game': 'players/{pid}/games/join',
        'show_game': 'players/{pid}/games/{gid}',
        'play_move': 'players/{pid}/games/{gid}/play/{play}'
    },

    get_url: function(key, pid, gid, play, name) {
        return this.base_url + this.urls[key]
            .replace('{pid}', pid)
            .replace('{gid}', gid)
            .replace('{play}', play)
            .replace('{name}', name)
    },

    fetch_player: function(url, callback) {
        var self = this;
        $.ajax({
            url: url,
            success: function(player) {
                self.player = player;
                self.player_error = null;
                if (callback) callback();
            },
            error: function(err) {
                self.player_error = err.responseJSON.error;
                if (callback) callback();
            }
        })
    },

    fetch_game: function(url, callback) {
        var self = this;
        $.ajax({
            url: url,
            success: function(game) {
                self.game = game;
                self.game_error = null;
                if (callback) callback();
            },
            error: function(err) {
                self.game_error = err.responseJSON.error;
                if (callback) callback();
            }
        })
    },
    new_player: function(name, callback) {
        var url = this.get_url('new_player', null, null, null, name);
        this.fetch_player(url, callback);
    },
    get_player: function(pid, callback) {
        var url = this.get_url('show_player', pid);
        this.fetch_player(url, callback);
    },
    new_game: function(callback) {
        var url = this.get_url('new_game', (this.player || noPlayer).pid);
        this.fetch_game(url, callback);
    },
    join_any_game: function(callback) {
        var url = this.get_url('join_any_game', (this.player || noPlayer).pid);
        this.fetch_game(url, callback);
    },
    resume_game: function(callback) {
        var url = this.get_url('resume_game', (this.player || noPlayer).pid)
        this.fetch_game(url, callback);
    },
    join_game: function(gid, callback) {
        var url = this.get_url('join_game', (this.player || noPlayer).pid, gid)
        this.fetch_game(url, callback);
    },
    get_game: function(gid, callback) {
        var url = this.get_url('show_game', (this.player || noPlayer).pid, gid)
        this.fetch_game(url, callback);
    },
    play_move: function(play, callback) {
        var url = this.get_url('play_move', (this.player || noPlayer).pid, (this.game || noGame).gid, play);
        this.fetch_game(url, callback);
    },
    sync: function() {
        if (!this.player_error && !this.game_error) {
            //if (this.player) this.get_player(this.player.pid);
            if (this.player && this.game) this.get_game(this.game.gid);       
        }
    },
    opponent_name: function() {
        for (name in (this.game || noGame).players) {
            if (name !== this.player.name && name !== 'treasure') return name;
        }
        return "";
    },
    player_can_play: function() {
        return this.game && this.game.status == 'playing' && !(this.player.name in this.game.turns[0]);
    },
    player_hand: function() {
        if (!this.game) return "";
        return has_cards_yes_no(this.game.players[this.player.name].hand);
    },
    opponent_hand: function() {
        if (!this.game) return "";
        return has_cards_yes_no(this.game.players[this.opponent_name()].hand);
    }
}

api = new TreasureApi("http://treasure.chrisproctor.net/");

(function(ext) {
    ext._shutdown = function() {};
    ext._getStatus = function() { return {status: 2, msg: 'Ready'};};

    ext.player_id = function() {return (api.player || noPlayer).pid;}
    ext.player_name = function() {return (api.player || noPlayer).name || "";}
    ext.opponent_name = api.opponent_name.bind(api);
    ext.game_id = function() {return (api.game || noGame).gid;}
    ext.treasure = function() {return (api.game || noGame).turns[0].treasure || "";}
    ext.player_score = function() { if (!api.game) return ""; return api.game.players[api.player.name].score;}
    ext.opponent_score = function() { if (!api.game) return ""; return api.game.players[api.opponent_name()].score;}
    ext.player_hand = api.player_hand.bind(api);
    ext.opponent_hand = api.opponent_hand.bind(api);

    ext.new_player = api.new_player.bind(api);
    ext.get_player = api.get_player.bind(api);
    ext.new_game = api.new_game.bind(api);
    ext.join_any_game = api.join_any_game.bind(api);
    ext.get_game = api.get_game.bind(api);
    ext.join_game = api.join_game.bind(api);
    ext.resume_game = api.resume_game.bind(api);
    ext.play_move = api.play_move.bind(api);
    ext.my_turn = api.player_can_play.bind(api);

    ext.game_status = function() { if (!api.game) return ""; return api.game.status; }
    ext.player_ok = function() { return !api.player_error;}
    ext.game_ok = function() { return !api.game_error;}
    ext.player_error_message = function() { return api.player_error || "";}
    ext.game_error_message = function() { return api.game_error || "";}

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['r', 'player name', 'player_name'],
            ['r', 'opponent name', 'opponent_name'],
            ['r', 'treasure', 'treasure'],
            ['r', 'player hand', 'player_hand'],
            ['r', 'opponent hand', 'opponent_hand'],
            ['r', 'player score', 'player_score'],
            ['r', 'opponent score', 'opponent_score'],

            ['b', "it's my turn", "my_turn"],

            ['w', "sign up as %s", 'new_player', 'name'],
            ['w', "sign in as %n", 'get_player'],
            ['w', "start a new game", 'new_game'],
            ['w', "join any open game", 'join_any_game'],
            ['w', "join game %n", 'join_game'],
            ['w', "resume a game I'm playing", 'resume_game'],
            ['w', "play %n", 'play_move'],

            ['r', 'player id', 'player_id'],
            ['r', 'game id', 'game_id'],
            ['r', 'game status', 'game_status'],
            ['b', 'player ok', 'player_ok'],
            ['b', 'game ok', 'game_ok'],
            ['r', 'player error message', 'player_error_message'],
            ['r', 'game error message', 'game_error_message'],
        ]
    };

    // Register the extension
    ScratchExtensions.register('Treasure extension', descriptor, ext);
})({});
