# pyfense_map.py
# contains map class for loading maps and paths associated with it

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder
import cocos

class PyFenseMap(cocos.layer.ScrollableLayer):
	def __init__(self, levelMap):
		super().__init__()
		self.levelMap = levelMap
		self.loadBackgroundImage()
		self.drawBackgroundImage()
		
	def loadBackgroundImage(self):
		#TODO: error handling for no image available case!
		#use python's PNGImageDecoder due to segfault causing bug in gdk_pixbuf2
		self.backgroundImage = pyglet.image.load("assets/" + self.levelMap + "_test.png", decoder=PNGImageDecoder())
		#self.backgroundImage = pyglet.image.load("assets/background.png", decoder=PNGImageDecoder())
		
	def drawBackgroundImage(self):
		self.backgroundSprite = cocos.sprite.Sprite(self.backgroundImage)
		self.backgroundSprite.postition = 300, 330
		self.add(self.backgroundSprite, z=0)
