from random import choice

# Implements strategies the bot player might choose

def random_strategy(state):
    "Returns a random card from the hand"
    return choice(hand(state))

def near_treasure_strategy(state):
    "Returns one of the three cards nearest the treasure"
    treasure = state['turns'][0]['treasure']
    cards_near_treasure = [card for dist, card in sorted([(abs(i - treasure), i) for i in hand(state)])]
    return choice(cards_near_treasure[:3])

def hand(state):
    return state['players']['bot']['hand']


strategies = {
    'RANDOM': random_strategy, 
    'NEAR_TREASURE': near_treasure_strategy
}


