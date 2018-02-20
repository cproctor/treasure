# A simpler client--just gets a game started right away.

# Note for BB&A students: 
# The simplest possible treasure client would simply create a new class which inherits from
# TreasureAutoplayClient and overrides the `render` method. 

from api import TreasureApi
from six.moves import input 


class TreasureAutoplayClient:
    "A class which autoplays a treasure game"

    def __init__(self, url, pid):
        "Creates a new instance of the api we can use, and starts a new game."

        self.api = TreasureApi(url=url, pid=pid) 
        self.api.new_game()
        self.api.set_autoplay()
        while self.api.game['status'] != 'complete':
            self.render()
            move = self.ask_player_to_choose_move()
            self.api.play_move(move)
        self.conclude_game()

    def render(self):
        "Presents a game state. (The api serves as our model, holding the game state.)"

        if len(self.api.game['turns']) > 1:
            print("LAST TURN I PLAYED {} AND {} PLAYED {}.".format(
                self.my_last_play(), 
                self.your_name(),
                self.your_last_play()
            ))
            print("THE SCORE IS {} (ME) to {} ({})".format(
                self.my_score(),
                self.your_score(), 
                self.your_name()
            ))
        print("THE TREASURE IS {}.".format(
            self.treasure()
        ))
        print("THE CARDS IN MY HAND ARE {}.".format(
            ", ".join(str(card) for card in self.my_hand())
        ))  

    def ask_player_to_choose_move(self):
        "Asks the player to choose a legal move, and then returns it."

        while True:
            choice = input("PLEASE CHOOSE A MOVE: ")
            if choice.isdigit() and int(choice) in self.my_hand():
                return int(choice)
            print("YOU DON'T HAVE THAT CARD. TRY AGAIN.")

    def conclude_game(self):
        "Wraps up the game"
        print("THE FINAL SCORE WAS {} (ME) TO {} ({})".format(
            self.my_score(),
            self.your_score(), 
            self.your_name()
        ))
        if self.my_score() > self.your_score():
            print("YAY! I WIN.")
        elif self.my_score() < self.your_score():
            print("ALAS. I LOST.")
        else:
            print("WEIRD. WE TIED.")
        

    # Helpers. These just make the job a little easier.

    def my_name(self):
        return self.api.player['name']

    def your_name(self):
        return self.api.opponent_name()

    def treasure(self):
        return self.api.game['turns'][0]['treasure']

    def my_score(self):
        return self.api.game['players'][self.my_name()]['score']

    def your_score(self):
        return self.api.game['players'][self.your_name()]['score']

    def my_hand(self):
        return self.api.game['players'][self.my_name()]['hand']

    def your_hand(self):
        return self.api.game['players'][self.your_name()]['hand']
   
    def my_last_play(self):
        if self.api.game['status'] == 'playing':
            return self.api.game['turns'][1][self.my_name()]
        if self.api.game['status'] == 'complete':
            return self.api.game['turns'][0][self.my_name()]

    def your_last_play(self):
        if self.api.game['status'] == 'playing':
            return self.api.game['turns'][1][self.your_name()]
        if self.api.game['status'] == 'complete':
            return self.api.game['turns'][0][self.your_name()]




# Checks to see whether this script has been executed directly 
# (versus imported by another script). If it has been executed directly, 
# then start a game! But don't do that if it was imported--perhaps the other script
# just wants to use the TreasureAutoplayClient class for its own purposes...
# This is a common idiom in Python programs
if __name__ == '__main__':
    URL = "http://treasure.chrisproctor.net"
    PID = 56231
    client = TreasureAutoplayClient(URL, PID)

    
