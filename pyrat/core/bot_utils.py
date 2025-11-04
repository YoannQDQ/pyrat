import logging

import numpy as np

INFINI = 0  # Infinity

MOVE_N = "N"
MOVE_S = "S"
MOVE_O = "O"
MOVE_E = "E"

logger = logging.getLogger("bot")


def direction(from_cell, to_cell):
    if to_cell[1] > from_cell[1]:
        direction = MOVE_N
    elif to_cell[1] < from_cell[1]:
        direction = MOVE_S
    elif to_cell[0] < from_cell[0]:
        direction = MOVE_O
    else:
        direction = MOVE_E
    return direction


def neighbors_map(maze_map, height):
    res = {}
    for cell in maze_map:
        res[transpose_cell(cell, height)] = [transpose_cell(c, height) for c in maze_map[cell]]
    return res


def transpose_cell(cell, maze_height, reverse=False):
    """Transpose a cell from (x, y) to (i, j) indexing"""
    if reverse:
        return (cell[1], maze_height - 1 - cell[0])
    return (maze_height - 1 - cell[1], cell[0])


##################################################
# Matrice des accès (type matrice adjacence)     #
# en entrée maze_map, maze_width, maze_height       #
# En sortie : la matrice des accès (0 ou 1)      #
##################################################
def matrice_access(maze_map, maze_width, maze_height):  # boiteau 24/04/2025
    nb_cells = maze_width * maze_height
    x = maze_map[(0, 0)]
    res = np.zeros((nb_cells, nb_cells))
    for i in range(maze_width):
        for j in range(maze_height):  # tenir compte de la symétrie de res et s'arrêter avant ...
            num = j * maze_width + i
            x = maze_map[(i, j)]
            # voisin de droite
            if i < maze_width - 1:
                if (i + 1, j) in x:
                    res[num, num + 1] = x[(i + 1, j)]
                    res[num + 1, num] = x[(i + 1, j)]
                else:
                    res[num, num + 1] = INFINI
                    res[num + 1, num] = INFINI
            # voisin de gauche
            if i > 0:
                if (i - 1, j) in x:
                    res[num, num - 1] = x[(i - 1, j)]
                    res[num - 1, num] = x[(i - 1, j)]
                else:
                    res[num, num - 1] = INFINI
                    res[num - 1, num] = INFINI
            # voisin haut
            if j < maze_height - 1:
                if (i, j + 1) in x:
                    res[num, num + maze_width] = x[(i, j + 1)]
                    res[num + maze_width, num] = x[(i, j + 1)]
                else:
                    res[num, num + maze_width] = INFINI
                    res[num + maze_width, num] = INFINI
            # voisin bas
            if j > 0:
                if (i, j - 1) in x:
                    res[num, num - maze_width] = x[(i, j - 1)]
                    res[num - maze_width, num] = x[(i, j - 1)]
                else:
                    res[num, num - maze_width] = INFINI
                    res[num - maze_width, num] = INFINI

    return res
