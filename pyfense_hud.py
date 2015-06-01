# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos
import pyglet
from math import floor
import pyfense_resources

class PyFenseHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.timeBetweenWaves = 3
        self.time = self.timeBetweenWaves
        self.displayStatusBar()
        self.buildingHudDisplayed = False
        self.startNextWaveTimer()
        #load tower sprites here, so that they only have to be loaded once
        #TODO: create a loop to load images
        #TODO: gracefully fail if pictures fail to load? (try/catch)
        self.towerThumbnail1 = cocos.sprite.Sprite(pyfense_resources.tower[0])
        self.towerThumbnail2 = cocos.sprite.Sprite(pyfense_resources.tower[1])
        self.towerThumbnail3 = cocos.sprite.Sprite(pyfense_resources.tower[2])
        self.towerThumbnails = [self.towerThumbnail1, self.towerThumbnail2, self.towerThumbnail3]
        #load selector to highlight currently selected cell
        self.addCellSelectorSprite()
        self.currentCellStatus = 0
        
    def displayStatusBar(self):
        self.waveLabel = cocos.text.Label('Current Wave: 1',
                anchor_x='center', anchor_y='center')
        w, h = cocos.director.director.get_window_size()
        self.waveLabel.position = w / 2, h - 30
        self.add(self.waveLabel)
        self.timeLabel = cocos.text.Label('Time until next Wave: ' +
                str(self.time) + ' Seconds', anchor_x='center', anchor_y='center')
        self.timeLabel.position = w / 2 - 250, h - 30
        self.add(self.timeLabel)
        self.liveLabel = cocos.text.Label('Remaining Lives: 30', 
                anchor_x='center', anchor_y='center')
        self.liveLabel.position = w / 2 + 200, h - 30
        self.add(self.liveLabel)
        self.currencyLabel = cocos.text.Label('500 Currency', 
                anchor_x='center', anchor_y='center')
        self.currencyLabel.position = w / 2 + 350, h - 30
        self.add(self.currencyLabel)
        
    def updateLiveNumber(self, liveNumber):
        self.liveLabel.element.text = ("Remaining Lives: " + str(liveNumber))
                
    def updateWaveNumber(self, waveNumber):
        self.waveLabel.element.text = ('Current Wave: ' + str(waveNumber))
        
    def updateCurrencyNumber(self, currencyNumber):
        self.currencyLabel.element.text = str(currencyNumber) + " Currency"
                
    def startNextWaveTimer(self):
        pyglet.clock.schedule_interval(self.updateNextWaveTimer, 1)
                
    def updateNextWaveTimer(self, dt):
        self.time -= dt
        self.timeLabel.element.text = ('Time until next Wave: ' +
                        str(round(self.time)) + ' Seconds')
        if (self.time <= 0):
            self.timeLabel.element.text =('GO')
            pyglet.clock.unschedule(self.updateNextWaveTimer)
            self.dispatch_event('on_next_wave_timer_finished')
            self.time = self.timeBetweenWaves

    def addCellSelectorSprite(self):
        self.cellSelectorSpriteRed = cocos.sprite.Sprite("assets/selector0.png")
        self.cellSelectorSpriteBlue = cocos.sprite.Sprite("assets/selector1.png")
        self.cellSelectorSpriteRed.position = 960, 540
        self.cellSelectorSpriteBlue.position = 960, 540
        self.cellSelectorSpriteBlue.visible = False
        self.cellSelectorSpriteRed.visible = False
        self.add(self.cellSelectorSpriteRed)
        self.add(self.cellSelectorSpriteBlue)
        (self.lastGrid_x, self.lastGrid_y) = self.cellSelectorSpriteRed.position
        self.lastGrid_x = int(self.lastGrid_x / 60) -1
        self.lastGrid_y = int(self.lastGrid_y / 60) -1

    def removeTowerBuildingHud(self):
        for picture in range (0, len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
        self.buildingHudDisplayed = False

    def buildTower(self, towerNumber):
        clicked_x = int(self.clicked_x / 60) * 60 + 30
        clicked_y = int(self.clicked_y / 60) * 60 + 30
        self.dispatch_event('on_build_tower', towerNumber, clicked_x, clicked_y)

    def displayTowerHud(self, kind, x, y):
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
        if kind == "build":
            for picture in range (0, len(self.towerThumbnails)):
                #use self.menuMin_x to center the menu below the coursor in x direction
                #ATTENTION, cocos2d always draws the CENTER of the sprite at the specified location
                self.towerThumbnails[picture].position = (self.menuMin_x + picture*self.towerThumbnails[picture].width + self.towerThumbnails[picture].width/2, y)
                self.add(self.towerThumbnails[picture])
            self.buildingHudDisplayed = True
        elif kind == "upgrade":
            pass

    # check WHETHER the click was on Hud Item
    def clickedOnTowerHudItem(self, x, y):
        #check if player clicked on a menu item
        #if yes, carry out the attached action (build/upgrade/cash-in tower)
        if y < self.menuMax_y + self.towerThumbnails[0].height / 2 and y > self.menuMin_y:
            #TODO: performance wise smart to check if menu being clicked instead of straight out jumping into the loop?
            if x > self.menuMin_x and x < self.menuMax_x:
                for i in range (0, len(self.towerThumbnails)):
                    if x > self.menuMin_x + i * self.towerThumbnails[i].width and x < self.menuMax_x - (len(self.towerThumbnails) - i - 1) * self.towerThumbnails[i].width:
                        return i
        return -1

    def on_mouse_release(self, x, y, buttons, modifiers):
        #TODO: only trigger if user clicked on buildable area
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        # check if user clicked on tower
        if 3 == self.currentCellStatus and False == self.buildingHudDisplayed:
            self.displayTowerHud("upgrade", x, y - self.towerThumbnails[0].height / 2)
            return
        if False == self.buildingHudDisplayed:
            #to store where tower has to be build
            #TODO: snap to grid
            self.clicked_x = x
            self.clicked_y = y
            self.displayTowerHud("build", self.clicked_x, self.clicked_y - self.towerThumbnails[0].height)
        else:
            hudItem = self.clickedOnTowerHudItem(x, y)
            if hudItem != -1:
                self.buildTower(hudItem)
                self.removeTowerBuildingHud()
            elif hudItem == -1:
                self.removeTowerBuildingHud()
                
    def on_mouse_motion(self, x, y, dx, dy):
        #class to highlight currently selected cell
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.dispatch_event('on_user_mouse_motion', x, y)
        grid_x = int(x / 60) 
        grid_y = int(y / 60) 
        if self.lastGrid_x != grid_x or self.lastGrid_y != grid_y:
            if self.currentCellStatus <= 1:
                self.cellSelectorSpriteBlue.visible = False
                self.cellSelectorSpriteRed.position = (grid_x * 60 + 30, grid_y * 60 + 30)
                self.cellSelectorSpriteRed.visible = True
            elif self.currentCellStatus > 1:
                self.cellSelectorSpriteRed.visible = False
                self.cellSelectorSpriteBlue.position = (grid_x * 60 + 30, grid_y * 60 + 30)
                self.cellSelectorSpriteBlue.visible = True
        

PyFenseHud.register_event_type('on_build_tower')
PyFenseHud.register_event_type('on_next_wave_timer_finished')
PyFenseHud.register_event_type('on_user_mouse_motion')
