# pyfense menu

import cocos
from cocos.scene import Scene
from cocos.director import director
from cocos.scenes import SplitRowsTransition
from cocos import menu

from pyfense_about import *

class PyFenseMenu(menu.Menu):
	def __init__(self):
		super(PyFenseMenu, self).__init__("PyFense")
		startGame = cocos.menu.MenuItem("Start Game", self.startGame)
		settings = cocos.menu.MenuItem("Settings", self.settings)
		about = cocos.menu.MenuItem("About", self.about)
		exit = cocos.menu.MenuItem("Exit", self.on_quit)
		menuItems = [startGame, settings, about, exit]
		self.create_menu(menuItems)
	
	#all functions save for the on_quit function still need logic
	def startGame(self):
		director.push(SplitRowsTransition(scene_level, duration=2))
		
	def settings(self):
		director.replace(scene_settings)
		
	def about(self):
		director.push(SplitRowsTransition(Scene(PyFenseAbout()), duration=2))
		
	def on_quit(self):
		exit()
