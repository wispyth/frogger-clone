from enum import Enum, auto

class Direction(int, Enum):
    LEFT  = -1
    RIGHT = +1

class Facing(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()

class GameState(Enum):
    START     = auto()
    PLAYING   = auto()
    PAUSED    = auto()
    GAME_OVER = auto()
    WIN       = auto()
