# game.py
# test

import cocos

class PyFenseUi(cocos.layer.Layer):
	def __init__(self):
		super(PyFenseUi, self).__init__()
		welcomeLabel = cocos.text.Label('Welcome to PyFense', 
										anchor_x='center', anchor_y='center')
		welcomeLabel.position = 200, 200
		self.add(welcomeLabel)

cocos.director.director.init()
pyfense_ui_layer = PyFenseUi()

main_scene = cocos.scene.Scene(pyfense_ui_layer)
cocos.director.director.run(main_scene)
