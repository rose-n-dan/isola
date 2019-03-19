from kivy.app import App
from kivy.uix.widget import Widget


class IsolaGame(Widget):
    pass


class IsolaApp(App):
    def build(self):
        return IsolaGame()


if __name__ == '__main__':
    IsolaApp().run()
