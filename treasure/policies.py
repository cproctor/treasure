# Implements policies (stratgies that choose a play when given a game state) and helper functions

from itertools import count
from random import randint

def nearest_card_policy(game, name):
    hand = game['players'][name]['hand']
    treasure = game['turns'][0]['treasure']
    return nearest(hand, treasure, randint(0,1))

def nearest(hand, target, prefer_higher=True):
    sign = 1 if prefer_higher else -1
    for i in count():
        if target + (sign * i) in hand:
            return target + (sign * i)
        if target - (sign * i) in hand:
            return target - (sign * i)

def greater_than_or_equal(hand, target):
    for card in hand:
        if card >= target: 
            return card
    
def less_than_or_equal(hand, target):
    for card in reversed(hand):
        if card <= target: 
            return card
