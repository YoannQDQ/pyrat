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
import random
import sys
from functools import lru_cache

import pygame

from pyrat.core.parameters import args

logger = logging.getLogger("display")

# Yellow color for python
PYTHON_COLOR = (255, 255, 0)
# Brownish color for rat
RAT_COLOR = (165, 42, 42)


@lru_cache(maxsize=128)
def image(path, scalex, scaley):
    return pygame.transform.smoothscale(pygame.image.load(path), (scalex, scaley))


class Blitter:
    def __init__(self, screen, offset_x, offset_y, scale, window_height):
        self.screen = screen
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale = scale
        self.window_height = window_height

    def draw_image(self, path, i, j):
        self.draw_tile(image(path, self.scale, self.scale), i, j)

    def draw_tile(self, surface, i, j):
        self.screen.blit(surface, (self.offset_x + self.scale * i, self.window_height - self.offset_y - self.scale * (j + 1)))


def image_of_maze(maze, blitter):
    last_cell = list(maze.keys())[-1]
    width = last_cell[0] + 1
    height = last_cell[1] + 1
    image_wall = image("resources/gameElements/wall.png", blitter.scale, blitter.scale)
    image_corner = image("resources/gameElements/corner.png", blitter.scale, blitter.scale)
    image_mud = image("resources/gameElements/mud.png", blitter.scale, blitter.scale)
    image_tiles = [image(f"resources/gameElements/tile{i}.png", blitter.scale, blitter.scale) for i in range(1, 11)]

    # Draw floor
    for i in range(width):
        for j in range(height):
            blitter.draw_tile(random.choice(image_tiles), i, j)
    # Draw walls and mud
    for i in range(width):
        for j in range(height):
            if (i - 1, j) not in maze[(i, j)]:
                blitter.draw_tile(image_wall, i, j)
            elif maze[(i, j)][(i - 1, j)] > 1:
                blitter.draw_tile(image_mud, i, j)
            if (i + 1, j) not in maze[(i, j)]:
                blitter.draw_tile(pygame.transform.rotate(image_wall, 180), i, j)

            elif maze[(i, j)][(i + 1, j)] > 1:
                blitter.draw_tile(pygame.transform.rotate(image_mud, 180), i, j)

            if (i, j + 1) not in maze[(i, j)]:
                blitter.draw_tile(pygame.transform.rotate(image_wall, 270), i, j)

            elif maze[(i, j)][(i, j + 1)] > 1:
                blitter.draw_tile(pygame.transform.rotate(image_mud, 270), i, j)
            if (i, j - 1) not in maze[(i, j)]:
                blitter.draw_tile(pygame.transform.rotate(image_wall, 90), i, j)
            elif maze[(i, j)][(i, j - 1)] > 1:
                blitter.draw_tile(pygame.transform.rotate(image_mud, 90), i, j)

    # Draw Borders
    for i in range(width):
        blitter.draw_tile(pygame.transform.rotate(image_wall, 270), i, -1)
        blitter.draw_tile(pygame.transform.rotate(image_wall, 90), i, height)
    for j in range(height):
        blitter.draw_tile(image_wall, 0, j)
        blitter.draw_tile(pygame.transform.rotate(image_wall, 180), width - 1, j)

    # Draw corners
    for i in range(width + 1):
        for j in range(height + 1):
            blitter.draw_tile(image_corner, i, j - 1)
            blitter.draw_tile(pygame.transform.rotate(image_corner, 90), i, j)
            blitter.draw_tile(pygame.transform.rotate(image_corner, 180), i - 1, j)
            blitter.draw_tile(pygame.transform.rotate(image_corner, 270), i - 1, j - 1)


def draw_pieces_of_cheese(pieces_of_cheese, blitter: Blitter):
    for i, j in pieces_of_cheese:
        blitter.draw_image("resources/gameElements/cheese.png", i, j)


def draw_explored_cells(seen_locations, blitter: Blitter, color):
    # Create semi-transparent solid color surface
    seen_cell = pygame.Surface((blitter.scale, blitter.scale))
    seen_cell.set_alpha(50)  # Set transparency level (0-255)
    seen_cell.fill(color)  # Fill with color

    for i, j in seen_locations:
        blitter.draw_tile(seen_cell, i, j)


def draw_players(player1_location, player2_location, blitter: Blitter, rotation1, rotation2):
    rat = image("resources/gameElements/movingRat.png", blitter.scale, blitter.scale)
    rat = pygame.transform.rotate(rat, rotation1)
    blitter.draw_tile(rat, *player1_location)

    python = image("resources/gameElements/movingPython.png", blitter.scale, blitter.scale)
    python = pygame.transform.rotate(python, rotation2)
    blitter.draw_tile(python, *player2_location)


font_sizes = [50, 25, 50, 25, 50, 50, 50]


def draw_text(text, color, max_size, index_size, x, y, screen):
    font = pygame.font.SysFont("monospace", font_sizes[index_size])
    label = font.render(text, 1, color)
    while label.get_rect().width > max_size:
        font_sizes[index_size] = font_sizes[index_size] - 1
        font = pygame.font.SysFont("monospace", font_sizes[index_size])
        label = font.render(text, 1, color)
    pygame.draw.rect(screen, (0, 0, 0), (x - label.get_rect().width // 2, y, label.get_rect().width, label.get_rect().height))
    screen.blit(label, (x - label.get_rect().width // 2, y))


def draw_scores(
    p1name,
    score1,
    p2name,
    score2,
    window_width,
    window_height,
    screen,
    player1_is_alive,
    player2_is_alive,
    moves1,
    miss1,
    moves2,
    miss2,
    stuck1,
    stuck2,
):
    if player1_is_alive:
        draw_text(
            "Score: " + str(score1),
            (255, 255, 255),
            window_width / 6,
            0,
            int(window_width / 12),
            window_width / 3 + 50,
            screen,
        )
        draw_text(p1name, (255, 255, 255), window_width / 6, 5, int(window_width / 12), window_width / 3, screen)
        draw_text(
            "Moves: " + str(moves1),
            (0, 255, 0),
            window_width / 6,
            1,
            int(window_width / 12),
            window_width / 3 + 150,
            screen,
        )
        draw_text(
            "Miss: " + str(miss1),
            (255, 0, 0),
            window_width / 6,
            1,
            int(window_width / 12),
            window_width / 3 + 180,
            screen,
        )
        draw_text(
            "Mud: " + str(stuck1),
            (255, 0, 0),
            window_width / 6,
            1,
            int(window_width / 12),
            window_width / 3 + 210,
            screen,
        )
    if player2_is_alive:
        draw_text(
            "Score: " + str(score2),
            (255, 255, 255),
            window_width / 6,
            2,
            int(11 * window_width / 12),
            window_width / 3 + 50,
            screen,
        )
        draw_text(p2name, (255, 255, 255), window_width / 6, 6, int(11 * window_width / 12), window_width / 3, screen)
        draw_text(
            "Moves: " + str(moves2),
            (0, 255, 0),
            window_width / 6,
            3,
            int(11 * window_width / 12),
            window_width / 3 + 150,
            screen,
        )
        draw_text(
            "Miss: " + str(miss2),
            (255, 0, 0),
            window_width / 6,
            3,
            int(11 * window_width / 12),
            window_width / 3 + 180,
            screen,
        )
        draw_text(
            "Mud: " + str(stuck2),
            (255, 0, 0),
            window_width / 6,
            3,
            int(11 * window_width / 12),
            window_width / 3 + 210,
            screen,
        )


def display_exit():
    pygame.quit()


def play(q_out, move):
    while not q_out.empty():
        q_out.get()
    q_out.put(move)


def load_image(path, scale_x, scale_y):
    return pygame.transform.smoothscale(pygame.image.load(path), (scale_x, scale_y))


def init_coords_and_images(width, height, window_width, window_height):
    scale = int(min((window_height - 50) / height, window_width * 2 / 3 / width))
    offset_x = window_width // 2 - int(width / 2 * scale)
    offset_y = max(25, window_height // 2 - int(scale * height / 2))
    scale_portrait_w = int(window_width / 6)
    scale_portrait_h = int(window_width / 6 * 800 / 541)

    def load_img(path):
        return load_image(path, scale, scale)

    image_portrait_python = load_image("resources/illustrations/python_left.png", scale_portrait_w, scale_portrait_h)
    image_portrait_rat = load_image("resources/illustrations/rat.png", scale_portrait_w, scale_portrait_h)

    return (scale, offset_x, offset_y, image_portrait_python, image_portrait_rat)


def build_background(
    screen,
    maze,
    offset_x,
    offset_y,
    window_width,
    window_height,
    image_portrait_rat,
    image_portrait_python,
    scale,
    player1_is_alive,
    player2_is_alive,
):
    screen.fill((0, 0, 0))
    maze_image = screen.copy()
    blitter = Blitter(maze_image, offset_x, offset_y, scale, window_height)
    image_of_maze(maze, blitter)

    if player1_is_alive:
        maze_image.blit(image_portrait_rat, (int(window_width / 12 - image_portrait_python.get_rect().width / 2), 15))
    if player2_is_alive:
        maze_image.blit(image_portrait_python, (int(window_width * 11 / 12 - image_portrait_python.get_rect().width / 2), 15))
    return maze_image


def run(
    maze,
    width,
    height,
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
    screen,
    infoObject,
):
    logger.log(2, "Starting rendering")
    window_width, window_height = pygame.display.get_surface().get_size()
    turn_time = args.turn_time
    (scale, offset_x, offset_y, image_portrait_python, image_portrait_rat) = init_coords_and_images(width, height, window_width, window_height)

    logger.log(2, "Defining constants")
    clock = pygame.time.Clock()
    new_player1_location = player1_location
    new_player2_location = player2_location
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
    maze_image = build_background(
        screen,
        maze,
        offset_x,
        offset_y,
        window_width,
        window_height,
        image_portrait_rat,
        image_portrait_python,
        scale,
        player1_is_alive,
        player2_is_alive,
    )

    starting_time = pygame.time.get_ticks()

    text_info = ""

    player1_locations = set()
    player2_locations = set()

    logger.log(2, "Starting main loop")
    while q_quit.empty():
        logger.log(2, "Checking events")
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                q_quit.put("sortir")
                # pygame.quit()
                break
            if event.type == pygame.VIDEORESIZE or (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
                if event.type == pygame.KEYDOWN and not (screen.get_flags() & 0x80000000):
                    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
                    window_width, window_height = infoObject.current_w, infoObject.current_h
                else:
                    if event.type == pygame.VIDEORESIZE:
                        window_width, window_height = event.w, event.h
                    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                (scale, offset_x, offset_y, image_portrait_python, image_portrait_rat) = init_coords_and_images(
                    width, height, window_width, window_height
                )
                maze_image = build_background(
                    screen,
                    maze,
                    offset_x,
                    offset_y,
                    window_width,
                    window_height,
                    image_portrait_rat,
                    image_portrait_python,
                    scale,
                    player1_is_alive,
                    player2_is_alive,
                )

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
        # if not(q_quit.empty()):
        #    break
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
        screen.fill((0, 0, 0))
        screen.blit(maze_image, (0, 0))

        blitter = Blitter(screen, offset_x, offset_y, scale, window_height)

        # Draw explored cells
        if show_path:
            if player1_is_alive:
                if new_player1_location not in player1_locations:
                    player1_locations.add(new_player1_location)
                draw_explored_cells(player1_locations, blitter, color=RAT_COLOR)

            if player2_is_alive:
                if new_player2_location not in player2_locations:
                    player2_locations.add(new_player2_location)

                draw_explored_cells(player2_locations, blitter, color=PYTHON_COLOR)

        draw_pieces_of_cheese(pieces_of_cheese, blitter)
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

        rotation1 = rotation(old_player1_location, new_player1_location)
        rotation2 = rotation(old_player2_location, new_player2_location)

        draw_players(player1_draw_location, player2_draw_location, blitter, rotation1, rotation2)

        draw_scores(
            p1name,
            score1,
            p2name,
            score2,
            window_width,
            window_height,
            screen,
            player1_is_alive,
            player2_is_alive,
            moves1,
            miss1,
            moves2,
            miss2,
            stuck1,
            stuck2,
        )
        if not (q_info.empty()):
            text_info = q_info.get()
        if text_info != "":
            draw_text(text_info, (255, 255, 255), window_width, 4, window_width // 2, 25, screen)
        if pygame.time.get_ticks() - starting_time < args.preparation_time:
            remaining = args.preparation_time - pygame.time.get_ticks() + starting_time
            if remaining > 0:
                draw_text(
                    "Starting in " + str(remaining // 1000) + "." + (str(remaining % 1000)).zfill(3),
                    (255, 255, 255),
                    window_width,
                    4,
                    window_width // 2,
                    25,
                    screen,
                )

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
