# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos
import pyglet
from math import floor
from pyglet.image.codecs.png import PNGImageDecoder

class PyFenseHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.currentWave = 1
        self.displayWaveNumber()
        self.buildingHudDisplayed = False
        
        #load tower sprites here, so that they only have to be loaded once
        #TODO: create a loop to load images
        #TODO: gracefully fail if pictures fail to load? (try/catch)
        self.towerThumbnail1 = cocos.sprite.Sprite(pyglet.image.load("assets/tower0.png", decoder=PNGImageDecoder()))
        self.towerThumbnail2 = cocos.sprite.Sprite(pyglet.image.load("assets/tower1.png", decoder=PNGImageDecoder()))
        self.towerThumbnail3 = cocos.sprite.Sprite(pyglet.image.load("assets/tower2.png", decoder=PNGImageDecoder()))
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
        #TODO: proper sourcing of available towers (read from settings?)
        #TODO: lower tower opacity if funds to build tower are insufficient
        #TODO: if player clicks on edge of map, shift HUD to still 
        #   entirely display all buildable towers
        
        self.menuMin_x = x - floor(len(self.towerThumbnails)/2)*self.towerThumbnails[0].width - self.towerThumbnails[0].width / 2
        self.menuMax_x = x + floor(len(self.towerThumbnails)/2)*self.towerThumbnails[0].width + self.towerThumbnails[0].width / 2
        #only half subtracted because function is being called with one half already subtracted
        #due to cocos2d assigning the sprite's center to specified location 
        self.menuMin_y = y - self.towerThumbnails[0].height / 2
        self.menuMax_y = y
        
        #draw buildable tower array
        for picture in range (0, len(self.towerThumbnails)):
            #use self.menuMin_x to center the menu below the coursor in x direction
            #ATTENTION, cocos2d always draws the CENTER of the sprite at the specified location
            self.towerThumbnails[picture].position = (self.menuMin_x + picture*self.towerThumbnails[picture].width + self.towerThumbnails[picture].width/2, y)
            self.add(self.towerThumbnails[picture])
        self.buildingHudDisplayed = True
        
    def removeTowerBuildingHud(self):
        for picture in range (0, len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
        self.buildingHudDisplayed = False
        
    def buildTower(self, towerNumber):
        self.dispatch_event('on_build_tower', towerNumber, self.clicked_x, self.clicked_y)    
        
    def on_mouse_release(self, x, y, buttons, modifiers):
        #TODO: only trigger if user clicked on buildable area
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)

        if self.buildingHudDisplayed == False:
            #to know store where tower has to be build
            #TODO: snap to grid
            self.clicked_x = x
            self.clicked_y = y
            self.displayTowerBuildingHud(x, y - self.towerThumbnails[0].height / 2)
        else:
            #check if player clicked on a menu item
            #if yes, carry out the attached action (build/upgrade/cash-in tower) 
            if y < self.menuMax_y + self.towerThumbnails[0].height / 2 and y > self.menuMin_y:
                #TODO: performance wise smart to check if menu being clicked instead of straight out jumping into the loop?
                if x > self.menuMin_x and x < self.menuMax_x:
                    for i in range (0, len(self.towerThumbnails)):
                        if x > self.menuMin_x + i * self.towerThumbnails[i].width and x < self.menuMax_x - (len(self.towerThumbnails) - i - 1) * self.towerThumbnails[i].width:
                            self.buildTower(i)
            self.removeTowerBuildingHud()
               
PyFenseHud.register_event_type('on_build_tower')