import pyglet
from pyglet.window import key
from pyglet import font

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import *
from cocos.layer import *

font.add_directory('data/Orbitron')
_font_ = 'Orbitron Light'

class PyFensePause(scene.Scene):

    def __init__(self):
        super().__init__()
        self.add(PauseLayer(), z=1)


class PauseLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()


        text1 = Label(
            '+++ Game Paused +++',
            font_name=_font_,
            font_size=30,
            anchor_x='center',
            anchor_y='center')

<<<<<<< HEAD
        self.key_font = {}
        self.key_font['font_name'] = 'Arial'
        self.key_font['font_size'] = 20
        self.key_font['anchor_x'] = 'center'
        self.key_font['anchor_y'] = 'center'

        text2 = Label('Press Q to quit game',
                      **self.key_font)
        text3 = Label('Press F to toggle Fullscreen',
                      **self.key_font)
=======
        text2 = Label(
            'Press Q to quit game',
            font_name=_font_,
            font_size=20,
            anchor_x='center',
            anchor_y='center')
>>>>>>> abceb30adb1e68788fa9c34edaaa8e5f5ac23f0f

        text1.position = w/2., h/2. + 50
        text2.position = w/2., h/2. - self.key_font['font_size']
        text3.position = w/2., h/2. - 2 * (self.key_font['font_size'] + 5)
        self.add(text1)
        self.add(text2)
        self.add(text3)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            director.pop()
            return True
        elif k == key.F:
            director.window.set_fullscreen(not director.window.fullscreen)
        elif k == key.Q:
            director.pop()
            director.pop()

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
