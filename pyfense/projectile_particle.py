"""
Projectile class for slow tower, that is handled by emitting particles
instead of moving an image.
"""

from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

import math

import pyglet


class PyFenseProjectileSlow(ParticleSystem, pyglet.event.EventDispatcher):

    # total particles
    total_particles = 2000

    # duration
    duration = 0.1
    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 0
    angle_var = 5

    # radial
    radial_accel = 1000
    radial_accel_var = 0

    # speed of particles, fallback value
    speed = 800
    speed_var = 50

    # emitter variable position
    pos_var = Point2(12, 0)

    # distance that particles fly, fallback value
    distance = 200

    # life of particles, fallback value
    life = 5
    life_var = 0.005

    # emits per frame
    emission_rate = 500

    # color of particles
    start_color = Color(0.58, 0.98, 0.98, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.6)
    end_color = Color(0.53, 0.96, 0.95, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.2)

    # size, in pixels
    size = 40
    size_var = 2.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True

    def __init__(self, towerParent, target, towerNumber,
                 speed, damage, effect, effect_duration, effect_factor):
        """
        Create a projectile.
        
        :Parameters:
            `towerParent`: tower object
                Tower that launched the projectile.
            `target` : enemy object
                Enemy that is targeted.
            `towerNumber` : int
                Number of the parent tower. 
            `rotation` : int
                Rotation of the parent tower.
            `speed` : int
                speed of the projectile.
            `damage` : int
                Damage the projectile causes.
            `effect` : string
                Effect that is caused by projectile (like poison or normal)
            `effect_duration` : int
                Duration that the effect is active.
            `effect_factor` : int
                How strong the effect is.
        """
                     
                     
        super().__init__()

        self.position = towerParent.position
        __class__.speed = speed
        __class__.distance = self._distance(target.position, self.position)
        __class__.life = __class__.distance / __class__.speed
        self.damage = damage

        self.schedule_interval(
            self._dispatch_hit_event, __class__.life, target, towerNumber,
            effect, effect_duration, effect_factor)

    def _dispatch_hit_event(self, dt, target, towerNumber, effect,
                            effect_duration, effect_factor):
        self.unschedule(self._dispatch_hit_event)
        self.dispatch_event('on_target_hit', self, target, towerNumber,
                            effect, effect_duration, effect_factor)

    def _distance(self, a, b):
        dis = math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)
        return dis

PyFenseProjectileSlow.register_event_type('on_target_hit')
