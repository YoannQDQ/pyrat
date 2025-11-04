import random

from bots.utils import direction

ariane_thread = []
dead_ends = []


def go(neighbors_map, player_location, pieces_of_cheese):
    choices = neighbors_map[player_location]
    new_choices = [c for c in choices if c not in ariane_thread and c not in dead_ends]
    if not new_choices:
        dead_ends.append(player_location)
        target = ariane_thread.pop()
    else:
        target = random.choice(new_choices)
        ariane_thread.append(player_location)
    return direction(player_location, target)
