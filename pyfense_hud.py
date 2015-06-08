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
        # load tower sprites here, so that they only have to be loaded once
        # TODO: create a loop to load images
        # TODO: gracefully fail if pictures fail to load? (try/catch)
        self.towerThumbnail1 = cocos.sprite.Sprite(
            pyfense_resources.tower[0][1]["image"])
        self.towerThumbnail2 = cocos.sprite.Sprite(
            pyfense_resources.tower[1][1]["image"])
        self.towerThumbnail3 = cocos.sprite.Sprite(
            pyfense_resources.tower[2][1]["image"])
        self.towerThumbnails = [self.towerThumbnail1,
                                self.towerThumbnail2, self.towerThumbnail3]
        self.noCashOverlay1 = cocos.sprite.Sprite(
            pyfense_resources.noCashOverlay)
        self.noCashOverlay2 = cocos.sprite.Sprite(
            pyfense_resources.noCashOverlay)
        self.noCashOverlay3 = cocos.sprite.Sprite(
            pyfense_resources.noCashOverlay)
        self.noCashOverlays = [self.noCashOverlay1,
                               self.noCashOverlay2,
                               self.noCashOverlay3]
        self.noCashOverlayDisplayed = [False for x in
                                       range(0, len(self.towerThumbnails))]
        # load selector to highlight currently selected cell
        self.addCellSelectorSprite()
        self.currentCellStatus = 0

    def displayStatusBar(self):
        self.waveLabel = cocos.text.Label('Current Wave: 1',
                                          anchor_x='center', anchor_y='center')
        w, h = cocos.director.director.get_window_size()
        self.waveLabel.position = w / 2, h - 30
        self.add(self.waveLabel)
        self.timeLabel = cocos.text.Label('Time until next Wave: ' +
                                          str(self.time) + ' Seconds',
                                          anchor_x='center', anchor_y='center')
        self.timeLabel.position = w / 2 - 250, h - 30
        self.add(self.timeLabel)
        self.liveLabel = cocos.text.Label('Remaining Lives: 30',
                                          anchor_x='center', anchor_y='center')
        self.liveLabel.position = w / 2 + 200, h - 30
        self.add(self.liveLabel)
        self.currentCurrency = 500
        self.currencyLabel = cocos.text.Label(str(self.currentCurrency) +
                                              ' Currency', anchor_x='center',
                                              anchor_y='center')
        self.currencyLabel.position = w / 2 + 350, h - 30
        self.add(self.currencyLabel)

    def updateLiveNumber(self, liveNumber):
        self.liveLabel.element.text = ("Remaining Lives: " + str(liveNumber))

    def updateWaveNumber(self, waveNumber):
        self.waveLabel.element.text = ('Current Wave: ' + str(waveNumber))

    def updateCurrencyNumber(self, currencyNumber):
        self.currencyLabel.element.text = str(currencyNumber) + " Currency"
        self.currentCurrency = currencyNumber

    def startNextWaveTimer(self):
        self.schedule_interval(self.updateNextWaveTimer, 1)

    def updateNextWaveTimer(self, dt):
        self.time -= dt
        self.timeLabel.element.text = ('Time until next Wave: ' +
                                       str(round(self.time)) + ' Seconds')
        if (self.time <= 0):
            self.timeLabel.element.text = ('GO')
            self.unschedule(self.updateNextWaveTimer)
            self.dispatch_event('on_next_wave_timer_finished')
            self.time = self.timeBetweenWaves

    def addCellSelectorSprite(self):
        self.cellSelectorSpriteRed = cocos.sprite.Sprite(
            pyfense_resources.selector0)
        self.cellSelectorSpriteBlue = cocos.sprite.Sprite(
            pyfense_resources.selector1)
        self.cellSelectorSpriteRed.position = 960, 540
        self.cellSelectorSpriteBlue.position = 960, 540
        self.cellSelectorSpriteBlue.visible = False
        self.cellSelectorSpriteRed.visible = False
        self.add(self.cellSelectorSpriteRed)
        self.add(self.cellSelectorSpriteBlue)

    def removeTowerBuildingHud(self):
        if self.buildingHudDisplayed == False:
            return
        for picture in range(0, len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
            if self.noCashOverlayDisplayed[picture] == True:
                self.remove(self.noCashOverlays[picture])
                self.noCashOverlayDisplayed[picture] = False
        self.buildingHudDisplayed = False

    def buildTower(self, towerNumber):
        clicked_x = int(self.clicked_x / 60) * 60 + 30
        clicked_y = int(self.clicked_y / 60) * 60 + 30
        self.dispatch_event('on_build_tower', towerNumber,
                            clicked_x, clicked_y)

    def displayTowerHud(self, kind, x, y):
        # displays the HUD to chose between towers to build
        # TODO: proper sourcing of available towers (read from settings?)
        # TODO: lower tower opacity if funds to build tower are insufficient
        # TODO: if player clicks on edge of map, shift HUD to still
        #   entirely display all buildable towers
        self.menuMin_x = x - floor(len(self.towerThumbnails)/2) * self.towerThumbnails[0].width - self.towerThumbnails[0].width / 2
        self.menuMax_x = x + floor(len(self.towerThumbnails)/2) * self.towerThumbnails[0].width + self.towerThumbnails[0].width / 2
        # only half subtracted because function is being called with
        # one half already subtracted
        # due to cocos2d assigning the sprite's center to specified location
        self.menuMin_y = y - self.towerThumbnails[0].height / 2
        self.menuMax_y = y
        # draw buildable tower array
        if kind == "build":
            for picture in range(0, len(self.towerThumbnails)):
                # use self.menuMin_x to center the menu below the
                # coursor in x direction
                # ATTENTION, cocos2d always draws the CENTER of the
                # sprite at the specified location
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    picture*self.towerThumbnails[picture].width +
                    self.towerThumbnails[picture].width/2, y)
                self.add(self.towerThumbnails[picture])
                if (self.currentCurrency < pyfense_resources.tower[picture][1]['cost']):
                    self.add(self.noCashOverlays[picture])
                    self.noCashOverlays[picture].position = (
                        self.menuMin_x +
                        picture*self.towerThumbnails[picture].width +
                        self.towerThumbnails[picture].width/2, y)
                    self.noCashOverlays[picture].opacity = 127
                    self.noCashOverlayDisplayed[picture] = True
            self.buildingHudDisplayed = True
        elif kind == "upgrade":
            pass

    # check WHETHER the click was on Hud Item
    def clickedOnTowerHudItem(self, x, y):
        # check if player clicked on an area where no tower can be built
        # check if player clicked on a menu item
        # if yes, carry out the attached action (build/upgrade/cash-in tower)
        if (y < self.menuMax_y + self.towerThumbnails[0].height / 2 and y > self.menuMin_y):
            # TODO: performance wise smart to check if menu being clicked instead of straight out jumping into the loop?
            if x > self.menuMin_x and x < self.menuMax_x:
                for i in range(0, len(self.towerThumbnails)):
                    if x > self.menuMin_x + i * self.towerThumbnails[i].width and x < self.menuMax_x - (len(self.towerThumbnails) - i - 1) * self.towerThumbnails[i].width:
                        return i
        return -1

    def on_mouse_release(self, x, y, buttons, modifiers):
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        # check if user clicked on tower
        # TODO: check on which tower the user actually clicked, indicated by towernr + 100
        if self.currentCellStatus == 3 and self.buildingHudDisplayed is False:
            self.displayTowerHud("upgrade", x, y - self.towerThumbnails[0].height / 2)
            return
        if False is self.buildingHudDisplayed and self.currentCellStatus == 2:
            #to store where tower has to be build
            #TODO: snap to grid
            self.clicked_x = x
            self.clicked_y = y
            self.displayTowerHud("build", self.clicked_x + 1.5 * self.towerThumbnails[0].height + 5, self.clicked_y - self.towerThumbnails[0].height / 2 - 5)
        elif self.currentCellStatus != 1 and self.currentCellStatus != 99:
            hudItem = self.clickedOnTowerHudItem(x, y)
            if hudItem != -1:
                self.buildTower(hudItem)
                self.removeTowerBuildingHud()
            elif hudItem == -1:
                self.removeTowerBuildingHud()

    def on_mouse_motion(self, x, y, dx, dy):
        # class to highlight currently selected cell
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.dispatch_event('on_user_mouse_motion', x, y)
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        if False is self.buildingHudDisplayed:
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
