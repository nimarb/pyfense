import pyglet
from pyglet.window import key
from pyglet import font

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import *
from cocos.layer import *

import pyfense_resources

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

        self.key_font = {}
        self.key_font['font_name'] = 'font_'
        self.key_font['font_size'] = 20
        self.key_font['anchor_x'] = 'center'
        self.key_font['anchor_y'] = 'center'

        text2 = Label('Press Q to quit game',
                      **self.key_font)
        text3 = Label('Press F to toggle Fullscreen',
                      **self.key_font)
        text4 = Label('Press V to toggle Vsync',
                      **self.key_font)
        text5 = Label('Press X to toggle FPS',
                      **self.key_font)
        text6 = Label('Press S to toggle Sound',
                      **self.key_font)

        text1.position = w/2., h/2. + 50
        text2.position = w/2., h/2. - 1 * (self.key_font['font_size'] + 8)
        text3.position = w/2., h/2. - 2 * (self.key_font['font_size'] + 8)
        text4.position = w/2., h/2. - 3 * (self.key_font['font_size'] + 8)
        text5.position = w/2., h/2. - 4 * (self.key_font['font_size'] + 8)
        text6.position = w/2., h/2. - 5 * (self.key_font['font_size'] + 8)

        self.add(text1)
        self.add(text2)
        self.add(text3)
        self.add(text4)
        self.add(text5)
        self.add(text6)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            director.pop()
            return True
        elif k == key.F:
            director.window.set_fullscreen(not director.window.fullscreen)
            return True
        elif k == key.V:
            director.window.set_vsync(not director.window.vsync)
            return True
        elif k == key.X:
            director.show_FPS = not director.show_FPS
            return True
        elif k == key.S:
            pyfense_resources.sounds = not pyfense_resources.sounds
            return True
        elif k == key.Q:
            director.pop()
            director.pop()
            return True

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
