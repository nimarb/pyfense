# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos
import pyglet
from math import floor
import pyfense_resources
from sys import platform as _platform #for OS check

class PyFenseHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.timeBetweenWaves = 3
        self.time = self.timeBetweenWaves
        self.displayStatusBar()
        self.buildingHudDisplayed = False
        # upgradeHudDisplayed is 0 if no Hud is displayed
        # it is 0.5 if the hud is displayed but no upgrade is displayed
        # eg if a tower is already at lvl 3, or has no upgrade
        # if an upgradeable tower is displayed, upgradeHudDisplayed takes the
        # value of: upgradeLevel
        self.upgradeHudDisplayed = 0
        self.startNextWaveTimer()
        # TODO: create a loop to load images
        self.towerThumbnail1 = cocos.sprite.Sprite(
            pyfense_resources.tower[0][1]["image"])
        self.towerThumbnail2 = cocos.sprite.Sprite(
            pyfense_resources.tower[1][1]["image"])
        self.towerThumbnail3 = cocos.sprite.Sprite(
            pyfense_resources.tower[2][1]["image"])
        self.towerThumbnails = [self.towerThumbnail1,
                                self.towerThumbnail2, self.towerThumbnail3]
        self.addTowerTexts()
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
                                       range(0, len(self.noCashOverlays))]
        self.destroyTowerIcon = cocos.sprite.Sprite(
            pyfense_resources.destroyTowerIcon)
        self.noTowerUpgradeIcon = cocos.sprite.Sprite(
            pyfense_resources.noTowerUpgradeIcon)
        self.addCellSelectorSprite()
        self.currentCellStatus = 0
        self.rangeIndicator = cocos.sprite.Sprite(pyfense_resources.range1920)
        self.add(self.rangeIndicator)
        self.rangeIndicator.visible = False

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
            pyfense_resources.selector1)
        self.cellSelectorSpriteGreen = cocos.sprite.Sprite(
            pyfense_resources.selector0)
        self.cellSelectorSpriteRed.position = 960, 540
        self.cellSelectorSpriteGreen.position = 960, 540
        self.cellSelectorSpriteGreen.visible = False
        self.cellSelectorSpriteRed.visible = False
        self.add(self.cellSelectorSpriteRed)
        self.add(self.cellSelectorSpriteGreen)

    def addTowerTexts(self):
        label1 = cocos.text.Label(" ", bold=True, anchor_x='center', 
            anchor_y='center', color=(255, 0, 0, 255))
        label2 = cocos.text.Label(" ", bold=True, anchor_x='center', 
            anchor_y='center', color=(255, 0, 0, 255))
        label3 = cocos.text.Label(" ", bold=True, anchor_x='center', 
            anchor_y='center', color=(255, 0, 0, 255))
        self.towerTexts = [label1, label2, label3]
        self.towerUpgradeText = cocos.text.Label(" ", bold=True, 
            anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))

    def removeTowerBuildingHud(self):
        if self.buildingHudDisplayed is False:
            return
        for picture in range(0, len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
            self.remove(self.towerTexts[picture])
            if self.noCashOverlayDisplayed[picture] == True:
                self.remove(self.noCashOverlays[picture])
                self.noCashOverlayDisplayed[picture] = False
        self.buildingHudDisplayed = False
        
    def removeTowerUpgradeHud(self):
        if self.upgradeHudDisplayed == 0:
            return
        self.remove(self.destroyTowerIcon)
        self.rangeIndicator.visible = False
        if self.upgradeHudDisplayed > 0.5:
            upgradeLevel = self.upgradeHudDisplayed
            if upgradeLevel < 3:
                self.remove(self.towerUpgradeThumbnail)
                self.remove(self.towerUpgradeText)
        elif self.upgradeHudDisplayed == 0.5:
            self.remove(self.noTowerUpgradeIcon)
        self.upgradeHudDisplayed = 0

    def buildTower(self, towerNumber):
        clicked_x = int(self.clicked_x / 60) * 60 + 30
        clicked_y = int(self.clicked_y / 60) * 60 + 30
        self.dispatch_event('on_build_tower', towerNumber,
                            clicked_x, clicked_y)
                            
    def upgradeTower(self):
        self.dispatch_event('on_upgrade_tower', 
            self.cellSelectorSpriteGreen.position)
        
    def destroyTower(self):
        self.dispatch_event('on_destroy_tower', 
            self.cellSelectorSpriteGreen.position)
            
    def displayRangeIndicator(self, nextUpgrade=False):
        towerNumber = int(str(self.clickedCellStatus)[1])
        if nextUpgrade is False:
            upgradeLevel = int(str(self.clickedCellStatus)[2])
        else:
            upgradeLevel = int(str(self.clickedCellStatus)[2]) + 1
        pos_x = int(self.clicked_x / 60) * 60 + 30
        pos_y = int(self.clicked_y / 60) * 60 + 30
        self.rangeIndicator.position = (pos_x, pos_y)
        towerRange = pyfense_resources.tower[towerNumber][upgradeLevel]['range']
        if _platform == "linux" or _platform == "linux2":
            self.rangeIndicator.scale = 10 * towerRange / 960 
        else:
            self.rangeIndicator.scale = towerRange / 960
        self.rangeIndicator.opacity = 100
        self.rangeIndicator.visible = True

    def displayTowerHud(self, kind, x, y):
        # displays the HUD to chose between towers to build
        self.menuMin_x = self.clicked_x + 5
        # only half subtracted because function is being called with
        # one half already subtracted
        # due to cocos2d assigning the sprite's center to specified location
        self.menuMin_y = y - self.towerThumbnails[0].height / 2
        self.menuMax_y = y
        # draw buildable tower array
        if kind == "build":
            self.menuMax_x = self.menuMin_x + len(self.towerThumbnails) * self.towerThumbnails[0].width
            for picture in range(0, len(self.towerThumbnails)):
                # ATTENTION, cocos2d always draws the CENTER of the
                # sprite at the specified location
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    picture*self.towerThumbnails[picture].width +
                    self.towerThumbnails[picture].width / 2, y)
                self.towerTexts[picture].element.text = str(pyfense_resources.tower[picture][1]["cost"])
                self.towerTexts[picture].position = (self.menuMin_x + 
                    picture*self.towerThumbnails[picture].width +
                    self.towerThumbnails[picture].width / 1.5, y - 
                    self.towerThumbnails[picture].height / 4)
                self.add(self.towerThumbnails[picture])
                self.add(self.towerTexts[picture])
                if (self.currentCurrency < pyfense_resources.tower[picture][1]['cost']):
                    self.add(self.noCashOverlays[picture])
                    self.noCashOverlays[picture].position = (
                        self.menuMin_x +
                        picture*self.towerThumbnails[picture].width +
                        self.towerThumbnails[picture].width / 2, y)
                    self.noCashOverlays[picture].opacity = 127
                    self.noCashOverlayDisplayed[picture] = True
            self.buildingHudDisplayed = True
        elif kind == "upgrade":
            self.menuMax_x = self.menuMin_x + 2 * self.destroyTowerIcon.width
            self.clickedCellStatus = self.currentCellStatus
            towerNumber = int(str(self.clickedCellStatus)[1])
            upgradeLevel = int(str(self.clickedCellStatus)[2])
            self.displayRangeIndicator()
            if upgradeLevel < 3:
                self.towerUpgradeThumbnail = cocos.sprite.Sprite(
                    #pyfense_resources.tower[towerNumber][3]["image"])
                    pyfense_resources.tower[towerNumber][upgradeLevel + 1]["image"])
                self.add(self.towerUpgradeThumbnail)
                self.towerUpgradeThumbnail.position = (self.menuMin_x + 
                    self.towerUpgradeThumbnail.width / 2, y)
                self.add(self.destroyTowerIcon)
                self.destroyTowerIcon.position = (self.menuMin_x + 
                    self.towerUpgradeThumbnail.width * 1.5, y)
                self.upgradeHudDisplayed = upgradeLevel
                self.towerUpgradeText.element.text = str(pyfense_resources.tower[towerNumber][upgradeLevel + 1]["cost"])
                self.towerUpgradeText.position = (self.menuMin_x + 
                    self.towerUpgradeThumbnail.width / 1.5, y - self.towerUpgradeThumbnail.width / 4)
                self.add(self.towerUpgradeText)
            else:
                self.add(self.noTowerUpgradeIcon)
                self.noTowerUpgradeIcon.position = (self.menuMin_x + 
                    self.noTowerUpgradeIcon.width / 2, y)
                self.add(self.destroyTowerIcon)
                self.destroyTowerIcon.position = (self.menuMin_x + 
                    self.destroyTowerIcon.width * 1.5, y)
                self.upgradeHudDisplayed = 0.5

    # check WHETHER the click was on Hud Item
    def clickedOnTowerHudItem(self, x, y):
        # check if player clicked on an area where no tower can be built
        # check if player clicked on a menu item
        # if yes, carry out the attached action (build/upgrade/cash-in tower)
        if self.buildingHudDisplayed is True:
            if (y < self.menuMax_y + self.towerThumbnails[0].height / 2 and y > self.menuMin_y):
                if x > self.menuMin_x and x < self.menuMax_x:
                    for i in range(0, len(self.towerThumbnails)):
                        if x > self.menuMin_x + i * self.towerThumbnails[i].width and x < self.menuMax_x - (len(self.towerThumbnails) - i - 1) * self.towerThumbnails[i].width:
                            return i
        elif self.upgradeHudDisplayed > 0:
            if (y < self.menuMax_y + self.destroyTowerIcon.height / 2 and y > self.menuMin_y):
                # a max of two items. need to manually change number incase a 3rd is needed
                if x > self.menuMin_x and x < self.menuMax_x:
                    for i in range(0, 2):
                        if x > self.menuMin_x + i * self.destroyTowerIcon.width and x < self.menuMin_x + (i + 1) * self.destroyTowerIcon.width:
                            return i
        return -1

    def on_mouse_release(self, x, y, buttons, modifiers):
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        # check if user clicked on tower
        if self.currentCellStatus > 3 and self.buildingHudDisplayed is False and self.upgradeHudDisplayed == 0:
            self.clicked_x = x
            self.clicked_y = y
            self.displayTowerHud("upgrade", self.clicked_x + len(self.towerThumbnails) / 2 * self.towerThumbnails[0].width + 5, self.clicked_y - self.towerThumbnails[0].height / 2 - 5)
        elif False is self.buildingHudDisplayed and self.currentCellStatus == 3 and self.upgradeHudDisplayed == 0:
            self.clicked_x = x
            self.clicked_y = y
            self.displayTowerHud("build", self.clicked_x + len(self.towerThumbnails) / 2 * self.towerThumbnails[0].width + 5, self.clicked_y - self.towerThumbnails[0].height / 2 - 5)
        elif self.upgradeHudDisplayed > 0 or self.buildingHudDisplayed is True:
            hudItem = self.clickedOnTowerHudItem(x, y)
            if hudItem != -1:
                if self.buildingHudDisplayed is True:
                    self.buildTower(hudItem)
                    self.removeTowerBuildingHud()
                elif self.upgradeHudDisplayed > 0:
                    if hudItem == 0:
                        self.upgradeTower()
                    elif hudItem == 1:
                        self.destroyTower()
                    self.removeTowerUpgradeHud()
            elif hudItem == -1:
                if self.buildingHudDisplayed is True:
                    self.removeTowerBuildingHud()
                elif self.upgradeHudDisplayed > 0:
                    self.removeTowerUpgradeHud()

    def on_mouse_motion(self, x, y, dx, dy):
        # selector to highlight currently selected cell
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.dispatch_event('on_user_mouse_motion', x, y)
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        if False is self.buildingHudDisplayed and self.upgradeHudDisplayed == 0:
            if self.currentCellStatus <= 2:
                self.cellSelectorSpriteGreen.visible = False
                self.cellSelectorSpriteRed.position = (grid_x * 60 + 30, grid_y * 60 + 30)
                self.cellSelectorSpriteRed.visible = True
            elif self.currentCellStatus > 2:
                self.cellSelectorSpriteRed.visible = False
                self.cellSelectorSpriteGreen.position = (grid_x * 60 + 30, grid_y * 60 + 30)
                self.cellSelectorSpriteGreen.visible = True
        if self.upgradeHudDisplayed > 0.5:
            if self.clickedOnTowerHudItem(x, y) == 0:
                self.displayRangeIndicator(nextUpgrade=True)
            else:
                self.displayRangeIndicator()

PyFenseHud.register_event_type('on_build_tower')
PyFenseHud.register_event_type('on_destroy_tower')
PyFenseHud.register_event_type('on_upgrade_tower')
PyFenseHud.register_event_type('on_next_wave_timer_finished')
PyFenseHud.register_event_type('on_user_mouse_motion')