# pyfense_game.py
# contains PyFenseGame class (scene)

import cocos
import pyglet
from cocos.director import director
from cocos import scene
from pyfense_map import *

class PyFenseGame(scene.Scene):
	def __init__(self, levelNumber):
		super().__init__()
		print(levelNumber)
		self.levelMapName = "lvl" + str(levelNumber)
		self.loadMap()
		
	def loadMap(self):
		self.levelMap = PyFenseMap(self.levelMapName)
		self.add(self.levelMap, z=1)
		