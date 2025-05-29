from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty
#from gleslottie import Lottie
from androidlottie4kivy import GLLottie


class MainClass(BoxLayout):
    _tex = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyApp(App):

    def build(self):

        return MainClass()


if __name__ == "__main__":

    MyApp().run()
