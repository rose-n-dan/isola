import kivy.properties
from kivy.app import App
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import kivy.graphics
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from scripts.Board import Board, Cell


class MainWindow(Screen):
    pass


class OptionWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Checker(Widget):
    game_board = Board()

    def move(self):
        for i in range(7):
            for j in range(7):
                if self.game_board.board[i, j] == 'W':
                    self.pos = Vector(250*j, 100*i+30)
                elif self.game_board.board[i, j] == 'B':
                    self.pos = Vector(20*j, 200*i)


class IsolaGame(Screen):
    board = Board()
    checkerB = kivy.properties.ObjectProperty(None)
    checkerW = kivy.properties.ObjectProperty(None)

    def start_game(self):
        self.checkerB.center = self.center
        self.checkerW.center = self.center

    def update(self, dt):
        self.checkerB.move()
        self.checkerW.move()

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
