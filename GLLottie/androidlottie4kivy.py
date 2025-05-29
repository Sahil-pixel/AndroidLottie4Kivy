# PEP8 formatted
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.properties import (ObjectProperty, ListProperty,
                             BooleanProperty, StringProperty)
from gleslottie import Lottie
import os


class GLLottie(Image):
    file_path = StringProperty('')
    _lottie = None

    def __init__(self, **kwargs):
        super(GLLottie, self).__init__(**kwargs)
        # self._lottie=Lottie()
        # f=os.path.join(os.getcwd(),"work2.json")
        # self._lottie.set_file(f)
        # self._lottie.bind(on_loaded=self.loaded)
        # self._lottie.bind(on_update=self._update)
        # self.file_path=os.path.join(os.getcwd(),"work2.json")

    def _update(self, obj,):
        # if self._lottie:
        self.texture = self._lottie._texture
        self.texture_size = list(self.texture.size)
        self.canvas.ask_update()

    def set_file(self, filepath):
        self._lottie.set_file(filepath)

    def loaded(self, *args):
        #print("loadede =====")
        self._lottie._play()

    def play(self):
        self._lottie._play()

    def pause(self):
        self._lottie._pause()

    def stop(self):
        self._lottie._stop()

    def on_file_path(self, obj, filepath):
        # print(filepath)
        if self._lottie:
            self._lottie.unbind(on_loaded=self.loaded)
            self._lottie.unbind(on_update=self._update)

            self._lottie. _clear_surface()
            self._lottie._clear()
            self._lottie._release2()
            # self._lottie._release()
            del self._lottie
            self._lottie = None
            self.texture = None
            # self.canvas.clear()
            self.canvas.ask_update()

        self._lottie = Lottie()
        self._lottie.bind(on_loaded=self.loaded)
        self._lottie.bind(on_update=self._update)
        self._lottie.set_file(filepath)
