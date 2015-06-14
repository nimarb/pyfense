import pyglet
from pyglet.window import key

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import *
from cocos.layer import *

class PyFensePause( scene.Scene ):
    
    def __init__( self ):
        super().__init__()

    def on_enter( self ):
        self.add( PauseLayer(), z=1 )

class PauseLayer( Layer, pyglet.event.EventDispatcher ):
        
    is_event_handler = True

    def __init__( self ):
        super().__init__()
        w, h = director.get_window_size()
        text = Label('+++ Game Paused +++',
                     font_name = 'Arial',
                     font_size = 20,
                     anchor_x = 'center',
                     anchor_y = 'center')
        text.position = w/2. , h/2.
        self.add(text)
        
    def on_key_press( self, k, m ):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q ):
            print("exit key pressed")
            director.pop()
            return True
              
    def on_mouse_release( self, x, y, b, m ):
        print("mouse to exit used")
        director.pop()
        return True
