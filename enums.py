from enum import Enum, auto

class Direction(int, Enum):
    LEFT  = -1
    RIGHT = +1

class GameState(Enum):
    PLAYING   = auto()
    GAME_OVER = auto()
    WIN       = auto()
