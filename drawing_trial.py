# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from cocos.actions import *
from cocos import layer
from cocos import sprite
from cocos.actions import *
import math

    
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
       
        self.background = PySprite('assets/background.png', 'center', 'fitHeight')
        self.enemy = PySprite('assets/enemy_ghost.png', (300,200) , 2)
        self.projectile = PySprite('assets/projectile.png', 'center', 0.3)
        self.add(self.background, z = 0)
        self.add(self.enemy, z=1)
        self.add(self.projectile, z= 2)
        
        self.moveVel(self.projectile, 500)
        
        
    #Move Projectile to enemy Position with certain velocity
    def moveVel(self, obj, speed):
        dist = self.distance(self.enemy.position, self.projectile.position)
        duration = dist/speed
        obj.do(MoveTo(self.enemy.position, duration))
        
       
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)

         
    
class PySprite(sprite.Sprite):
    
    #Adds a Sprite with filepath
    def __init__(self, filepath, position, scale):
        super().__init__(filepath)
                
        #Recognize 'center' as keyword for position
        if position == 'center':
            self.position =  director.get_window_size()[0]/2, director.get_window_size()[1]/2 
        else:
            self.position = position
            
        #Recognize 'fitHeight' and'fitWidth' as keywords for scale
        if scale == 'fitHeight':
            self.scale = director.get_window_size()[1]/self.height
        elif scale == 'fitWidth':
            self.scale = director.get_window_size()[0]/self.width
        else:
            self.scale = scale
                
        
        
        
        
        
 


        
        
    
    
    






        
      
#    def drawSprite(self, filepath, position, scale, z):
#        self.filepath = filepath
#        self.z = z
#        
#        
#        #Recognize 'fitHeight' and 'fitWidth' as keyword for scale
##        if scale == 'fitHeight':
##             self.scale = settings["window"]["height"]/self.image.height
##        elif scale == 'fitWidth':
##             self.scale = settings["window"]["width"]/self.image.width
##        else:
#        self.scale = scale
#        
#        #Recognize 'center' as keyword for position
#        if position == 'center':
#            self.position = settings["window"]["width"]/2, settings["window"]["height"]/2
#           
#        else:
#            self.position = position
#            
#        print(self.filepath)
#        print(self.position)
#        print(self.scale)
#        print(self.z)
#        
#        image = sprite.Sprite(filepath)
#
#        image.position = 0,0
#        image.scale = 6
#        
#        print(image.position)
#        
#        self.add(image, self.z)
#        
#        
        
        #Import and draw sprites
#        background = sprite.Sprite('assets/background.png')
#        background.scale = settings["window"]["height"]/background.height        
#        background.position = settings["window"]["width"]/2, settings["window"]["height"]/2
#  
#        self.add(background, z=0)
#         
#        projectile = sprite.Sprite('assets/projectile.png')
 #       projectile.position = settings["window"]["width"]/2, settings["window"]["height"]/2
  #      projectile.scale = 0.2
   #     self.add(projectile, z=2)
         
#        enemy = sprite.Sprite('assets/enemy_ghost.png')
 #       enemy.position = 300, 200
  #      enemy.scale = 2
   #     self.add(enemy, z=1)
         
         

             
              
      
         
         
    
   
if __name__ == "__main__":
    main()        