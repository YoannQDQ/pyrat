#!/usr/bin/env python
#    Copyright Â© 2017 Vincent Gripon (vincent.gripon@imt-atlatique.fr) and IMT Atlantique
#
#    This file is part of PyRat.
#
#    PyRat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyRat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.
import random
import re
import sys
from ast import literal_eval
from pathlib import Path

from pyrat.core.bot_utils import transpose_cell


# compute the connected component of a given initial cell with depth-first search
def connected_region(maze, cell, connected, possible_border):
    for i, j in maze[cell]:
        if connected[i][j] == 0:
            connected[i][j] = 1
            possible_border.append((i, j))
            connected_region(maze, (i, j), connected, possible_border)


def gen_mud(mud_density, mud_range):
    if random.uniform(0, 1) < mud_density:
        return random.randrange(2, mud_range + 1)
    return 1


def generate_maze(width, height, target_density, connected, symmetry, mud_density, mud_range, maze_file, seed):
    if maze_file != "":
        content = Path(maze_file).read_text()
        lines = content.split("\n")
        width = int(lines[0])
        height = int(lines[1])
        maze = {}
        for i in range(width):
            for j in range(height):
                maze[(i, j)] = {}
                line = lines[i + j * width + 2].split(" ")
                if line[0] != "0":
                    maze[(i, j)][(i, j + 1)] = int(line[0])
                if line[1] != "0":
                    maze[(i, j)][(i, j - 1)] = int(line[1])
                if line[2] != "0":
                    maze[(i, j)][(i - 1, j)] = int(line[2])
                if line[3] != "0":
                    maze[(i, j)][(i + 1, j)] = int(line[3])
        line = lines[height * width + 2].split(" ")
        pieces_of_cheese = []
        for index in line:
            pieces_of_cheese.append((int(index) % width, int(index) // width))
    else:
        random.seed(seed)
        # Start with purely random maze
        maze = {}
        not_considered = {}
        for i in range(width):
            for j in range(height):
                maze[(i, j)] = {}
                not_considered[(i, j)] = True
        for i in range(width):
            for j in range(height):
                if not (symmetry) or not_considered[(i, j)]:
                    if random.uniform(0, 1) > target_density and i + 1 < width:
                        m = gen_mud(mud_density, mud_range)
                        maze[(i, j)][(i + 1, j)] = m
                        maze[(i + 1, j)][(i, j)] = m
                        if symmetry:
                            maze[(width - 1 - i, height - 1 - j)][(width - 2 - i, height - 1 - j)] = m
                            maze[(width - 2 - i, height - 1 - j)][(width - 1 - i, height - 1 - j)] = m
                    if random.uniform(0, 1) > target_density and j + 1 < height:
                        m = gen_mud(mud_density, mud_range)
                        maze[(i, j)][(i, j + 1)] = m
                        maze[(i, j + 1)][(i, j)] = m
                        if symmetry:
                            maze[(width - 1 - i, height - 2 - j)][(width - 1 - i, height - 1 - j)] = m
                            maze[(width - 1 - i, height - 1 - j)][(width - 1 - i, height - 2 - j)] = m
                    if symmetry:
                        not_considered[(i, j)] = False
                        not_considered[(width - 1 - i, height - 1 - j)] = False
        for i in range(width):
            for j in range(height):
                if len(maze[(i, j)]) == 0 and (i == 0 or j == 0 or i == width - 1 or j == height - 1):
                    m = gen_mud(mud_density, mud_range)
                    possibilities = []
                    if i + 1 < width:
                        possibilities.append((i + 1, j))
                    if j + 1 < height:
                        possibilities.append((i, j + 1))
                    if i - 1 >= 0:
                        possibilities.append((i - 1, j))
                    if j - 1 >= 0:
                        possibilities.append((i, j - 1))
                    chosen = possibilities[random.randrange(len(possibilities))]
                    maze[(i, j)][chosen] = m
                    maze[chosen][(i, j)] = m
                    if symmetry:
                        ii, jj = chosen
                        maze[(width - 1 - i, height - 1 - j)][(width - 1 - ii, height - 1 - jj)] = m
                        maze[(width - 1 - ii, height - 1 - jj)][(width - 1 - i, height - 1 - j)] = m

        # Then connect it
        if connected:
            connected = [[0] * height] * width
            possible_border = [(0, height - 1)]
            connected[0][height - 1] = 1
            connected_region(maze, (0, height - 1), connected, possible_border)
            while 1:
                border = []
                new_possible_border = []
                for i, j in possible_border:
                    is_candidate = False
                    if (i + 1, j) not in maze[(i, j)] and i + 1 < width and connected[i + 1][j] == 0:
                        border.append(((i, j), (i + 1, j)))
                        is_candidate = True
                    if (i - 1, j) not in maze[(i, j)] and i > 0 and connected[i - 1][j] == 0:
                        border.append(((i, j), (i - 1, j)))
                        is_candidate = True
                    if (i, j + 1) not in maze[(i, j)] and j + 1 < height and connected[i][j + 1] == 0:
                        border.append(((i, j), (i, j + 1)))
                        is_candidate = True
                    if (i, j - 1) not in maze[(i, j)] and j > 0 and connected[i][j - 1] == 0:
                        border.append(((i, j), (i, j - 1)))
                        is_candidate = True
                    if is_candidate:
                        new_possible_border.append((i, j))
                possible_border = new_possible_border
                if border == []:
                    break
                a, b = border[random.randrange(len(border))]
                m = gen_mud(mud_density, mud_range)
                maze[a][b] = m
                maze[b][a] = m
                ai, aj = a
                bi, bj = b
                if symmetry:
                    bsym = (width - 1 - bi, height - 1 - bj)
                    asym = (width - 1 - ai, height - 1 - aj)
                    maze[asym][bsym] = m
                    maze[bsym][asym] = m
                connected[bi][bj] = 1
                connected_region(maze, b, connected, possible_border)
                possible_border.append(b)
                if symmetry and connected[width - 1 - bi][height - 1 - bj] == 0 and connected[width - 1 - ai][height - 1 - aj] == 1:
                    connected[width - 1 - bi][height - 1 - bj] = 1
                    connected_region(maze, bsym, connected, possible_border)
                    possible_border.append(bsym)
        pieces_of_cheese = []
    return width, height, pieces_of_cheese, maze


def generate_players_positions(width, height, symmetry, player1_location, player2_location, start_random):
    if symmetry:
        if start_random:
            player1_location = (random.randrange(width // 2 - 1), random.randrange(height // 2 - 1))
        if player1_location == (-1, -1):
            player1_location = (0, 0)
        player2_location = width - player1_location[0] - 1, height - player1_location[1] - 1

    else:
        if start_random:
            player1_location = (random.randrange(width), random.randrange(height))
            player2_location = (random.randrange(width), random.randrange(height))
        if player1_location == (-1, -1):
            player1_location = (0, 0)
        if player2_location == (-1, -1):
            player2_location = (width - 1, height - 1)

    return player1_location, player2_location


# Generate pieces of cheese
def generate_pieces_of_cheese(nb_pieces, width, height, symmetry, player1_location, player2_location):
    # Simple case, no symmetry, simply select random locations among available ones
    if not symmetry:
        avaliable_locations = list({(x, y) for x in range(width) for y in range(height)} - {player1_location, player2_location})
        return random.sample(avaliable_locations, max(1, min(nb_pieces, len(avaliable_locations))))

    # Symmetric case
    avaliable_locations = {(x, y) for x in range(width // 2) for y in range(height)}

    # odd width case, add the first half of the central column
    if width % 2 == 1:
        avaliable_locations.update({(width // 2, y) for y in range(height // 2)})
    avaliable_locations = list(avaliable_locations - {player1_location, player2_location})

    # Odd number of pieces case, reserve the center cell
    positions = []
    if nb_pieces % 2 == 1:
        if width % 2 == 0 or height % 2 == 0:
            sys.exit("The maze has even width or even height and thus cannot contain an odd number of pieces of cheese if symmetric.")
        center_cell = (width // 2, height // 2)
        if center_cell in (player1_location, player2_location):
            sys.exit("Cannot place odd number of pieces of cheese symmetrically when one player is at the center cell.")
        positions.append(center_cell)

    for x, y in random.sample(avaliable_locations, nb_pieces // 2):
        positions.append((x, y))
        positions.append((width - x - 1, height - y - 1))

    return positions


def generate_pieces_of_cheese_notrandom(width, height, symmetry, player1_location, player2_location, position_cheese):
    positions = []

    def check_position(i, j, symmetry=False):
        nonlocal positions
        i, j = int(i), int(j)
        if (i, j) == player1_location or (i, j) == player2_location:
            sys.exit(f"position_cheese invalid argument {(i, j)}: cheese on player")
        if i < 0 or i >= height or j < 0 or j >= width:
            sys.exit(f"position_cheese invalid argument {(i, j)}: {position_cheese}")
        positions.append((i, j))
        if symmetry:
            check_position(height - 1 - i, width - 1 - j, False)

    try:
        with Path(position_cheese).open() as test:
            pattern = r"(\d+).*(\d+)"
            for line in enumerate(test, 1):
                if match := re.match(pattern, line):
                    check_position(int(match[1]), int(match[2]), symmetry)
    except FileNotFoundError:
        try:
            raw = list(literal_eval(position_cheese))
            if len(raw) > 0:
                if isinstance(raw[0], tuple | list):  # Accept input as (i1,j1),(i2,j2),...,(in,jn) or [i1,j1], [i2,j2], ... , [in,jn]
                    raw = list(raw)
                elif isinstance(raw[0], int):  # Accept input as i1,j1,i2,j2,...,in,jn
                    raw = [tuple(raw[i : i + 2]) for i in range(0, len(raw), 2)]
                else:
                    sys.exit(f"position_cheese invalid argument: {position_cheese}")
                for cheese in raw:
                    check_position(*cheese, symmetry)
        except (ValueError, SyntaxError):
            sys.exit(f"position_cheese invalid argument: {position_cheese}")

    # Transpose positions from i,j to x,y
    positions = [transpose_cell(pos, height, reverse=True) for pos in positions]

    return positions
