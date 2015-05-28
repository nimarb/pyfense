#projectile class

import cocos
from cocos import sprite
from cocos import actions
from cocos.actions import *
import math
from math import sqrt
import pyglet


class PyFenseProjectile(sprite.Sprite):
    def __init__(self, target, origin, velocity):
        super().__init__("assets/projectile0.png", position = origin, scale = 0.3)
        
        self.velocity = velocity
        self.target = target
        self.moveVel(self, self.target, self.velocity)
        
        #self.kill
        
    # Move to position of target with certain velocity    
    def moveVel(self, projectile, enemy, velocity):
        dist = self.distance(self.target, self.position)
        duration = dist/velocity
        projectile.do(MoveTo(self.target, duration))
        
        
        
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)