import pyglet
from pyglet.window import key

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import *
from cocos.layer import *


class PyFensePause(scene.Scene):

    def __init__(self):
        super().__init__()
        self.add(PauseLayer(), z=1)


class PauseLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()

        text = RichLabel('+++ Game Paused +++ \\' +
                         'Press Q to quit game',
                         font_name='Arial',
                         font_size=20,
                         anchor_x='center',
                         anchor_y='center',
                         halign='center')
        text.element.width = w * 0.3
        text.element.multiline = True
        text.element.wrap_lines = True
        text.position = w/2., h/2. + 25
        self.add(text)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            director.pop()
            return True
        elif k == key.Q:
            director.pop()
            director.pop()

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
