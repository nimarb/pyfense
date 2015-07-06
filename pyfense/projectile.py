# pyfense_projectile
# projectile class

from cocos import sprite
from cocos import actions
import math
import pyglet


class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(
            self, towerParent, target, image, towerNumber, rotation,
            velocity, damage, effect, effectduration):
        projectilePng = image
        super().__init__(projectilePng, position=towerParent.position,
                         scale=1)
        self.rotation = rotation
        self.damage = damage
        self.velocity = velocity
        self.distance = self._distance(target.position, self.position)
        self.duration = self._duration()
        self.do(actions.MoveTo(target.position, self.duration))
        self.schedule_interval(
            self._dispatch_hit_event, self.duration, target, towerNumber,
            effect, effectduration)

        # Dispatch event, when enemy is hit
    def _dispatch_hit_event(self, dt, target, towerNumber, effect,
                         effectduration):
        self.unschedule(self._dispatch_hit_event)     
        self.dispatch_event('on_enemy_hit', self, target, towerNumber,
                            effect, effectduration)
    
    def _duration(self):
        dur = self.distance/self.velocity
        return dur

    def _distance(self, a, b):
        dis = math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)
        return dis

PyFenseProjectile.register_event_type('on_enemy_hit')
