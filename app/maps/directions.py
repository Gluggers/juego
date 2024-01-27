from enum import Enum


class CardinalDirection(Enum):
    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x3
    WEST = 0x4


class MovementDirection(Enum):
    MOVE_UP = 0x1
    MOVE_RIGHT = 0x2
    MOVE_DOWN = 0x3
    MOVE_LEFT = 0x4
