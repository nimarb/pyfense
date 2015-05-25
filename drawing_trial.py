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
    layer = drawingTrial()
    main_scene = cocos.scene.Scene(layer)
    director.run(main_scene)
    
    
class drawingTrial(layer.Layer):
     def __init__(self):
         super().__init__()
         background = sprite.Sprite('assets/background.png')
         background.position = settings["window"]["width"]/2, settings["window"]["height"]/2
         background.scale = settings["window"]["height"]/background.height
         self.add(background, z=0)
         
         projectile = sprite.Sprite('assets/projectile.png')
         projectile.position = settings["window"]["width"]/2, settings["window"]["height"]/2
         projectile.scale = 0.5
         self.add(projectile, z=1)
         
         move = MoveTo((30, 40), 3)
         projectile.do(move)
      
         #scale = ScaleBy(3, duration=4)
         #background.do(  scale + Reverse(scale) )
         
         #background.draw()
         
    
   
if __name__ == "__main__":
    main()