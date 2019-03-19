from enum import Enum
import numpy as np


class Cell(Enum):
    PLAYER_WHITE = 'W'
    PLAYER_BLACK = 'B'
    EMPTY = '_'
    USED = 'x'

    def __repr__(self):
        return self.value


class Board:
    def __init__(self):
        self.board = np.full((7, 7), Cell.EMPTY)
        self.board[0, 3] = Cell.PLAYER_WHITE
        self.board[6, 3] = Cell.PLAYER_BLACK


b = Board()
print(b.board)
