# pyfense menu

import cocos
from cocos.scenes import SplitRowsTransition

class PyFenseMenu(cocos.menu.Menu):
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
		cocos.director.director.replace(SplitRowsTransition(scene_level, duration=2))
		
	def settings(self):
		cocos.director.director.replace(scene_settings)
		
	def about(self):
		cocos.director.director.replace(SplitRowsTransition(scene_about, duration=2))
		
	def on_quit(self):
		exit()
