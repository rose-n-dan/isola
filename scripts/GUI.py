from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from scripts.Board import Board, Cell


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
                if board.board[i, j] == Cell.PLAYER_WHITE:
                    self.pos = Vector(250*j, 100*i+30)
                elif board.board[i, j] == Cell.PLAYER_BLACK:
                    self.pos = Vector(20*j, 200*i)


class IsolaGame(Screen):
    board = Board()
    checkerB = ObjectProperty(None)
    checkerW = ObjectProperty(None)

    def start_game(self):
        self.checkerB.center = self.center
        self.checkerW.center = self.center

    def update(self, dt):
        self.checkerB.move(self.board)
        self.checkerW.move(self.board)

    def on_touch_move(self, touch):
        if self.checkerW.pos == touch.pos:
            self.checkerW.pos = touch.pos
        if self.checkerB.pos == touch.pos:
            self.checkerB.pos = touch.pos


class IsolaApp(App):
    def build(self):
        return kv

        game = IsolaGame()
        game.start_game()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


kv = Builder.load_file("Isola.kv")


if __name__ == '__main__':
    IsolaApp().run()
