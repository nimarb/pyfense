# pyfense_about.py
# contains PyFenseAbout class (menu)

import cocos
from cocos import menu
from cocos import text

import pyglet

class PyFenseAbout(menu.Menu):
    def __init__(self):
        super().__init__("About PyFense")
        back = menu.MenuItem("Back", self.back)
        abtText = menu.MenuItem("PyFense is a Tower Defense style game made by five students at TUM", self.void)
        #abtText.label.position = 512, 600
        #self.super(abtText, self).item["font_size"] = 14
        #aboutText = text.Label("PyFense is a Tower Defense style game made by five students at TUM", 
        #    font_size=14, anchor_x='center', anchor_y='center')
        #aboutText = pyglet.text.Label("asdasdsd", font_size=14, anchor_x='center', anchor_y='center')
        #aboutText.position = 512, 600
        self.create_menu([back, abtText])
        #self.add(aboutText)
        
    def back(self):
        cocos.director.director.pop()
    def void(self):
        pass
        