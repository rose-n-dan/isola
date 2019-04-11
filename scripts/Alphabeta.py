from scripts.Move import Move
from scripts.Board import Cell

WHITE_WINS = 100
BLACK_WINS = -100


def alphabeta(board, depth, alpha, beta):
    heuristic_value = board.eval_boardstate()

    print("Heuristic value: {}".format(heuristic_value))

    if depth == 0 or \
            heuristic_value == WHITE_WINS or heuristic_value == BLACK_WINS:  # terminal state - game ended
        return heuristic_value, None

    best_move = None

    if board.white_turn:
        ret_value = BLACK_WINS - 1
        for move in board.find_possible_moves(board.find_checker_pos(Cell.PLAYER_WHITE)):
            mv = Move(board.find_checker_pos(Cell.PLAYER_WHITE)[0],
                      board.find_checker_pos(Cell.PLAYER_WHITE)[1],
                      move[0],
                      move[1])

            print('The move is: {}'.format(mv))

            board.move(mv)

            print(board.board)

            new_ret_value = max(ret_value,
                                alphabeta(board, depth - 1, alpha, beta)[0])

            if new_ret_value > ret_value:
                best_move = mv
                ret_value = new_ret_value

            alpha = max(alpha, ret_value)

            # undo moving
            board.undo_move(mv)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return ret_value, best_move

    elif not board.white_turn:
        ret_value = WHITE_WINS + 1
        for move in board.find_possible_moves(board.find_checker_pos(Cell.PLAYER_BLACK)):
            mv = Move(board.find_checker_pos(Cell.PLAYER_BLACK)[0],
                      board.find_checker_pos(Cell.PLAYER_BLACK)[1],
                      move[0],
                      move[1])
            print('The move is: {}'.format(mv))

            board.move(mv)

            print(board.board)

            new_ret_value = min(ret_value,
                                alphabeta(board, depth - 1, alpha, beta)[0])

            if new_ret_value < ret_value:
                best_move = mv
                ret_value = new_ret_value

            beta = min(beta, ret_value)

            # undo moving
            board.undo_move(mv)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return ret_value, best_move