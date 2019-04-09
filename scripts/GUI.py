#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import *
from kivy.clock import Clock

from scripts.Board import Board, Cell, minmax
from scripts.Move import Move

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
Config.write()


def cell_to_pixel(pos):
    return (Window.size[0] * (pos[1] / 7),
            (Window.size[1] * 6 / 7) - (Window.size[1] * pos[0] / 7))


def pixel_to_cell(pos):
    return (6 - int(pos[1] // (Window.size[0] / 7)),
            int(pos[0] // (Window.size[1] / 7)))


def get_cell_size():
    return (Window.size[0] / 7,
            Window.size[1] / 7)


class IsolaWindow(Screen):
    pass


class MainWindow(Screen):
    pass


class OptionWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class GameTypeWindow(Screen):
    pass


class Checker(Widget):

    def move(self, board):
        for i in range(7):
            for j in range(7):
                if board.board[i, j] == self.color:
                    self.pos = cell_to_pixel((i, j))


class IsolaGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.board = Board()
        # self.checkers declared in .kv

        # temporary - for each move
        self.current_options = []
        self.current_options_canvas = []
        self.starting_cell = None

        self.used_cells_canvas = []

        self.is_black_ai = True
        self.is_white_ai = False
        self.depth = 4
        self.game_started = False

    def start_game(self):
        self.checkers[self.board.white_turn].move(self.board)
        self.checkers[not self.board.white_turn].move(self.board)

    def update(self, dt):
        if self.game_started and ((self.is_black_ai and not self.board.white_turn) or
                                  (self.is_white_ai and self.board.white_turn)):
            Clock.usleep(500000)
            ret_val, move = minmax(self.board, self.depth)
            print(ret_val, move)
            self.move_current_checker(move)
            print(self.board.board)

    def move_current_checker(self, mv):
        # move the checker on the board
        self.board.move(mv)
        # then move its canvas
        self.checkers[not self.board.white_turn].pos = cell_to_pixel((mv.end_row, mv.end_col))
        # and paint square on used cell
        with self.canvas:
            Color(1, 0, 0, 0.6)
            self.used_cells_canvas.append(Rectangle(pos=cell_to_pixel((mv.start_row, mv.start_col)),
                                                    size=get_cell_size()))

    def on_touch_down(self, touch):
        if self.checkers[self.board.white_turn].collide_point(*touch.pos):
            self.starting_cell = pixel_to_cell(touch.pos)
            cell = pixel_to_cell(touch.pos)
            self.current_options = self.board.find_possible_moves(cell)
            with self.canvas:
                Color(0, 1, 0, .6)
                for option in self.current_options:
                    self.current_options_canvas.append(Rectangle(pos=cell_to_pixel(option),
                                                                 size=get_cell_size()))

    def on_touch_move(self, touch):
        if self.starting_cell is not None:
            self.checkers[self.board.white_turn].pos[0] += touch.dx
            self.checkers[self.board.white_turn].pos[1] += touch.dy

    def on_touch_up(self, touch):
        # if right checker was touched down and it is touched up on available square
        if self.starting_cell is not None and pixel_to_cell(touch.pos) in self.current_options:
            # prepare move
            current_pos = (self.starting_cell[0], self.starting_cell[1])
            ending_pos = pixel_to_cell(touch.pos)
            move = Move(current_pos[0], current_pos[1],
                        ending_pos[0], ending_pos[1])

            self.move_current_checker(move)

        # if right checker was touched down and it is touched up on unavailable square
        # move it on its starting square
        elif self.starting_cell is not None:
            self.checkers[self.board.white_turn].pos = cell_to_pixel(self.starting_cell)

        # remove all the leftovers
        for rectangle in self.current_options_canvas:
            self.canvas.remove(rectangle)
        self.current_options_canvas.clear()
        self.starting_cell = None


class IsolaApp(App):

    def build(self):
        kv = Builder.load_file("Isola.kv")
        return kv

    def on_start(self):
        self.root.ids.iw.ids.ig.start_game()
        Clock.schedule_interval(self.root.ids.iw.ids.ig.update, 1.0 / 60.0)

        # SHOWCASE
        # b = Board()
        # b.board[5, 1] = Cell.USED
        # b.board[5, 5] = Cell.USED
        # b.board[4, 2] = Cell.USED
        # b.board[0, 3] = Cell.EMPTY
        # b.board[1, 0] = Cell.PLAYER_WHITE
        # # print(b.board)
        # b.board[5, 2] = Cell.USED
        # b.board[3, 2] = Cell.USED
        # b.board[2, 5] = Cell.USED
        # b.board[3, 6] = Cell.USED
        # b.board[5, 6] = Cell.USED
        # b.board[6, 5] = Cell.USED
        # b.board[0, 2] = Cell.USED
        #
        # # b.board[4, 4] = Cell.PLAYER_BLACK
        # # b.board[6, 3] = Cell.USED
        #
        # ret_val, mv = minmax(b, 3)
        # print("WINNING heuristic value: {}, move: {}".format(ret_val, mv))
        # b.move(mv)
        # print(b.board)


if __name__ == '__main__':
    IsolaApp().run()
