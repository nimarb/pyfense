#projectile class

import cocos
from cocos import sprite
from cocos import actions
from cocos.actions import *
import math
from math import sqrt


class PyFenseProjectile(sprite.Sprite):
    def __init__(self, target, origin):
        super().__init__("assets/projectile.png", position = origin, scale = 0.3)
        #moveTo = (target[0]-origin[0], target[1]-origin[1])
        #self.do(actions.MoveBy(moveTo, 0.4))
        self.target = target
        self.moveVel(self, self.target, 2000)
        
        self.kill
        
    # Move to position of target with certain velocity    
    def moveVel(self, projectile, enemy, velocity):
        dist = self.distance(self.target, self.position)
        duration = dist/velocity
        projectile.do(MoveTo(self.target, duration))
        
        
    def distance(self, a, b):
        return math.sqrt( (b[0] - a[0])**2 + (b[1]-a[1])**2)        