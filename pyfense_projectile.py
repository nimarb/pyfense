#projectile class

import cocos
from cocos import sprite
from cocos import actions
from cocos.actions import *
import math
from math import sqrt
import pyglet
from threading import Timer

import pyfense_entities
from pyfense_entities import *

class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    is_event_handler = True
    
    def __init__(self, target, origin, velocity):
      
        super().__init__("assets/projectile.png", position = origin, scale = 0.3)
        
        self.velocity = velocity
        self.target = target
        self.moveVel(self, self.target, self.velocity)
        
        # After x seconds function is called
        t = Timer(self.duration, self.dispatchHitEvent) 
        t.start()
        
        
        # Remove projectile and dispatch event
    def dispatchHitEvent(self):
        #print('enemy hit!!')
        self.dispatch_event('on_enemy_hit', self) 
        PyFenseEntities.startAnimation(self.position)   
        self.kill()
        
    # Move to position of target with certain velocity    
    def moveVel(self, projectile, enemy, velocity):
        dist = self.distance(self.target, self.position)
        self.duration = dist/velocity
        projectile.do(MoveTo(self.target, self.duration))
        
        
        
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)
        
PyFenseProjectile.register_event_type('on_enemy_hit')