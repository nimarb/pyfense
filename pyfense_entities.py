# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)

from pyglet.image.codecs.png import PNGImageDecoder
import math

import cocos
from cocos.director import clock

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *
from pyfense_hud import *


class PyFenseEntities(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.towers = []
        self.projectiles = []
        # create new enemy every x seconds

    def startWave(self, waveNumber):
        clock.schedule_interval(self.addEnemy, 1.5)

    def buildTower(self, towerNumber, pos_x, pos_y):
        tower = PyFenseTower(self.enemies, towerNumber, (pos_x, pos_y))
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=1)

    def on_projectile_fired(self, tower, target, projectileVelocity, damage):
        projectile = PyFenseProjectile(tower, target, projectileVelocity, damage)
        self.projectiles.append(projectile)
        i = self.projectiles.index(projectile)
        self.projectiles[i].push_handlers(self)
        self.add(projectile, z=2)

    def on_enemy_hit(self, projectile, target):
        #Animation not working at the moment, no idea why...
        #self.startAnimation(projectile.position)
        target.healthPoints -= projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)        
        if target in self.enemies and target.healthPoints <= 0:
            self.remove(target)
            self.enemies.remove(target)

    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.add(enemy)
        self.add(enemy.drawHealthBar())


    def startAnimation(self, position):
        # load the example explosion as a pyglet image
        spritesheet = pyglet.image.load(
        'assets/explosions-pack/spritesheets/explosion-1.png',
        decoder=PNGImageDecoder())
        # use ImageGrid to divide your sprite sheet into smaller regions
        grid = pyglet.image.ImageGrid(spritesheet, 
                                      1, 8, item_width=32, item_height=32)
        # convert to TextureGrid for memory efficiency
        textures = pyglet.image.TextureGrid(grid)
        # access the grid images as you would items in a list
        # this way you get a sequence for your animation
        # reads from bottom left corner to top right corner
        explosionSprites = textures[0:len(textures)]
        #create pyglet animation objects

        explosion = pyglet.image.Animation.from_image_sequence(
                    explosionSprites, 0.05, loop=True)

        explosionSprite = cocos.sprite.Sprite(explosion)
        explosionSprite.position = position
        explosionSprite.scale = 2
        self.add(explosionSprite, z=2)