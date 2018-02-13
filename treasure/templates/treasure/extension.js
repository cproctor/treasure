
function TreasureApi(url) {
    this.base_url = url;
    this.ok = true;
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
        return this.urls[key]
            .replace('{pid}', pid)
            .replace('{gid}', gid)
            .replace('{play}', play)
            .replace('{name}', name)
    },

    fetch_player: function(url, callback) {
        var self = this;
        $.ajax({
            url: this.base_url + url,
            success: function(player) {
                console.log(player);
                self.player = player;
                callback();
            },
            error: function(err) {
                console.log(err);
                self.error = err.message;
                callback();
            }
        })
    },

    new_player: function(name, callback) {
        console.log("GETTING NEW PLAYER");
        this.fetch_player(this.get_url('new_player', null, null, null, name), callback);
    }
}

api = new TreasureApi("http://treasure.chrisproctor.net/");



(function(ext) {
    var my_turn = false;
    ext._shutdown = function() {};
    ext._getStatus = function() { return {status: 2, msg: 'Ready'};};

    ext.is_ok = function() {return api.ok;}
    ext.error_message = function() {return "TEST ERROR";}
    ext.player_id = function() {return (api.player || {}).pid;}
    ext.player_name = function() {return (api.player || {}).name;}
    ext.game_id = function() {return (api.game || {}).gid;}

    ext.new_player = api.new_player.bind(api);

    ext.when_my_turn = function() {};

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['r', 'error message', 'error_message'],
            ['b', 'OK', 'is_ok'],
            ['r', 'player id', 'player_id'],
            ['r', 'player name', 'player_name'],
            ['r', 'game id', 'game_id'],

            ['h', "when it's my turn", "when_my_turn"],

            ['w', "sign up as %s", 'new_player', 'name']
        ]
    };

    // Register the extension
    ScratchExtensions.register('Treasure extension', descriptor, ext);
})({});

/*
Blocks I need:
    reporters
        PID
        GID
        name
        join any game
        

*/
