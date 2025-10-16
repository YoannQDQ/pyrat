import random

from bots.utils import MOVE_E, MOVE_N, MOVE_O, MOVE_S


def go(*args):
    return random.choice([MOVE_N, MOVE_S, MOVE_O, MOVE_E])
