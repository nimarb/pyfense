# pyfense_game.py
# contains PyFenseGame class (scene)

import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from pyfense_map import *

class PyFenseGame(scene.Scene):
	def __init__(self, levelNumber):
		super.__init__()
		self.levelMap = "level_" + levelNumber
		
	def loadMap():
		self.levelMap = PyFenseMap(self.levelMap)
		
	def get_level_number():
		return self.levelNumber
	