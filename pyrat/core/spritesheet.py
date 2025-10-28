from functools import cache

import pygame


@cache
def sheet(filename):
    return pygame.image.load(filename).convert()


@cache
def image_at(filename, rectangle, colorkey=None):
    rect = pygame.Rect(rectangle)
    source = sheet(filename)
    image = pygame.Surface(rect.size).convert()
    image.blit(source, (0, 0), rect)
    image.set_colorkey(colorkey)
    return image
