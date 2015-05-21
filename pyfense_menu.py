# pyfense menu

import cocos
from cocos.scene import Scene
from cocos.director import director
from cocos.scenes import SplitRowsTransition
from cocos.scenes import SlideInRTransition
from cocos import menu

from pyfense_about import *
from pyfense_settings import *
from pyfense_level import *

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
		director.push(SlideInRTransition(Scene(PyFenseLevel()), duration=1))

	def settings(self):
		director.push(SlideInRTransition(Scene(PyFenseSettings()), duration=1))

	def about(self):
		director.push(SlideInRTransition(Scene(PyFenseAbout()), duration=1))

	def on_quit(self):
		exit()
