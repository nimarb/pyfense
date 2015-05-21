# game.py
# test

import pyglet
from pyglet.window import key

import cocos
from cocos.director import director
from cocos.actions import *

# import of other custom game files
from pyfense_menu import *


# settings (later to be read from cfg file)
# some values might/will change during the course of the game
# for those values, only starting values are being defined here
settings = {
	"window": {
		"width": 800,
		"height": 600,
		"caption": "PyFense",
		"vsync": True,
		"fullscreen": False,
		#ATTENTION: misspelling intentional, pyglet fcked up
		"resizable": True
	}, 
	"world": {
		"gameSpeed": 1.0
	},
	"player": {
		"currency": 200	
	},
	"general": {
		"showFps" : True
	}
}
		
def main():

    director.init(**settings['window'])
    layer_menu = PyFenseMenu()
    scene_menu = cocos.scene.Scene(layer_menu)
    director.set_show_FPS(settings["general"]["showFps"])
    director.run(scene_menu)

if __name__ == '__main__':
    main()
