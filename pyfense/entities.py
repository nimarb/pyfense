"""
 pyfense_entities.py
 contains the layer on which all enemies and towers are placed (layer)

 z-order of objects in entities:
 z = 0: empty
 z = 1: projectiles before leaving tower radius
 z = 2: towers
 z = 3: enemies
 z = 4: projectiles after leaving tower radius and particle projectiles
 z = 5: explosion
 z = 6: Healthbar background (red)
 z = 7: Healthbar foreground (green)
 z = 8: Warning
"""
import os

import pyglet
from pyglet.window import key
from pyglet import clock
from pyglet import font

import cocos
from cocos.director import director

# import pyfense_tower
from pyfense import enemy
from pyfense import projectile
from pyfense import projectile_particle
from pyfense import pause
from pyfense import resources
from pyfense import particles
from pyfense import highscore
import math

font.add_directory(os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'assets/'))
_font_ = 'Orbitron Light'


class PyFenseEntities(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self, path, startTile, endTile):
        super().__init__()
        self.enemies = []
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.towers = []
        self.projectiles = []
        self.schedule(self._update)
        self.path = path
        self.startTile = startTile
        self.endTile = endTile
        self.wavequantity = len(resources.waves)
        self.enemieslength = 0
        self.polynomial2 = 0  # quadratic
        self.polynomial1 = 2  # linear
        self.polynomial0 = -(self.polynomial1 - 1)  # offset
        self.enemyHealthFactor = 1
        self.schedule_interval(self._update_enemies_order, 0.2)

        # variables that you want to check or modify in the interpreter
        director.interpreter_locals["entities"] = self
        director.interpreter_locals["enemies"] = self.enemies
        director.interpreter_locals["towers"] = self.towers

        # update runs every tick
    def _update(self, dt):
        self._has_enemy_reached_end()

    def next_wave(self, waveNumber):
        self.modulo_wavenumber = (waveNumber - 1) % self.wavequantity + 1
        self.enemy_list = resources.waves[self.modulo_wavenumber]
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.enemyHealthFactor = math.floor((waveNumber - 1) /
                                            self.wavequantity) + 1
        self.multiplier = ((self.polynomial2 * (self.enemyHealthFactor ** 2)) +
                           (self.polynomial1 * self.enemyHealthFactor) +
                           self.polynomial0)
        if self.wavequantity - self.modulo_wavenumber == 1:
            self._show_warning(1)
        elif self.wavequantity - self.modulo_wavenumber == 0:
            self._show_warning(2)
        elif self.modulo_wavenumber == 1 and waveNumber != 1:
            self._show_warning(3)
        self.enemieslength = len(self.enemy_list)
        self.schedule_interval(self._add_enemy, 0, self.startTile, self.path,
                               self.enemy_list, self.multiplier)
        #import pdb; pdb.set_trace()

    def _show_warning(self, warningNumber):
        if warningNumber == 1:
            warningLabel = cocos.text.Label(
                'Enemies will get stronger in 2 Waves!!!',
                font_name=_font_, font_size=64,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 200))
        elif warningNumber == 2:
            warningLabel = cocos.text.Label(
                'Enemies will get stronger next Wave!!!',
                font_name=_font_, font_size=64,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 200))
        elif warningNumber == 3:
            warningLabel = cocos.text.Label(
                'Enemies are now stronger!!!',
                font_name=_font_, font_size=64,
                anchor_x='center', anchor_y='center', color=(255, 0, 0, 200))
        w, h = cocos.director.director.get_window_size()
        warningLabel.position = w / 2, h / 2
        self.add(warningLabel, z=8)
        blinkaction = cocos.actions.Blink(3, 2)
        warningLabel.do(blinkaction)
        clock.schedule_once(lambda dt: self.remove(warningLabel), 3.5)

    def build_tower(self, tower):
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=2)
        return tower.attributes["cost"]

    def get_tower_at(self, position):
        for tower in self.towers:
            if tower.position == position:
                return tower

    def remove_tower(self, position):
        tower = self.get_tower_at(position)
        accumulated_cost = tower.get_accumulated_cost()
        self.remove(tower)
        self.towers.remove(tower)
        return accumulated_cost

    def on_projectile_fired(self, tower, target, projectileimage, towerNumber,
                            rotation, projectileSpeed, damage, effect,
                            effectDuration, effectFactor):

        if towerNumber == 4:
            new_projectile = projectile_particle.PyFenseProjectileSlow(
                tower, target, towerNumber, rotation, projectileSpeed,
                damage, effect, effectDuration, effectFactor)
            self.projectiles.append(new_projectile)
            new_projectile.push_handlers(self)
            self.add(new_projectile, z=4)
        else:
            new_projectile = projectile.PyFenseProjectile(
                tower, target, projectileimage, towerNumber, rotation,
                projectileSpeed, damage, effect, effectDuration, effectFactor)
            self.projectiles.append(new_projectile)
            new_projectile.push_handlers(self)
            self.add(new_projectile, z=1)

    def on_target_hit(self, projectile, target, towerNumber, effect,
                      effectDuration, effectFactor):
        """
        Handels the case, that an projectile hits the target and decides w.r.t.
        the effect which event is called. The projectile is removed.
        """
        explosion = eval('particles.Explosion' + str(towerNumber) + '()')
        explosion.position = target.position
        self.add(explosion, z=5)
        clock.schedule_once(lambda dt, x: self.remove(x), 0.5,
                            explosion)
        self.damage = projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)

        if effect in ('splash', 'splash-slow'):
            self._splash_damage(self.damage, target, towerNumber, effect,
                                effectDuration, effectFactor)
        elif effect in ('normal', 'poison', 'slow'):
            self._deal_damage(self.damage, target, effect,
                              effectDuration, effectFactor)
        else:
            raise ValueError('unknown effect type: ' + effect)

    def _deal_damage(self, damage, target, effect,
                     effectDuration, effectFactor):
        """Deals damage to enemys and handels events slow and poison."""
        target.healthPoints -= damage
        target.update_healthbar()
        if not self.on_has_enemy_died(target):
            if effect == 'slow':
                target.freeze(effectFactor, effectDuration)
            elif effect == 'poison':
                target.poison(effectFactor, effectDuration)
                # TODO: check why ValueError can be raised, is enemy dead or
                # has another enemy in the list died?
                try:
                    self.enemies[self.enemies.index(target)
                                 ].push_handlers(self)
                except ValueError:
                    pass

    def on_has_enemy_died(self, target):
        """checks whether the target has died and returns true if so"""
        if target in self.enemies and target.healthPoints <= 0:
            target.stop_movement()
            self.remove(target.healthBarBackground)
            self.remove(target.healthBar)
            self.remove(target)
            self.enemies.remove(target)
            deathAnimation = particles.Death()
            deathAnimation.position = target.position
            self.add(deathAnimation, z=5)
            clock.schedule_once(lambda dt, x: self.remove(x), 0.5,
                                deathAnimation)
            self.diedEnemies += 1
            self.dispatch_event('on_enemy_death', target)
            self._is_wave_finished()
            return True
        return False

    def _splash_damage(self, damage, target, towerNumber, effect,
                       effectDuration, effectFactor):
        if effect == 'splash-slow':
            new_effect = 'slow'
            dmg_range = 50
        else:
            new_effect = 'normal'
            dmg_range = effectFactor
        targets = self._find_enemys_in_range(target, dmg_range)
        if not target == []:
            for enemy in targets:
                self._deal_damage(damage, enemy, new_effect, effectDuration,
                                  effectFactor)

    def _find_enemys_in_range(self, position, range):
        """
        Looks and gives back enemys in range
        """
        targets = []
        for enemy in self.enemies:
            if(enemy.x < cocos.director.director.get_window_size()[0] and
               # Enemy still in window
               enemy.y < cocos.director.director.get_window_size()[1]):
                # Distance to enemy smaller than range
                if (self._distance(enemy, position) < range):
                    targets.append(enemy)
        return targets

    def _distance(self, a, b):
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    def _is_wave_finished(self):
        if self.spawnedEnemies == self.enemieslength:
            if self.diedEnemies == self.spawnedEnemies:
                self.dispatch_event('on_next_wave')

    def _add_enemy(self, dt, startTile, path, enemylist, multiplier):
        self.unschedule(self._add_enemy)
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
            self.schedule_interval(self._add_enemy,
                                   self.enemy_list[self.spawnedEnemies - 1][2],
                                   self.startTile, self.path,
                                   self.enemy_list, self.multiplier)
        self._is_wave_finished()

    # Removes enemy from entity when the enemy has reached
    def _has_enemy_reached_end(self):
        if self.enemies and self.enemies[0].position == self.endTile:
            self.enemies[0].stop_movement()
            self.dispatch_event('on_enemy_reached_goal')
            self.remove(self.enemies[0])
            self.remove(self.enemies[0].healthBar)
            self.remove(self.enemies[0].healthBarBackground)
            self.enemies.remove(self.enemies[0])
            self.diedEnemies += 1
            self._is_wave_finished()

    def _update_enemies_order(self, dt):
        if self.enemies:
            self.enemies.sort(key=lambda x: x.distance, reverse=True)

    # Overrides the Esc key and quits the game on "Q"
    def on_key_press(self, k, m):
        if k == key.ESCAPE:
            director.push(pause.PyFensePause())
            return True
        if k == key.Q:
            director.replace(highscore.PyFenseLost())

PyFenseEntities.register_event_type('on_next_wave')
PyFenseEntities.register_event_type('on_enemy_death')
PyFenseEntities.register_event_type('on_enemy_reached_goal')
