from api import TreasureApi
from argparse import ArgumentParser
from time import sleep


class TreasureClient:
    def __init__(self, url=None, pid=None, name=None, gid=None):
        self.api = TreasureApi(url=args.url, pid=args.pid, name=args.name)
        if gid and gid in api.player['games_playing']:
            self.api.get_game(gid=gid)
        else:
            self.select_game()

    def select_game(self):
        print("How would you like to join a game?")
        while not self.prompt_choices([
            ('n', 'new game', self.new_game),
            ('r', 'resume an ongoing game', self.api.resume_game),
            ('j', 'join any game', self.api.join_any_game),
            ('s', 'join a specific game', self.join_game)
        ]):
            print("Sorry, that didn't work. Please choose an option:")

        print("Playing game {} against {}".format(self.api.game['gid'], self.api.opponent_name()))
        self.play_turn()

    def new_game(self):
        self.api.new_game()
        return self.wait_for_game_to_start()

    def wait_for_game_to_start(self):
        self.api.get_game()
        if self.api.game['status'] == 'playing':
            return True
        print("Waiting for another player to join.")
        return self.prompt_choices([
            ('w', 'keep waiting', self.wait_for_game_to_start),
            ('o', 'choose another game', self.select_game)
        ])

    def join_game(self):
        return self.api.join_game(gid=input("Game ID: "))

    def play_turn(self):
        if self.api.can_play():
            hand = self.api.game['players'][self.api.player['name']]['hand']
            print("Treasure is {}. Choose a play. (Your hand is {}.)".format(
                self.api.game['turns'][0]['treasure'], 
                ", ".join(str(card) for card in hand)
            ))
            while not self.api.play_move(play=input("> ")):
                print("That's not a valid choice.")

        if self.api.game['status'] == 'playing':
            print("Waiting for opponent's move...")
        while self.api.game['status'] == 'playing' and not self.api.can_play():
            self.api.get_game()
            sleep(1)

        print("{} plays {}. You {}.".format(
            self.api.opponent_name(),
            self.api.last_complete_turn()[self.api.opponent_name()],
            {-1: 'lose', 0: 'tie', 1: 'win'}[self.api.last_turn_result()]
        ))
        print("Your score: {}. {}'s score: {}".format(
            self.api.game['players'][self.api.player['name']]['score'],
            self.api.opponent_name(),
            self.api.game['players'][self.api.opponent_name()]['score'],
        ))
        if self.api.game['status'] == 'playing':
            self.play_turn()
        else:
            self.end_game()

    def end_game(self):
        print("Game over. Your score: {}; Opponent's score: {}".format(
            self.api.game['players'][self.api.player['name']]['score'],
            self.api.game['players'][self.api.opponent_name()]['score'],
        ))
        self.select_game()
        
    def prompt_choices(self, choices):
        for key, message, action in choices:
            print("  [{}] {}".format(key, message))
        while True:
            choice = input("> ")
            for key, message, action in choices:
                if choice == key: 
                    return action()


if __name__ == '__main__':
    parser = ArgumentParser(description='Play treasure')
    parser.add_argument('--url', default="http://localhost:8000", help="treasure server url")
    parser.add_argument('--pid', help="player id, if already existing")
    parser.add_argument('--name', help="player name, if creating a new player")
    parser.add_argument('--gid', help="game id, if already existing")
    args = parser.parse_args()
    client = TreasureClient(url=args.url, pid=args.pid, name=args.name, gid=args.gid)

