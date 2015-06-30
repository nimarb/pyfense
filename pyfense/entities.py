"""
 pyfense_entities.py
contains the layer on which all enemies and towers are placed (layer)
"""
import pyglet
from pyglet.window import key
from pyglet import clock

import cocos
from cocos.director import director

# import pyfense_tower
from pyfense import enemy
from pyfense import projectile
# import pyfense_hud
from pyfense.pause import PyFensePause
from pyfense import resources
from pyfense import particles
from pyfense import highscore
import math


class PyFenseEntities(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self, path, startTile, endTile):
        super().__init__()
        self.enemies = []
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.towers = []
        self.projectiles = []
        self.schedule(self.update)
        self.path = path
        self.startTile = startTile
        self.endTile = endTile
        self.wavequantity = len(resources.waves)
        self.enemieslength = 0
        self.polynomial2 = 0  # quadratic
        self.polynomial1 = 2  # linear
        self.polynomial0 = -(self.polynomial1 - 1)  # offset
        self.enemyHealthFactor = 1
        clock.schedule_interval(self.updateEnemiesOrder, 0.2)

        # update runs every tick
    def update(self, dt):
        self.hasEnemyReachedEnd()

    def nextWave(self, waveNumber):
        self.modulo_wavenumber = (waveNumber-1) % self.wavequantity+1
        self.enemy_list = resources.waves[self.modulo_wavenumber]
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.enemyHealthFactor = math.floor((waveNumber - 1) /
                                            self.wavequantity) + 1
        self.multiplier = ((self.polynomial2 * (self.enemyHealthFactor**2)) +
                           (self.polynomial1 * self.enemyHealthFactor) +
                           self.polynomial0)
        if self.wavequantity-self.modulo_wavenumber == 1:
            self.showWarning(1)
        elif self.wavequantity-self.modulo_wavenumber == 0:
            self.showWarning(2)
        elif self.modulo_wavenumber == 1 and waveNumber != 1:
            self.showWarning(3)
        self.enemieslength = len(self.enemy_list)
        clock.schedule_once(self.addEnemy, 0, self.startTile, self.path,
                            self.enemy_list, self.multiplier)

    def showWarning(self, warningNumber):
        if warningNumber == 1:
            self.warningLabel = cocos.text.Label(
                'Enemies will get stronger in 2 Waves!!!',
                font_name='Times New Roman', font_size=32,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
        elif warningNumber == 2:
            self.remove(self.warningLabel)
            self.warningLabel = cocos.text.Label(
                'Enemies will get stronger next Wave!!!',
                font_name='Times New Roman', font_size=32,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
        elif warningNumber == 3:
            self.remove(self.warningLabel)
            self.warningLabel = cocos.text.Label(
                'Enemies are now stronger!!!',
                font_name='Times New Roman', font_size=32,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
            clock.schedule_once(lambda dt: self.remove(self.warningLabel), 15)
        w, h = cocos.director.director.get_window_size()
        self.warningLabel.position = w / 2, h - 100
        self.add(self.warningLabel)
        blinkaction = cocos.actions.Blink(3, 3)
        self.warningLabel.do(blinkaction)

    def buildTower(self, tower):
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=2)
        return tower.attributes["cost"]

    def getTowerAt(self, position):
        for tower in self.towers:
            if tower.position == position:
                return tower

    def removeTower(self, position):
        tower = self.getTowerAt(position)
        self.remove(tower)
        self.towers.remove(tower)
        return tower.attributes["cost"]

    def on_projectile_fired(self, tower, target, projectileimage, towerNumber,
                            rotation, projectileVelocity, damage):
        newProjectile = projectile.PyFenseProjectile(tower, target,
                                                          projectileimage,
                                                          towerNumber,
                                                          rotation,
                                                          projectileVelocity,
                                                          damage)
        self.projectiles.append(newProjectile)
        newProjectile.push_handlers(self)
        self.add(newProjectile, z=1)
        duration = 80 / projectileVelocity
        clock.schedule_once(lambda dt: self.changeZ(projectile, 1, 4),
                            duration)

    def changeZ(self, cocosnode, z_before, z_after):
        if (z_before, cocosnode) in self.children:
            self.remove(cocosnode)
            self.add(cocosnode, z_after)

    def on_enemy_hit(self, projectile, target, towerNumber):
        explosion = eval('particles.Explosion' +
                         str(towerNumber) + '()')
        explosion.position = target.position
        self.add(explosion, z=5)
        pyglet.clock.schedule_once(lambda dt, x: self.remove(x), 0.5,
                                   explosion)
        target.healthPoints -= projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)
        target.updateHealthBar()
        if target in self.enemies and target.healthPoints <= 0:
            target.die()
            self.remove(target.healthBarBackground)
            self.remove(target.healthBar)
            self.remove(target)
            self.enemies.remove(target)
            deathAnimation = particles.Death()
            deathAnimation.position = target.position
            self.add(deathAnimation, z=5)
            pyglet.clock.schedule_once(lambda dt, x: self.remove(x), 0.5,
                                       deathAnimation)
            self.diedEnemies += 1
            self.dispatch_event('on_enemy_death', target)
            self.isWaveFinished()

    def isWaveFinished(self):
        if self.spawnedEnemies == self.enemieslength:
            if self.diedEnemies == self.spawnedEnemies:
                self.dispatch_event('on_next_wave')

    def addEnemy(self, dt, startTile, path, enemylist, multiplier):
        position = startTile
        toCreateEnemy = enemy.PyFenseEnemy(position,
                                           enemylist[self.spawnedEnemies][0],
                                           enemylist[self.spawnedEnemies][1],
                                           1, path, multiplier)
        self.enemies.append(toCreateEnemy)
        self.spawnedEnemies += 1
        self.add(toCreateEnemy, z=3)
        self.add(toCreateEnemy.healthBarBackground, z=6)
        self.add(toCreateEnemy.healthBar, z=7)
        if self.spawnedEnemies != self.enemieslength:
            clock.schedule_once(self.addEnemy,
                                self.enemy_list[self.spawnedEnemies-1][2],
                                self.startTile, self.path,
                                self.enemy_list, self.multiplier)
        self.isWaveFinished()

    # Removes enemy from entity when no action is running,
    # ie the enemy has reached
    def hasEnemyReachedEnd(self):
        # if self.enemies and not self.enemies[0].actions:
        if self.enemies and not self.enemies[0].position != self.endTile:
            self.enemies[0].die()
            self.dispatch_event('on_enemy_reached_goal')
            self.remove(self.enemies[0])
            self.remove(self.enemies[0].healthBar)
            self.remove(self.enemies[0].healthBarBackground)
            self.enemies.remove(self.enemies[0])
            self.diedEnemies += 1
            self.isWaveFinished()

    def updateEnemiesOrder(self, dt):
        if self.enemies:
            self.enemies.sort(key=lambda x: x.distance, reverse=True)

    # Overrides the Esc key and quits the game on "Q"
    def on_key_press(self, k, m):
        if k == key.ESCAPE:
            director.push(PyFensePause())
            return True
        if k == key.Q:
            director.replace(highscore.PyFenseLost())

PyFenseEntities.register_event_type('on_next_wave')
PyFenseEntities.register_event_type('on_enemy_death')
PyFenseEntities.register_event_type('on_enemy_reached_goal')
