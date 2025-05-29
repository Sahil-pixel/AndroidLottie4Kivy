# Lottie file Rendering using OpenGL Texture rendering for Android
### Description 
GLLottie Class

GLLottie is a Kivy widget that extends Image to display Lottie animations using OpenGL via the gleslottie library and java backend for Android. It manages loading, displaying, and controlling Lottie animation files seamlessly in your Kivy app.
Properties

    file_path (StringProperty)
    tex_width=512 (texture size)
    tex_height=512
    The path to the Lottie JSON animation file. Changing this property loads a new animation.(Not workig properly right now )

Methods

    on_file_path(obj, filepath)
    Automatically called when file_path changes. Cleans up the previous animation if any, then loads and initializes the new animation.

    _update(obj)
    Called on every animation frame update. Updates the widget texture to display the current animation frame.

    loaded(*args)
    Called once the animation file finishes loading. Automatically starts playing the animation.

    set_file(filepath)
    Sets a new Lottie animation file on the current animation player instance.

    Playback Controls:

        play() — Start or resume animation playback.

        pause() — Pause the animation.

        stop() — Stop the animation.

[![Watch the video on YouTube](https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg)](https://youtube.com/shorts/1dD2m1Yj-Dw?si=UwCECiU9zMkc5_IR)

 ```python
 ##main.py###
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
```
```kv
#myapp.kv
#:import os os
<MainClass>
	orientation:'vertical'
	FloatLayout:
		GLLottie:
			id:img
			size_hint:None,None
			pos_hint:{'center_x':0.5,'center_y':0.5}
			size:self.texture_size
			file_path:os.path.join(os.getcwd(),"work4.json")

			#texture: root._tex
		
		ToggleButton:
			pos_hint:{'center_x':0.2,'center_y':0.1}
			text:'P/S'
			size_hint:None,None
			size:dp(100),dp(80)
			state:'normal'
			on_state:  img.play() if self.state=='normal' else img.stop()
		Button:
			pos_hint:{'center_x':0.8,'center_y':0.1}
			text:'Load another'
			size_hint:None,None
			size:dp(100),dp(80)
			#state:'normal'
			on_release:img.file_path=os.path.join(os.getcwd(),"work2.json")

```
```buildozer.spec 

Around 16 Line

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json



# (int) Target Android API, should be as high as possible.
android.api = 34



Edit your  buildozer.spec 
Around 177 Line

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src =./src

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = True


Around 203 Line

# (list) Gradle dependencies to add
android.gradle_dependencies = com.airbnb.android:lottie:5.2.0,androidx.appcompat:appcompat:1.6.1,androidx.core:core-ktx:1.9.0,androidx.activity:activity:1.6.0



```
For More details read gleslottie.py and java codes 


## Pay for Support

If you find this project helpful and want to support development, you can donate for support:

-  [![Support me on Ko-fi](https://img.shields.io/badge/Support%20me%20on-Ko--fi-%23FF5F5F.svg?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/sahilpixel)
  
- [![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue?style=flat&logo=paypal&logoColor=white)](https://paypal.me/SKSAHILIN?country.x=IN&locale.x=en_GB)


Thank you for your support!
