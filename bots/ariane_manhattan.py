from bots.utils import direction, manhattan_distance

ariane_thread = []
dead_ends = []


def go(neighbors_map, player_location, pieces_of_cheese):
    choices = neighbors_map[player_location]
    new_choices = [c for c in choices if c not in ariane_thread and c not in dead_ends]
    if not new_choices:
        dead_ends.append(player_location)
        target = ariane_thread.pop()
    else:
        # Select the closest cheese among new choices
        closest_distance = -1
        for choice in new_choices:
            for cheese in pieces_of_cheese:
                dist = manhattan_distance(choice, cheese)
                if closest_distance == -1 or dist < closest_distance:
                    closest_distance = dist
                    target = choice

        ariane_thread.append(player_location)

    return direction(player_location, target)
