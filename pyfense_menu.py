# pyfense menu

import cocos

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
		exit()
	def settings(self):
		exit()
	def about(self):
		exit()
	def on_quit(self):
		exit()
	
