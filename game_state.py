from enum import Enum


class GameState(Enum):
    GAME_MENU = -1
    GAME_RUNNING = 0
    GAME_PAUSE = 1
    GAME_OVER = 2
