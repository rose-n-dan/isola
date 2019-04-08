from enum import Enum
from copy import deepcopy
import numpy as np
from itertools import product

from scripts.Move import Move


WHITE_WINS = 100
BLACK_WINS = -100

MAX_DEPTH = 4


class Cell(Enum):
    PLAYER_WHITE = 'W'
    PLAYER_BLACK = 'B'
    EMPTY = '_'
    USED = 'x'

    def __repr__(self):
        return self.value


class Board:

    class GameState(Enum):
        WHITE_MOVES = 'w'
        WHITE_CHOOSES = 'wc'
        BLACK_MOVES = 'b'
        BLACK_CHOOSES = 'bc'

        def __repr__(self):
            return self.value

    def __init__(self):
        self.board = np.full((7, 7), Cell.EMPTY)
        self.board[0, 3] = Cell.PLAYER_WHITE
        self.board[6, 3] = Cell.PLAYER_BLACK
        self.game_state = self.GameState.WHITE_MOVES

    def move(self, move):
        player_color = self.board[move.start_row, move.start_col]
        print(player_color, move.start_row, move.start_col)

        self.board[move.end_row, move.end_col] = player_color
        self.board[move.start_row, move.start_col] = Cell.EMPTY

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


def minmax(board, depth):
    heuristic_value = board.eval_boardstate()

    if depth == MAX_DEPTH or \
       heuristic_value == WHITE_WINS or heuristic_value == BLACK_WINS: # terminal state - game ended
        return heuristic_value, _

    best_move = None

    if board.game_state == board.GameState.WHITE_MOVES:
        ret_value = BLACK_WINS - 1
        for move in board.find_possible_moves(board.find_checker_pos(Cell.PLAYER_WHITE)):
            mv = Move(board.find_checker_pos(Cell.PLAYER_WHITE)[0],
                      board.find_checker_pos(Cell.PLAYER_WHITE)[1],
                      move[0],
                      move[1])
            board.move(mv)
            for i in range(7):
                for j in range(7):
                    if board.board[i, j] == Cell.EMPTY:
                        board.board[i, j] = Cell.USED
                        board.game_state = board.GameState.BLACK_MOVES
                        new_ret_value = max(ret_value,
                                        minmax(board, depth - 1))
                        if new_ret_value > ret_value:
                            best_move = mv
                        ret_value = new_ret_value
                        # undo choosing
                        board.game_state = board.GameState.WHITE_MOVES
                        board[i, j] = Cell.EMPTY
            # undo moving
            board.move(mv.undo())
        return ret_value, best_move

    elif board.game_state == board.GameState.BLACK_MOVES:
        ret_value = WHITE_WINS + 1
        for move in board.find_possible_moves(board.find_checker_pos(Cell.PLAYER_BLACK)):
            mv = Move(board.find_checker_pos(Cell.PLAYER_BLACK)[0],
                      board.find_checker_pos(Cell.PLAYER_BLACK)[1],
                      move[0],
                      move[1])
            board.move(mv)
            for i in range(7):
                for j in range(7):
                    if board.board[i, j] == Cell.EMPTY:
                        board.board[i, j] = Cell.USED
                        board.game_state = board.GameState.WHITE_MOVES
                        ret_value = min(ret_value,
                                        minmax(board, depth - 1))
                        # undo choosing
                        board.game_state = board.GameState.BLACK_MOVES
                        board[i, j] = Cell.EMPTY
            # undo moving
            board.move(mv.undo())
        return ret_value
