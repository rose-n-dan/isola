from enum import Enum

from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.button import Button

from scripts.Board import Board, Cell
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

    class GameState(Enum):
        WHITE_MOVES = 'w'
        WHITE_CHOOSES = 'wc'
        BLACK_MOVES = 'b'
        BLACK_CHOOSES = 'bc'

        def __repr__(self):
            return self.value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = self.GameState.WHITE_MOVES
        self.board = Board()
        self.moves = []
        self.current_options = []
        self.starting_cell = None

    def start_game(self):
        self.checkers['w'].move(self.board)
        self.checkers['b'].move(self.board)

    def update(self, dt):
        pass

    def on_touch_down(self, touch):
        print(self.board.board)
        if self.game_state == self.GameState.WHITE_MOVES or self.game_state == self.GameState.BLACK_MOVES:
            if self.checkers[self.game_state.value].collide_point(*touch.pos):
                self.starting_cell = pixel_to_cell(touch.pos)
                cell = pixel_to_cell(touch.pos)
                print(touch.pos, cell)
                self.current_options = self.board.find_possible_moves(cell)
                with self.canvas:
                    Color(0, 1, 0, .6)
                    for option in self.current_options:
                        self.moves.append(Rectangle(pos=cell_to_pixel(option),
                                                    size=get_cell_size()))

    def on_touch_move(self, touch):
        if self.starting_cell is not None:
            self.checkers[self.game_state.value].pos[0] += touch.dx
            self.checkers[self.game_state.value].pos[1] += touch.dy

    def on_touch_up(self, touch):
        # if game_state is MOVE
        if self.game_state == self.GameState.WHITE_MOVES or self.game_state == self.GameState.BLACK_MOVES:
            # if right checker was touched down and it is touched up on available square
            if self.starting_cell is not None and pixel_to_cell(touch.pos) in self.current_options:
                # prepare move
                current_pos = (self.starting_cell[0], self.starting_cell[1])
                ending_pos = pixel_to_cell(touch.pos)
                move = Move(current_pos[0], current_pos[1],
                            ending_pos[0], ending_pos[1])
                # move the checker on the board
                self.board.move(move)
                # then move its canvas
                self.checkers[self.game_state.value].pos = cell_to_pixel(ending_pos)

                # changing game_state to <same_player>_CHOOSES
                if self.game_state == self.GameState.WHITE_MOVES:
                    self.game_state = self.GameState.WHITE_CHOOSES
                elif self.game_state == self.GameState.BLACK_MOVES:
                    self.game_state = self.GameState.BLACK_CHOOSES

            # if right checker was touched down and it is touched up on unavailable square
            # move it on its starting square
            elif self.starting_cell is not None:
                self.checkers[self.game_state.value].pos = cell_to_pixel(self.starting_cell)

            # remove all the leftovers
            for rectangle in self.moves:
                self.canvas.remove(rectangle)
            self.moves.clear()
            self.starting_cell = None

        # if game_state is CHOOSE
        elif self.game_state == self.GameState.WHITE_CHOOSES or self.game_state == self.GameState.BLACK_CHOOSES:
            if self.board.board[pixel_to_cell(touch.pos)] == Cell.EMPTY:
                self.board.board[pixel_to_cell(touch.pos)] = Cell.USED

                with self.canvas:
                    Color(1, 0, 0, .6)
                    Rectangle(pos=cell_to_pixel(pixel_to_cell(touch.pos)),
                              size=get_cell_size())

                # changing game_state to <opposite_player>_CHOOSES
                if self.game_state == self.GameState.WHITE_CHOOSES:
                    self.game_state = self.GameState.BLACK_MOVES
                if self.game_state == self.GameState.BLACK_CHOOSES:
                    self.game_state = self.GameState.WHITE_MOVES


class IsolaApp(App):

    def build(self):
        kv = Builder.load_file("Isola.kv")
        return kv

    def on_start(self):
        self.root.ids.iw.ids.ig.start_game()
        Clock.schedule_interval(self.root.ids.iw.ids.ig.update, 1.0 / 60.0)


if __name__ == '__main__':
    IsolaApp().run()
