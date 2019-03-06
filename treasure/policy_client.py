# This client connects to the treasure server and automatically plays games according to a policy. 
# A policy is a function which is given a game state and player name, and then chooses the 
# next card to play. Examples are below.

from api import TreasureApi
from time import sleep
import logging

class TreasurePolicyClient:
    def __init__(self, url, pid, policy, interval=2, log=None):
        self.policy = policy
        self.log = log or get_logger(__file__, "policy_client.log")
        self.interval = interval
        self.pid = pid
        self.api = TreasureApi(url=url, pid=pid)
        self.games = []

    def play_open_games(self):
        """
        Automatically plays whenever it can, on all open games. Aditionally makes sure 
        there is always one game waiting to start, so that others can join.
        """
        while True:
            self.play_all_possible_turns()
            sleep(self.interval)

    def play_all_games(self):
        """
        Joins every available game and plays whenever possible.
        """
        while True: 
            while self.api.join_any_game():
                self.log.info("Joined game {}".format(self.api.game['gid']))
            self.play_all_possible_turns()
            sleep(self.interval)

    def play_all_possible_turns(self):
        profile = self.api.get_player()
        if not any(profile['games_waiting']):
            self.api.new_game()
            self.log.info("Created game {}".format(self.api.game['gid']))
        for gid in profile['games_playing']:
            game = self.api.get_game(gid=gid)
            choice = self.policy(game, self.api.player['name'])
            self.log.info("Playing {} in game {}".format(choice, gid))
            self.api.play_move(choice)

def get_logger(logName, fileName, level=logging.DEBUG):
    "Gets a preconfigured logger"
    log = logging.getLogger(logName)
    log.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh = logging.FileHandler(fileName)
    sh = logging.StreamHandler()
    for h in [fh, sh]:
        h.setLevel(level)
        h.setFormatter(formatter)
        log.addHandler(h)
    return log

if __name__ == '__main__':
    from policies import nearest_card_policy
    client = TreasurePolicyClient("http://treasure.chrisproctor.net", 16261, nearest_card_policy)
    client.play_all_games()
    
        
            
