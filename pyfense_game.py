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
		print(levelNumber)
		self.levelMapName = "lvl" + str(levelNumber)
		self.loadMap()
		self.displayEntities()
		self.displayHud()
		
	def loadMap(self):
		self.levelMap = PyFenseMap(self.levelMapName)
		self.add(self.levelMap, z=0)
		
	def displayEntities(self):
		self.entityMap = PyFenseEntities()
		self.add(self.entityMap, z=1)
		
	def displayHud(self):
		self.hud = PyFenseHud()
		self.add(self.hud, z=2)
	
		