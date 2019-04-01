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


def cell_to_pixel(pos):
    return (Window.size[0] * (pos[0] / 7),
            Window.size[1] * (pos[1] / 7))


def pixel_to_cell(pos):
    return (int(pos[0] // (Window.size[0] / 7)),
            int(pos[1] // (Window.size[1] / 7)))


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
                    self.pos = cell_to_pixel((j, i))


class IsolaGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        self.checkerB = ObjectProperty(Checker())
        self.checkerW = ObjectProperty(Checker())
        self.moves = []
        self.current_options = []
        self.starting_cell = None

    def start_game(self):
        self.checkerB.move(self.board)
        self.checkerW.move(self.board)

    def update(self, dt):
        # self.checkerB.move(self.board)
        # self.checkerW.move(self.board)
        pass

    def on_touch_down(self, touch):
        if self.checkerB.collide_point(*touch.pos):
            self.starting_cell = pixel_to_cell(touch.pos)
            cell = pixel_to_cell(touch.pos)
            self.current_options = self.board.find_possible_moves(cell)
            with self.canvas:
                Color(0, 1, 0, .4)
                for option in self.current_options:
                    self.moves.append(Rectangle(pos=cell_to_pixel(option),
                                                size=get_cell_size()))

    def on_touch_move(self, touch):
        self.checkerB.pos[0] += touch.dx
        self.checkerB.pos[1] += touch.dy

    def on_touch_up(self, touch):
        if pixel_to_cell(touch.pos) in self.current_options:
            current_pos = (self.starting_cell[0],
                           self.starting_cell[1])
            ending_pos = pixel_to_cell(touch.pos)
            move = Move(current_pos[1], current_pos[0],
                        ending_pos[1], ending_pos[0])
            self.board.move(move)
            self.checkerB.pos = cell_to_pixel(ending_pos)
        else:
            self.checkerB.pos = cell_to_pixel(self.starting_cell)

        for rectangle in self.moves:
            self.canvas.remove(rectangle)
        self.moves.clear()


class IsolaApp(App):

    def build(self):
        kv = Builder.load_file("Isola.kv")
        return kv

    def on_start(self):
        self.root.ids.iw.ids.ig.start_game()
        Clock.schedule_interval(self.root.ids.iw.ids.ig.update, 1.0 / 60.0)
        pass


if __name__ == '__main__':
    IsolaApp().run()
