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

import logging
import math
import random
import sys
from dataclasses import dataclass
from functools import cache, lru_cache

import pygame

from pyrat.core.parameters import args
from pyrat.core.spritesheet import image_at

logger = logging.getLogger("display")

# Yellow color for python
PYTHON_COLOR = (255, 255, 0)
# RED color for rat
RAT_COLOR = (255, 0, 0)


@lru_cache(maxsize=128)
def image(path, scalex, scaley):
    return pygame.transform.scale(pygame.image.load(path), (scalex, scaley))


class MazePainter:
    def __init__(self, maze, cell_size=32):
        self.maze = maze
        self.cell_size = cell_size
        last_cell = list(maze.keys())[-1]
        self.columns = last_cell[0] + 1
        self.rows = last_cell[1] + 1
        self.margins = 5
        self.surface = pygame.Surface((self.columns * self.cell_size + 2 * self.margins, self.rows * self.cell_size + 2 * self.margins))
        self.compute_floor()
        self.compute_walls()

        self.animation_index = 0

    def draw_floor(self):
        self.surface.blit(self.floor, (0, 0))

    def draw_walls(self):
        self.surface.blit(self.walls, (0, 0))

    def draw_explored_cell(self, new_location, color):
        # Create semi-transparent solid color surface
        seen_cell = pygame.Surface((self.cell_size, self.cell_size))
        seen_cell.set_alpha(50)  # Set transparency level (0-255)
        seen_cell.fill(color)  # Fill with color
        self.draw_tile(seen_cell, *new_location, target=self.floor)

    def draw_pieces_of_cheese(self, pieces_of_cheese):
        for i, j in pieces_of_cheese:
            self.draw_image("resources/gameElements/cheese.png", i, j)

    def draw_tile(self, surface, i, j, target=None):
        """Warning: i means column and j means row, and (0,0) is bottom-left corner"""
        target = target or self.surface
        target.blit(surface, (self.cell_size * i + self.margins, self.cell_size * (self.rows - 1 - j) + self.margins))

    def draw_image(self, path, i, j, target=None):
        tile = image(path, self.cell_size, self.cell_size)
        self.draw_tile(tile, i, j, target=target)

    def draw_player(self, player_location, rotation, player_type):
        if player_type == "rat":
            self.animation_index = (self.animation_index + 1) % (3 * 8)
            if rotation == 0:
                y = 3 * 32
            if rotation == 90:
                y = 1 * 32
            if rotation == 180:
                y = 0
            if rotation == 270:
                y = 2 * 32
            sprite = image_at("resources/gameElements/rat_sprite_sheet.png", (self.animation_index // 8 * 32, y, 32, 32), colorkey=(0, 255, 0))

        else:
            sprite = image("resources/gameElements/moving_snake.png", self.cell_size, self.cell_size)
            if self.animation_index // 12 % 2 == 0:
                sprite = pygame.transform.flip(sprite, True, False)
            sprite = pygame.transform.rotate(sprite, rotation)

        self.draw_tile(sprite, *player_location)

    def compute_floor(self):
        self.floor = pygame.Surface((self.columns * self.cell_size + 2 * self.margins, self.rows * self.cell_size + 2 * self.margins))
        self.floor.fill((0, 0, 0))
        image_tiles = [image(f"resources/gameElements/tile{i}.png", self.cell_size, self.cell_size) for i in range(1, 11)]
        # Draw floor
        for i in range(self.columns):
            for j in range(self.rows):
                self.draw_tile(random.choice(image_tiles), i, j, target=self.floor)

    def compute_walls(self):
        self.walls = pygame.Surface((self.columns * self.cell_size + 2 * self.margins, self.rows * self.cell_size + 2 * self.margins))
        self.walls.set_colorkey((255, 0, 255))
        self.walls.fill((255, 0, 255))
        image_wall = image("resources/gameElements/wall.png", self.cell_size, self.cell_size)
        image_corner = image("resources/gameElements/corner.png", self.cell_size, self.cell_size)
        image_mud = image("resources/gameElements/mud.png", self.cell_size, self.cell_size)

        # Draw walls and mud
        for i in range(self.columns):
            for j in range(self.rows):
                if (i - 1, j) not in self.maze[(i, j)]:
                    self.draw_tile(image_wall, i, j, target=self.walls)
                elif self.maze[(i, j)][(i - 1, j)] > 1:
                    self.draw_tile(image_mud, i, j, target=self.walls)
                if (i + 1, j) not in self.maze[(i, j)]:
                    self.draw_tile(pygame.transform.rotate(image_wall, 180), i, j, target=self.walls)

                elif self.maze[(i, j)][(i + 1, j)] > 1:
                    self.draw_tile(pygame.transform.rotate(image_mud, 180), i, j, target=self.walls)

                if (i, j + 1) not in self.maze[(i, j)]:
                    self.draw_tile(pygame.transform.rotate(image_wall, 270), i, j, target=self.walls)

                elif self.maze[(i, j)][(i, j + 1)] > 1:
                    self.draw_tile(pygame.transform.rotate(image_mud, 270), i, j, target=self.walls)
                if (i, j - 1) not in self.maze[(i, j)]:
                    self.draw_tile(pygame.transform.rotate(image_wall, 90), i, j, target=self.walls)
                elif self.maze[(i, j)][(i, j - 1)] > 1:
                    self.draw_tile(pygame.transform.rotate(image_mud, 90), i, j, target=self.walls)
        # Draw Borders
        for i in range(self.columns):
            self.draw_tile(pygame.transform.rotate(image_wall, 270), i, -1, target=self.walls)
            self.draw_tile(pygame.transform.rotate(image_wall, 90), i, self.rows, target=self.walls)
        for j in range(self.rows):
            self.draw_tile(image_wall, self.columns, j, target=self.walls)
            self.draw_tile(pygame.transform.rotate(image_wall, 180), -1, j, target=self.walls)

        # Draw corners
        def draw_bottom_left_corner(i, j):
            self.draw_tile(pygame.transform.rotate(image_corner, 90), i, j, target=self.walls)
            self.draw_tile(pygame.transform.rotate(image_corner, 0), i, j - 1, target=self.walls)
            self.draw_tile(pygame.transform.rotate(image_corner, 270), i - 1, j - 1, target=self.walls)
            self.draw_tile(pygame.transform.rotate(image_corner, 180), i - 1, j, target=self.walls)

        for i in range(self.columns + 1):
            for j in range(self.rows + 1):
                high_left_wall = bool(self.maze.get((i, j)) and (i - 1, j) not in self.maze[(i, j)])
                low_left_wall = bool(self.maze.get((i, j - 1)) and (i - 1, j - 1) not in self.maze[(i, j - 1)])
                left_wall = i == 0 or i == self.columns or high_left_wall or low_left_wall

                right_bottom_wall = bool(self.maze.get((i, j)) and (i, j - 1) not in self.maze[(i, j)])
                left_bottom_wall = bool(self.maze.get((i - 1, j)) and (i - 1, j - 1) not in self.maze[(i - 1, j)])
                bottom_wall = j == 0 or j == self.rows or right_bottom_wall or left_bottom_wall

                has_bottom_left_corner = (left_wall and bottom_wall) or (low_left_wall ^ high_left_wall) or (right_bottom_wall ^ left_bottom_wall)

                if has_bottom_left_corner:
                    draw_bottom_left_corner(i, j)


@cache
def compute_label(text, color, font_size, max_width):
    font = pygame.font.Font("resources/fonts/BoldPixels.ttf", font_size)
    label = font.render(text, 1, color)
    while label.get_rect().width > max_width:
        font_size -= 1
        font = pygame.font.Font("resources/fonts/BoldPixels.ttf", font_size)
        label = font.render(text, 1, color)
    return label


def draw_text(text, color, max_width, font_size, x, y, screen, mode="center"):
    label = compute_label(text, color, font_size, max_width)
    if mode == "center":
        x = x - label.get_rect().width // 2
    pygame.draw.rect(screen, (0, 0, 0), (x, y, label.get_rect().width, label.get_rect().height))
    screen.blit(label, (x, y))


def draw_centered_text(text, color, font_size, y, surface):
    draw_text(text, color, surface.get_width(), font_size, surface.get_width() // 2, y, surface)


@dataclass
class PlayerScore:
    name: str
    score: int
    moves: int
    misses: int
    stuck: int
    alive: bool


def draw_scores(players: list[PlayerScore], screen: pygame.Surface):
    window_width, _window_height = pygame.display.get_surface().get_size()

    y_offset = 60 + 256  # Height of the player picture + top margin
    x_margin = 10

    score_surface = pygame.Surface((window_width / 6 - 2 * x_margin, 175))
    for i, player in enumerate(players):
        if player.alive:
            dest = score_surface.copy()
            draw_centered_text(player.name.title(), (255, 255, 255), 40, y=0, surface=dest)
            draw_centered_text(f"Score: {player.score}", (255, 255, 255), 50, y=50, surface=dest)
            draw_centered_text(f"Moves: {player.moves}", (0, 255, 0), 25, y=100, surface=dest)
            draw_centered_text(f"Miss: {player.misses}", (255, 0, 0), 25, y=125, surface=dest)
            draw_centered_text(f"Mud: {player.stuck}", (137, 81, 41), 25, y=150, surface=dest)

            x = x_margin if i % 2 == 0 else window_width - window_width / 6 + x_margin
            screen.blit(dest, (x, y_offset))


def play(q_out, move):
    while not q_out.empty():
        q_out.get()
    q_out.put(move)


def build_static_hub(screen: pygame.Surface, player1_is_alive, player2_is_alive):
    hub = screen.copy()
    hub.fill((0, 0, 0))
    hub.set_colorkey((0, 0, 0))
    window_width = hub.get_width()
    if player1_is_alive:
        rat = pygame.image.load("resources/illustrations/rat.png")
        rat = pygame.transform.scale(rat, (rat.get_width() * 2, rat.get_height() * 2))
        hub.blit(rat, (int(window_width / 12 - rat.get_rect().width / 2), 60))
    if player2_is_alive:
        python = pygame.image.load("resources/illustrations/python.png")
        python = pygame.transform.scale(python, (python.get_width() * 2, python.get_height() * 2))
        hub.blit(python, (int(window_width * 11 / 12 - python.get_rect().width / 2), 60))
    return hub


def run(
    maze,
    q,
    q_render_in,
    q_quit,
    p1name,
    p2name,
    q1_out,
    q2_out,
    is_human_rat,
    is_human_python,
    show_path,
    q_info,
    pieces_of_cheese,
    player1_location,
    player2_location,
    player1_is_alive,
    player2_is_alive,
    screen: pygame.Surface,
    info_object,
):
    logger.log(2, "Starting rendering")
    window_width, window_height = pygame.display.get_surface().get_size()
    turn_time = args.turn_time
    old_turn_number = -1

    logger.log(2, "Defining constants")
    clock = pygame.time.Clock()
    new_player1_location = player1_location
    new_player2_location = player2_location
    old_player1_location = new_player1_location
    old_player2_location = new_player2_location
    time_to_go1 = pygame.time.get_ticks()
    time_to_go2 = pygame.time.get_ticks()
    score1 = 0
    score2 = 0
    moves1 = 0
    moves2 = 0
    miss1 = 0
    miss2 = 0
    stuck1 = 0
    stuck2 = 0

    logger.log(2, "Trying to initialize Joystick")
    pygame.joystick.init()
    try:
        j0 = pygame.joystick.Joystick(0)
        j0.init()
        print("Enabled joystick: " + j0.get_name() + " with " + str(j0.get_numaxes()) + " axes", file=sys.stderr)
        j1 = pygame.joystick.Joystick(1)
        j1.init()
        print("Enabled joystick: " + j1.get_name() + " with " + str(j1.get_numaxes()) + " axes", file=sys.stderr)
    except pygame.error:
        pass

    logger.log(2, "Building background image")

    maze_painter = MazePainter(maze)
    hub_image = build_static_hub(screen, player1_is_alive, player2_is_alive)

    starting_time = pygame.time.get_ticks()

    text_info = ""

    player1_locations = set()
    player2_locations = set()

    logger.log(2, "Starting main loop")
    while q_quit.empty():
        logger.log(2, "Checking events")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                unicode = event.dict["unicode"].lower()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (unicode == "q" or event.key == pygame.K_ESCAPE)):
                q_quit.put("sortir")
                break
            if event.type == pygame.VIDEORESIZE or (event.type == pygame.KEYDOWN and unicode == "f"):
                if event.type == pygame.KEYDOWN and not (screen.get_flags() & 0x80000000):
                    screen = pygame.display.set_mode((info_object.current_w, info_object.current_h), pygame.FULLSCREEN)
                    window_width, window_height = info_object.current_w, info_object.current_h
                else:
                    if event.type == pygame.VIDEORESIZE:
                        window_width, window_height = event.w, event.h
                    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

                hub_image = build_static_hub(screen, player1_is_alive, player2_is_alive)

            if event.type == pygame.KEYDOWN and (is_human_rat or is_human_python):
                if event.key == pygame.K_LEFT:
                    play(q1_out, "L")
                if event.key == pygame.K_RIGHT:
                    play(q1_out, "R")
                if event.key == pygame.K_UP:
                    play(q1_out, "U")
                if event.key == pygame.K_DOWN:
                    play(q1_out, "D")
                if event.key == pygame.K_KP4:
                    play(q2_out, "L")
                if event.key == pygame.K_KP6:
                    play(q2_out, "R")
                if event.key == pygame.K_KP8:
                    play(q2_out, "U")
                if event.key == pygame.K_KP5:
                    play(q2_out, "D")

        logger.log(2, "Processing joysticks")
        try:
            x, y = j0.get_axis(3), j0.get_axis(4)
            if x < -0.7:
                play(q1_out, "L")
            if x > 0.7:
                play(q1_out, "R")
            if y < -0.7:
                play(q1_out, "U")
            if y > 0.7:
                play(q1_out, "D")
        except:
            pass
        try:
            x, y = j1.get_axis(3), j1.get_axis(4)
            if x < -0.7:
                play(q2_out, "L")
            if x > 0.7:
                play(q2_out, "R")
            if y < -0.7:
                play(q2_out, "U")
            if y > 0.7:
                play(q2_out, "D")
        except:
            pass
        logger.log(2, "Looking for updates from core program")
        while not (q.empty()):
            (
                pieces_of_cheese,
                nnew_player1_location,
                nnew_player2_location,
                score1,
                score2,
                moves1,
                moves2,
                miss1,
                miss2,
                stuck1,
                stuck2,
            ) = q.get()

            old_player1_location = new_player1_location
            old_player2_location = new_player2_location

            if not (args.desactivate_animations):
                if nnew_player1_location != new_player1_location:
                    time_to_go1 = pygame.time.get_ticks() + turn_time * maze[new_player1_location][nnew_player1_location]
                    player1_location = new_player1_location
                if nnew_player2_location != new_player2_location:
                    player2_location = new_player2_location
                    time_to_go2 = pygame.time.get_ticks() + turn_time * maze[new_player2_location][nnew_player2_location]
            new_player1_location = nnew_player1_location
            new_player2_location = nnew_player2_location
            if args.desactivate_animations:
                player1_location = new_player1_location
                player2_location = new_player2_location

        logger.log(2, "Starting draw")

        ticking = pygame.time.get_ticks()
        turn_number = ticking // turn_time

        # Refresh hub and text only every turn
        if turn_number > old_turn_number:
            old_turn_number = turn_number
            # Blit the static images (maze floor)
            screen.blit(hub_image, (0, 0))

            draw_scores(
                [
                    PlayerScore(p1name, score1, moves1, miss1, stuck1, player1_is_alive),
                    PlayerScore(p2name, score2, moves2, miss2, stuck2, player2_is_alive),
                ],
                screen,
            )

        if not (q_info.empty()):
            text_info = q_info.get()
        if text_info != "":
            draw_text(text_info, (255, 255, 255), window_width, 40, window_width // 2, 5, screen)
        if pygame.time.get_ticks() - starting_time < args.preparation_time:
            remaining = args.preparation_time - pygame.time.get_ticks() + starting_time
            if remaining > 0:
                draw_text(
                    "Starting in " + str(remaining // 1000) + "." + (str(remaining % 1000)).zfill(3),
                    (255, 255, 255),
                    window_width,
                    40,
                    window_width // 2,
                    5,
                    screen,
                )

        maze_painter.draw_floor()

        # Draw explored cells
        if show_path:
            if player1_is_alive and player1_location not in player1_locations:
                player1_locations.add(player1_location)
                maze_painter.draw_explored_cell(player1_location, color=RAT_COLOR)

            if player2_is_alive and player2_location not in player2_locations:
                player2_locations.add(player2_location)
                maze_painter.draw_explored_cell(player2_location, color=PYTHON_COLOR)
        maze_painter.draw_walls()
        maze_painter.draw_pieces_of_cheese(pieces_of_cheese)

        if not (args.desactivate_animations):
            if time_to_go1 <= pygame.time.get_ticks() or player1_location == new_player1_location:
                player1_location = new_player1_location
                player1_draw_location = player1_location
            else:
                prop = (time_to_go1 - pygame.time.get_ticks()) / (maze[player1_location][new_player1_location] * turn_time)
                i, j = player1_location
                ii, jj = new_player1_location
                player1_draw_location = i * prop + ii * (1 - prop), j * prop + jj * (1 - prop)
            if time_to_go2 <= pygame.time.get_ticks() or player2_location == new_player2_location:
                player2_location = new_player2_location
                player2_draw_location = player2_location
            else:
                prop = (time_to_go2 - pygame.time.get_ticks()) / (maze[player2_location][new_player2_location] * turn_time)
                i, j = player2_location
                ii, jj = new_player2_location
                player2_draw_location = i * prop + ii * (1 - prop), j * prop + jj * (1 - prop)
        else:
            player1_draw_location = player1_location
            player2_draw_location = player2_location

        def rotation(old_loc, new_loc):
            if old_loc[1] < new_loc[1]:
                return 0
            if old_loc[1] > new_loc[1]:
                return 180
            if old_loc[0] < new_loc[0]:
                return 270
            if old_loc[0] > new_loc[0]:
                return 90
            return 0

        if player1_is_alive:
            rotation1 = rotation(old_player1_location, new_player1_location)
            maze_painter.draw_player(player1_draw_location, rotation1, "rat")
        if player2_is_alive:
            rotation2 = rotation(old_player2_location, new_player2_location)
            maze_painter.draw_player(player2_draw_location, rotation2, "sheep")

        available_width = window_width * 2 / 3
        available_height = window_height - 75

        maze_height = maze_painter.surface.get_height()
        maze_width = maze_painter.surface.get_width()

        scale = min(available_height / maze_height, available_width / maze_width)
        if scale > 1:
            scale = math.floor(scale)
        scaled_maze = pygame.transform.scale(maze_painter.surface, (int(maze_width * scale), int(maze_height * scale)))

        screen.blit(scaled_maze, ((window_width - scaled_maze.get_width()) / 2, 50 + (available_height - scaled_maze.get_height()) / 2))

        logger.log(2, "Drawing on screen")
        pygame.display.flip()
        if not (args.desactivate_animations):
            clock.tick(60)
        else:
            if not (args.synchronous):
                clock.tick(1000 / turn_time)
    logger.log(2, "Exiting rendering")
    q_render_in.put("quit")
    if is_human_python:
        q2_out.put("")
    if is_human_rat:
        q1_out.put("")
