from enum import Enum
import numpy as np
from itertools import product

from scripts.Move import Move


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
        print(player_color, move.start_row, move.start_col)

        self.board[move.end_row, move.end_col] = player_color
        self.board[move.start_row, move.start_col] = Cell.EMPTY

        self.is_white_turn = not self.is_white_turn

    def find(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i, j] == Cell.PLAYER_WHITE:
                    pass

    def find_possible_moves(self, pos):
        pos = (pos[0], pos[1])
        options = []
        for move in list(product((-1, 1), (-2, 2))) + list(product((-2, 2), (-1, 1))):
            option = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= option[0] < 7 and 0 <= option[1] < 7:
                if self.board[option] == Cell.EMPTY:
                    options.append(option)

        return options
