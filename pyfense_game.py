# pyfense_game.py
# contains PyFenseGame class (scene)

import cocos
import pyglet
from cocos.director import director
from cocos import scene

from pyfense_map import *
from pyfense_entities import *
from pyfense_hud import *

class PyFenseGame(scene.Scene):
	def __init__(self, levelNumber):
		super().__init__()
		self.levelMapName = "lvl" + str(levelNumber)
		self.loadMap()
		self.displayEntities()
		self.displayHud()
		self.currentWave = 0
		self.currentLives = 30
		self.currentCurrency = 500
		#initialise game grid to store where enemies can walk, 
		# towers can be build and where towers are already built
		#one grid cell is 60x60px large (full hd resolution scale) 
		#gameGrid can be called by using gameGrid[y][x]
		#key: 
		#0 := no tower can be build, no enemy can walk
		#1 := no tower can be build, enemy can walk
		#2 := tower can be build, no enemy can walk
		#3 := tower has been built, no enemy can walk, no tower can be build (can upgrade (?))
		self.gameGrid = [[0 for x in range (32)] for x in range(18)]

	def loadMap(self):
		self.levelMap = PyFenseMap(self.levelMapName)
		self.add(self.levelMap, z=0)

	def displayEntities(self):
		self.entityMap = PyFenseEntities()
		self.entityMap.push_handlers(self)
		self.add(self.entityMap, z=1)

	def displayHud(self):
		self.hud = PyFenseHud()
		self.hud.push_handlers(self)
		self.add(self.hud, z=2)
		
	def setGridPix(self, x, y, kind):
		if kind < 0 or kind > 3:
			print("WRONG GRID TYPE, fix ur shit")
			return
		grid_x = int(x / 60)
		grid_y = int(y / 60)
		self.setGrid(grid_x, grid_y, kind)
		
	def setGrid(self, grid_x, grid_y, kind):
		if kind < 0 or kind > 3:
			print("WRONG GRID TYPE, fix ur shit")
			return
		self.gameGrid[grid_y][grid_x] = kind
		
	def getGridPix(self, x, y):
		grid_x = int(x / 60)
		grid_y = int(y / 60)
		#gracefully fail for resolution edge cases
		if grid_x > 31:
			grid_x = 31
		if grid_y > 17:
			grid_y = 17
		return self.gameGrid[grid_y][grid_x]
		
	def on_enemy_death(self, enemy):
		self.currentCurrency += enemy.worth
		self.hud.updateCurrencyNumber(self.currentCurrency)
		
	def on_user_mouse_motion(self, x, y):
		self.hud.currentCellStatus = self.getGridPix(x, y)		
		
	def on_build_tower(self, towerNumber, pos_x, pos_y):
		#TODO: check if tower can be build here?
		#TODO: check if sufficient currency available to build tower
		tower = PyFenseTower(self.entityMap.enemies, towerNumber, (pos_x, pos_y))
		if tower.cost > self.currentCurrency:
			print("not enough cash, building tower failed")
			return
		self.currentCurrency -= self.entityMap.buildTower(tower)
		self.setGridPix(pos_x, pos_y, 3)
		self.hud.updateCurrencyNumber(self.currentCurrency)

	def on_next_wave(self):
		self.hud.startNextWaveTimer()
		
	def on_next_wave_timer_finished(self):
		self.currentWave += 1
		self.entityMap.nextWave(self.currentWave)
		self.hud.updateWaveNumber(self.currentWave)
		
	def on_enemy_reached_goal(self):
		self.currentLives -= 1
		self.hud.updateLiveNumber(self.currentLives)
		if self.currentLives == 0:
			print("YOU LOST THE GAME")

