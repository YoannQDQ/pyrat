import random

from bots.utils import direction


def go(neighbors_map, player_location, pieces_of_cheese):
    choices = neighbors_map[player_location]
    target = random.choice(choices)
    return direction(player_location, target)
