from enum import Enum
import numpy as np

from Move import Move


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

        self.is_white_turn = True

    def move(self, move):
        player_color = self.board[move.start_row, move.start_col]

        if player_color != Cell.PLAYER_WHITE and player_color != Cell.PLAYER_BLACK:
            raise IOError('Starting cell is not a player cell!')
        elif self.is_white_turn and player_color != Cell.PLAYER_WHITE:
            raise IOError('It\'s white turn - move white checker')
        elif not self.is_white_turn and player_color != Cell.PLAYER_BLACK:
            raise IOError('It\'s black turn - move black checker')

        if not move.is_L_shape():
            raise IOError('Move is not L shape!')

        self.board[move.end_row, move.end_col] = player_color
        self.board[move.start_row, move.start_col] = Cell.USED

        self.is_white_turn = not self.is_white_turn

