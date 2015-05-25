# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from cocos.actions import *
from cocos import layer
from cocos import sprite
from cocos.actions import *

    
settings = {
	"window": {
		"width": 1024,
		"height": 768,
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
    director.init(**settings["window"])
    layer_menu = drawingTrial()
    scene_menu = cocos.scene.Scene(layer_menu)
    director.run(scene_menu)
    
    
class drawingTrial(layer.Layer):
     def __init__(self):
         super().__init__()
         background = sprite.Sprite('assets/background.png')
         background.position = settings["window"]["width"]/2, settings["window"]["height"]/2
         background.scale = 0.2
         self.add(background, z=1)
         scale = ScaleBy(3, duration=4)
         background.do(  scale + Reverse(scale) )
         
         #background.draw()
         
    
   
if __name__ == "__main__":
    main()