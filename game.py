# game.py
# test

import cocos
from cocos.actions import *


# settings (later to be read from cfg file)
# some values might/will change during the course of the game
# for those values, only starting values are being defined here
settings = {
	"window": {
		"width": 800,
		"height": 600,
		"caption": "PyFense",
		"vsync": True,
		"fullscreen": False,
		#ATTENTION: misspelling intentional, pyglet fcked up
		"resizable": True
	}, 
	"world": {
		"gameSpeed": 1.0
	},
	"player": {
		"currency": 200	
	}
}

class PyFenseMenu(cocos.menu.Menu):
	def __init__(self):
		super(PyFenseMenu, self).__init__("PyFense")
		startGame = cocos.menu.MenuItem("Start Game", self.startGame)
		settings = cocos.menu.MenuItem("Settings", self.settings)
		about = cocos.menu.MenuItem("About", self.about)
		exit = cocos.menu.MenuItem("Exit", self.on_quit)
		menuItems = [startGame, settings, about, exit]
		self.create_menu(menuItems)
	def startGame(self):
		exit()
	def settings(self):
		exit()
	def about(self):
		exit()
	def on_quit(self):
		exit()
	
	
class PyFenseUi(cocos.layer.Layer):
	def __init__(self):
		super(PyFenseUi, self).__init__()
		welcomeLabel = cocos.text.Label('Welcome to PyFense', 
										anchor_x='center', anchor_y='center')
		welcomeLabel.position = 200, 200
		self.add(welcomeLabel)
		scale = ScaleBy(3, duration=0.5)
		welcomeLabel.do(Repeat(scale + Reverse(scale)))

def main():
	cocos.director.director.init(**settings['window'])
	pyfense_ui_layer = PyFenseUi()
	pyfense_menu = PyFenseMenu()
	main_scene = cocos.scene.Scene(pyfense_menu)
	cocos.director.director.run(main_scene)

if __name__ == '__main__':
	main()
