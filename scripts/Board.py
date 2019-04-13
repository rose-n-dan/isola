from enum import Enum
from copy import deepcopy
import numpy as np
from itertools import product


WHITE_WINS = 100
BLACK_WINS = -100


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
        self.white_turn = True

    def move(self, move):
        player_color = self.board[move.start_row, move.start_col]
        self.board[move.end_row, move.end_col] = player_color
        self.board[move.start_row, move.start_col] = Cell.USED
        self.white_turn = not self.white_turn

    def undo_move(self, mv):
        tmp_mv = deepcopy(mv)
        tmp_mv.revert()
        self.move(tmp_mv)
        self.board[tmp_mv.start_row, tmp_mv.start_col] = Cell.EMPTY

    def find_checker_pos(self, color):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i, j] == color:
                    return (i, j)

    def find_possible_moves(self, pos):
        pos = (pos[0], pos[1])
        options = []
        for move in list(product((-1, 1), (-2, 2))) + list(product((-2, 2), (-1, 1))):
            option = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= option[0] < 7 and 0 <= option[1] < 7:
                if self.board[option] == Cell.EMPTY:
                    options.append(option)

        return options

    def eval_boardstate(self):
        white_moves = len(self.find_possible_moves(self.find_checker_pos(Cell.PLAYER_WHITE)))
        black_moves = len(self.find_possible_moves(self.find_checker_pos(Cell.PLAYER_BLACK)))

        if white_moves == 0:
            return BLACK_WINS
        elif black_moves == 0:
            return WHITE_WINS
        else:
            return white_moves - black_moves
