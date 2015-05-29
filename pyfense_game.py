# pyfense_game.py
# contains PyFenseGame class (scene)

import cocos
import pyglet
import math
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
		#initialise game grid to store where enemies can walk, 
		# towers can be build and where towers are already built
		#one grid cell is 60x60px large (full hd resolution scale) 
		#key: 
		#0 := no tower can be build, no enemy can walk
		#1 := no tower can be build, enemy can walk
		#2 := tower can be build, no enemy can walk
		#3 := tower has been built, no enemy can walk, no tower can be build (can upgrade (?))
		self.gameGrid = [[0 for x in range (8)] for x in range(16)]

	def loadMap(self):
		self.levelMap = PyFenseMap(self.levelMapName)
		self.add(self.levelMap, z=0)

	def displayEntities(self):
		self.entityMap = PyFenseEntities()
		self.add(self.entityMap, z=1)

	def displayHud(self):
		self.hud = PyFenseHud()
		self.hud.push_handlers(self)
		self.add(self.hud, z=2)
		
	def setGridPix(self, x, y, kind)
		if kind < 0 or kind > 3:
			print("WRONG GRID TYPE, fix ur shit")
			return
		grid_x = math.abs(x / 60)
		grid_y = math.abs(y / 60)
		self.setGrid(grid_x, grid_y, kind)
		
	def setGrid(self, grid_x, grid_y, kind):
		if kind < 0 or kind > 3:
			print("WRONG GRID TYPE, fix ur shit")
			return
		self.gameGrid[grid_x][grid_y] = kind
		
	def on_build_tower(self, towerNumber, pos_x, pos_y):
		self.entityMap.buildTower(towerNumber, pos_x, pos_y)

	def on_timer_out(self, wave):
		self.entityMap.startWave(wave)
