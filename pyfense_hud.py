# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos
import pyglet
from math import floor
from pyglet.image.codecs.png import PNGImageDecoder

class PyFenseHud(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.currentWave = 1
        self.displayWaveNumber()
        self.buildingHudDisplayed = False
        
        #load tower sprites here, so that they only have to be loaded once
        #TODO: create a loop to load images
        self.towerThumbnail1 = cocos.sprite.Sprite(pyglet.image.load("assets/tower.png", decoder=PNGImageDecoder()))
        self.towerThumbnail2 = cocos.sprite.Sprite(pyglet.image.load("assets/tower1.png", decoder=PNGImageDecoder()))
        self.towerThumbnail3 = cocos.sprite.Sprite(pyglet.image.load("assets/enemy.png", decoder=PNGImageDecoder()))
        self.towerThumbnails = [self.towerThumbnail1, self.towerThumbnail2, self.towerThumbnail3]
        
    def displayWaveNumber(self):
        #displays the number of the current wave of enemies
        self.waveLabel = cocos.text.Label('Current Wave: ' + str(self.currentWave), 
                anchor_x='center', anchor_y='center')
        w, h = cocos.director.director.get_window_size()
        self.waveLabel.position = w / 2, h - 30
        self.add(self.waveLabel)
        
    def displayTowerBuildingHud(self, x, y):
        #displays the HUD to chose between towers to build
        #TODO: proper sourcing of available towers (read settings?)
        #TODO: lower tower opacity if funds to build tower are insufficient
        
        self.menuMin_x = x - floor(len(self.towerThumbnails)/2)*self.towerThumbnails[0].width
        self.menuMax_x = x + floor(len(self.towerThumbnails)/2)*self.towerThumbnails[0].width
        self.menuMin_y = y - self.towerThumbnails[0].height / 2
        self.menuMax_y = y
        
        #draw buildable tower array
        for picture in range (0,len(self.towerThumbnails)):
            #use self.menuMin_x to center the menu below the coursor in x direction
            self.towerThumbnails[picture].position = (self.menuMin_x + picture*self.towerThumbnails[picture].width, y)
            self.add(self.towerThumbnails[picture])
        self.buildingHudDisplayed = True
        
    def removeTowerBuildingHud(self):
        for picture in range (0,len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
        self.buildingHudDisplayed = False
        
    def buildTower(towerNumber):
        print("tower number " + str(towerNumber) + " is being build")
        
    def on_mouse_release(self, x, y, buttons, modifiers):
        #TODO: only trigger if user clicked on buildable area
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        if self.buildingHudDisplayed == False:
            self.displayTowerBuildingHud(x, y - self.towerThumbnails[0].height / 2)
        else:
            #check if player clicked on a menu item
            #if yes, carry out the attached action (build/upgrade/cash-in tower) 
            #TODO: check on which Item the user clicked
            if x > self.menuMin_x and x < self.menuMax_x:
                if y < self.menuMax_y + self.towerThumbnails[0].height / 2 and y > self.menuMin_y:
                    print("clicked on menu")
            self.removeTowerBuildingHud()
