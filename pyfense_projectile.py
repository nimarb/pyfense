#projectile class

import cocos
from cocos import sprite
from cocos import actions
from cocos.actions import *
import math
from math import sqrt
import pyglet
from pyglet.image.codecs.png import PNGImageDecoder
from threading import Timer

class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    is_event_handler = True
    
    def __init__(self, towerParent, target, velocity):
        projectilePng = pyglet.image.load("assets/projectile0.png", decoder=PNGImageDecoder())
        super().__init__(projectilePng, position = towerParent.position, scale = 0.3)
        self.moveVel(self, target, velocity)
        
        # After x seconds function is called
        t = Timer(self.duration, self.dispatchHitEvent, args=(target,)) 
        t.start()
        
        # Dispatch event, when enemy is hit
    def dispatchHitEvent(self, target):
        self.dispatch_event('on_enemy_hit', self, target) 

        
    # Move to position of target with certain velocity    
    def moveVel(self, projectile, target, velocity):
        dist = self.distance(target.position, self.position)
        self.duration = dist/velocity
        projectile.do(MoveTo(target.position, self.duration))
        
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)
        
    def startAnimation(self, position):
        #ANIMATION FOR EXPLOSION
        # load the example explosion as a pyglet image
        spritesheet = pyglet.image.load('assets/explosions-pack/spritesheets/explosion-1.png', decoder=PNGImageDecoder())
        # use ImageGrid to divide your sprite sheet into smaller regions
        grid = pyglet.image.ImageGrid(spritesheet, 1, 8, item_width=32, item_height=32)
        # convert to TextureGrid for memory efficiency
        textures = pyglet.image.TextureGrid(grid)
        # access the grid images as you would items in a list
        # this way you get a sequence for your animation
        # reads from bottom left corner to top right corner
        explosionSprites = textures[0:len(textures)]
        #create pyglet animation objects
        explosion = pyglet.image.Animation.from_image_sequence(explosionSprites, 0.05, loop=False)
        explosionSprite = cocos.sprite.Sprite(explosion)
        explosionSprite.position = position
        explosionSprite.scale = 1.8
        
        self.add(explosionSprite, z=2) 
        
PyFenseProjectile.register_event_type('on_enemy_hit')        
