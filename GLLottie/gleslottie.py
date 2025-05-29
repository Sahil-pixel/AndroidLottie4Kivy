# PEP8 formatted
from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread

from kivy.graphics.texture import Texture
from kivy.graphics import Fbo, Rectangle, Callback, ClearBuffers, ClearColor
from kivy.clock import Clock
from kivy.event import EventDispatcher
import os

GL_TEXTURE_EXTERNAL_OES = autoclass(
    'android.opengl.GLES11Ext').GL_TEXTURE_EXTERNAL_OES
SurfaceTexture = autoclass('android.graphics.SurfaceTexture')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
LottieRenderer = autoclass('org.kivy.lottie.LottieRenderer')


class LottieLoadListener(PythonJavaClass):
    __javainterfaces__ = ['org/kivy/lottie/OnLottieLoadListener']
    __javacontext__ = 'app'  # Required on Android

    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    @java_method('(Lcom/airbnb/lottie/LottieComposition;Z)V')
    def onLoaded(self, composition, loaded):
        print(f"Lottie loaded ? ", loaded)
        if self.callback:
            self.callback(loaded)

    @java_method('(Ljava/lang/Throwable;)V')
    def onFailed(self, exception):
        print("Failed to load Lottie:", exception.toString())


class Lottie(EventDispatcher):
    __events__ = ('on_loaded', 'on_update')
    _update_ev = None
    _texture = None
    _lottie = None
    _lottie_texture = None
    _surface_texture = None
    _fbo = None
    _texture_cb = None

    def __init__(self, width=512, height=512, fps=30, *args, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self._fps = fps

    def set_file(self, filepath=''):
        # self._release2()
        #file_path = os.path.join(os.getcwd(), 'work2.json')
        activity = PythonActivity.mActivity
        listener = LottieLoadListener(self._on_loaded)
        self._lottie = LottieRenderer(activity, listener)
        self._set_file(filepath)
        #(width, height) = width,height
        width, height = self.width, self.height
        self._resolution = (self.width, self.height)
        self._lottie_texture = Texture(width=width, height=height,
                                       target=GL_TEXTURE_EXTERNAL_OES,
                                       colorfmt='rgba')
        print(self._lottie_texture)

        self._surface_texture = SurfaceTexture(int(self._lottie_texture.id))
        self._surface_texture.setDefaultBufferSize(width, height)

        self._lottie.setSurfaceTexture(self._surface_texture)

        self._fbo = Fbo(size=self._resolution)
        self._fbo['resolution'] = (float(width), float(height))
        self._fbo.shader.fs = '''
                #extension GL_OES_EGL_image_external : require
                #ifdef GL_ES
                    precision highp float;
                #endif

                varying vec4 frag_color;
                varying vec2 tex_coord0;

                uniform sampler2D texture0;
                uniform samplerExternalOES texture1;
                uniform vec2 resolution;

                void main()
                {
                    vec2 coord = vec2(tex_coord0.y * (
                        resolution.y / resolution.x), 1. -tex_coord0.x);
                    gl_FragColor = texture2D(texture1, tex_coord0);
                }
            '''
        with self._fbo:
            self._texture_cb = Callback(
                lambda instr: self._lottie_texture.bind)
            Rectangle(size=self._resolution)

        # self._update_start()

    # detete the object
    def __del__(self):
        self._release()

    def _release2(self):
        self._stop()
        if self._fbo:
            self._clear_fbo()
        for attr in ['_fbo', '_surface_texture', '_lottie_texture', '_lottie', '_texture_cb', '_texture']:
            if hasattr(self, attr):
                delattr(self, attr)

    def _release(self):
        if self._lottie is None:
            return
        self._stop()

        # clear texture and it'll be reset in `_update` pointing to new FBO
        # self._surface_texture.release()
        # if self._fbo:
        self._clear_fbo()
        del self._fbo, self._surface_texture, self._lottie_texture, self._lottie, self._texture_cb, self._texture

    def _on_loaded(self, loaded):
        print("CALL BACK ", loaded)
        # if self._lottie:
        #    self.play()
        self.dispatch("on_loaded")

        #width = self.lottie.getIntrinsicWidth()
        #height = self.lottie.getIntrinsicHeight()
        #print("Lottie resolution:", width, "x", height)

    def _update_start(self):
        if self._update_ev:
            self._update_ev.cancel()
        self._update_ev = Clock.schedule_interval(self._update, 1 / self._fps)

    def _update_stop(self):
        if self._update_ev:
            self._update_ev.cancel()

    def _update(self, dt):
        self._surface_texture.updateTexImage()
        self._lottie.renderFrame()

        self._texture_cb.ask_update()
        self._fbo.draw()
        if not self._texture:
            self._texture = self._fbo.texture
        self._callback()

    def _callback(self,):
        # print("hello==")
        self.dispatch('on_update',)

    def _clear_fbo(self):
        if self._fbo:
            with self._fbo:
                ClearColor(0, 0, 0, 0)
                ClearBuffers()
            self._fbo.draw()

    def on_update(self, *args): pass
    def on_loaded(self, *args): pass

    # Playback Controls
    @run_on_ui_thread
    def _play(self, *args):
        if self._lottie:
            self._lottie.play()

        self._update_start()

    @run_on_ui_thread
    def _pause(self):
        if self._lottie:
            self._lottie.pause()

    @run_on_ui_thread
    def _resume(self):
        if self._lottie:
            self._lottie.resume()

    @run_on_ui_thread
    def _stop(self):
        if self._lottie:
            self._lottie.stop()
        self._update_stop()

    def _set_file(self, file_path):
        if self._lottie:
            self._lottie.setFile(file_path)

    def set_speed(self, speed):
        if self._lottie:
            self._lottie.setSpeed(speed)

    def set_repeat_count(self, count):
        if self._lottie:
            self._lottie.setRepeatCount(count)

    def get_repeat_count(self):
        return self._lottie.getRepeatCount() if self._lottie else 0

    def set_repeat_mode(self, mode):
        if self._lottie:
            self._lottie.setRepeatMode(mode)

    def get_repeat_mode(self):
        return self._lottie.getRepeatMode() if self._lottie else -1

    def is_running(self):
        return self._lottie.isRunning() if self._lottie else False

    # Progress Controls
    def set_progress(self, progress):
        if self._lottie:
            self._lottie.setProgress(progress)

    def get_progress(self):
        return self._lottie.getProgress() if self._lottie else 0.0

    def get_duration(self):
        return self._lottie.getDuration() if self._lottie else 0.0

    # Animator Listeners
    def add_animator_listener(self, listener):
        if self._lottie:
            self._lottie.addAnimatorListener(listener)

    def remove_animator_listener(self, listener):
        if self._lottie:
            self._lottie.removeAnimatorListener(listener)

    # Cleanup
    @run_on_ui_thread
    def _clear(self):
        if self._lottie:
            self._lottie.clear()

    @run_on_ui_thread
    def _clear_surface(self):
        if self._lottie:
            self._lottie.clearSurface()
