# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from cocos.actions import *
from cocos import layer
from cocos import sprite
from cocos.actions import *
import pyglet
import math

    
settings = {
	"window": {
		"width": 1024,
		"height": 768,
		"caption": "PyFense",
		"vsync": False,
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

    if layer.projectile.position == (512, 384):
        layer.startAnimation()
       

    director.run(main_scene)
    
class drawingTrial(layer.Layer):
    def __init__(self):
        super().__init__()
       
        #Add Sprites and draw them
        self.background = PySprite('assets/background.png', 'center', 'fitHeight')
        self.enemy = PySprite('assets/enemy_ghost.png', (300,200) , 2)
        self.projectile = PySprite('assets/projectile.png', 'center', 0.3)
        self.add(self.background, z = 0)
        self.add(self.enemy, z=1)
        self.add(self.projectile, z= 2)
        
        #Move Projectile with speed 500
        self.moveVel(self.projectile, 500)


        


       
        

        
    #Move Projectile to enemy Position with certain velocity and Hide when enemy is hit
    def moveVel(self, obj, speed):
        dist = self.distance(self.enemy.position, self.projectile.position)
        duration = dist/speed
        #With Delay
        #obj.do(Delay(1) + MoveTo(self.enemy.position, duration))
        obj.do(MoveTo(self.enemy.position, duration)  + Hide())
        

       
    #Distance between two Positions, ie tupel with x and y coordinate   
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)

         
    def startAnimation(self):
        print(self.projectile.position)
        #ANIMATION FOR EXPLOSION
        
        # load the example explosion as a pyglet image
        spritesheet = pyglet.image.load('assets/explosion01_128.png')
            
        # use ImageGrid to divide your sprite sheet into smaller regions
        grid = pyglet.image.ImageGrid(spritesheet, 10, 10, item_width=128, item_height=128)
                
        # convert to TextureGrid for memory efficiency
        textures = pyglet.image.TextureGrid(grid)
                  
        # access the grid images as you would items in a list
        # this way you get a sequence for your animation
        # reads from bottom left corner to top right corner
        explosionSprites = textures[0:len(textures)]
                   
        #create pyglet animation objects
        explosion = pyglet.image.Animation.from_image_sequence(explosionSprites, 1e-6, loop=False)
        explosionSprite = cocos.sprite.Sprite(explosion)
        explosionSprite.position = self.enemy.position
        explosionSprite.scale = 0.4
        self.add(explosionSprite, z=2)
    
    
class PySprite(sprite.Sprite):
    
    #Adds a Sprite with filepath, position and scale
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
   
if __name__ == "__main__":
    main()        