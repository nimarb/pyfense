import cocos
import cocos.particle
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2



class Explosion(ParticleSystem):

    # total particles
    total_particles = 800

    # duration
    duration = 0.1

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 5

    # speed of particles
    speed = 200
    speed_var = 50

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 2	
    life_var = 1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.7, 0.2, 0.1, 1.0)
    start_color_var = Color(0.5, 0.5, 0.5, 0.0)
    end_color = Color(0.5, 0.5, 0.5, 0.0)
    end_color_var = Color(0.5, 0.5, 0.5, 0.0)

    # size, in pixels
    size = 15
    size_var = 2.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class Fire(ParticleSystem):

    # total particles
    total_particles = 500

    # duration
    duration = 0.05

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 100
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.76, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 70.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


