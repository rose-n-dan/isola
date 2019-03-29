from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from scripts.Board import Board, Cell


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
    pass

    # def move(self, board):
    #     for i in range(7):
    #         for j in range(7):
    #             if board.board[i, j] == Cell.PLAYER_WHITE:
    #                 self.pos = Vector(450*j, 100*i+30)
    #             elif board.board[i, j] == Cell.PLAYER_BLACK:
    #                 self.pos = Vector(20*j, 200*i)


class IsolaGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        self.checkerB = ObjectProperty(Checker())
        self.checkerW = ObjectProperty(Checker())

    def start_game(self):
        self.checkerB.center = self.center
        self.checkerW.center = self.center

    def update(self, dt):
        self.checkerB.move(self.board)
        self.checkerW.move(self.board)

    def on_touch_down(self, touch):
        print('Touch pos: {}'.format(touch))
        print('Self.pos: {}'.format(self.checkerB.pos))
        if self.checkerB.collide_point(*touch.pos):
            print('OK')


class IsolaApp(App):

    def build(self):
        kv = Builder.load_file("Isola.kv")
        return kv

    def on_start(self):
        pass


if __name__ == '__main__':
    IsolaApp().run()
