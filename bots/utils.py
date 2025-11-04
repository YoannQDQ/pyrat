from pyrat.core.bot_utils import MOVE_E, MOVE_N, MOVE_O, MOVE_S


def direction(from_cell, to_cell):
    if to_cell[0] > from_cell[0]:
        direction = MOVE_S
    elif to_cell[0] < from_cell[0]:
        direction = MOVE_N
    elif to_cell[1] < from_cell[1]:
        direction = MOVE_O
    else:
        direction = MOVE_E
    return direction


def manhattan_distance(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
