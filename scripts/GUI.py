import kivy.properties
from kivy.app import App
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget

from scripts.Board import Board, Cell


class Checker(Widget):
    obj = Board()

    def move(self):
        for i in range(7):
            for j in range(7):
                if self.obj.board[i, j] == Cell.PLAYER_WHITE:
                    self.pos = Vector(250*j, 100*i+30)
                elif self.obj.board[i, j] == Cell.PLAYER_BLACK:
                    self.pos = Vector(20*j, 100*i)




class IsolaGame(Widget):
    checkerB = kivy.properties.ObjectProperty(None)
    checkerW = kivy.properties.ObjectProperty(None)

    def start_game(self):
        self.checkerB.center = self.center
        self.checkerW.center = self.center

    def update(self, dt):
        self.checkerB.move()
        self.checkerW.move()


class IsolaApp(App):
    def build(self):
        game = IsolaGame()
        game.start_game()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    IsolaApp().run()
