# This is an example of how you might re-use the code from api and client_autoplay
# to write your own text-based interface. All you need to do is implement your own
# `render` method.

from client_autoplay import TreasureAutoplayClient
from random import choice

class FunnyClient(TreasureAutoplayClient):

    def render(self):
        if len(self.api.game['turns']) > 1:
            print(self.tell_last_turn_result() + ' ' + self.tell_score())
        print(self.tell_smalltalk() + ' ' + self.tell_treasure() + ' ' + self.tell_hand())
        

    def tell_last_turn_result(self):
        return "Last turn, {} played {}.".format(
            self.your_name(), 
            self.your_last_play()
        )

    def tell_score(self):
        return "Here's how it is. You've got {} and {} has {}.".format(
            self.my_score(),
            self.your_name(),
            self.your_score()
        )

    def tell_smalltalk(self):
        return choice([
            "Oh, hey there. It's your turn!",
            "sup.",
            "Yoo-hoo darling!",
            "Pardon, if now is a good time, it is your turn."
        ])

    def tell_treasure(self):
        if self.treasure() == 13:
            return "Whoa! It's the big treasure!"
        elif self.treasure() == 1: 
            return "Hey there! The treasure is 1."
        elif self.treasure() > 7:
            return "Look out--pretty big {} treasure incoming. What are you going to do?".format(self.treasure())
        else:
            return "It's a little {} treasure this time.".format(self.treasure())

    def tell_hand(self):
        return "Here's what you've got left: {}".format(
            ", ".join(str(card) for card in self.my_hand())
        )
        
# Checks to see whether this script has been executed directly 
# (versus imported by another script). If it has been executed directly, 
# then start a game! But don't do that if it was imported--perhaps the other script
# just wants to use the TreasureAutoplayClient class for its own purposes...
# This is a common idiom in Python programs
if __name__ == '__main__':
    URL = "http://treasure.chrisproctor.net"
    PID = 56231
    client = FunnyClient(URL, PID)

    
