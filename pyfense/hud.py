# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos
import pyglet
from pyfense import resources


class PyFenseHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.timeBetweenWaves = 3
        self.time = self.timeBetweenWaves
        self._display_status_bar()
        self.buildingHudDisplayed = False
        # upgradeHudDisplayed is 0 if no Hud is displayed
        # it is 0.5 if the hud is displayed but no upgrade is available
        # if an upgradeable tower is displayed, upgradeHudDisplayed takes the
        # value of the tower's upgradeLevel
        self.upgradeHudDisplayed = 0
        self.start_next_wave_timer()
        self.towerThumbnails = []
        for i in range(0, 5):
            self.towerThumbnails.append(cocos.sprite.Sprite(
                resources.tower[i][1]['image']))
        self.noCashOverlays = []
        for i in range(0, 5):
            self.noCashOverlays.append(cocos.sprite.Sprite(
                resources.noCashOverlay))
        self.noCashOverlayDisplayed = [False for x in
                                       range(0, len(self.noCashOverlays))]
        self.destroyTowerIcon = cocos.sprite.Sprite(
            resources.destroyTowerIcon)
        self.noTowerUpgradeIcon = cocos.sprite.Sprite(
            resources.noTowerUpgradeIcon)
        self._add_tower_texts()
        self._add_cell_selector_sprite()
        self.currentCellStatus = 0
        self.rangeIndicator = cocos.sprite.Sprite(resources.range1920)
        self.add(self.rangeIndicator)
        self.rangeIndicator.visible = False

    def _display_status_bar(self):
        self.waveLabel = cocos.text.Label('Current Wave: 1', bold=True,
                                          anchor_x='center',
                                          anchor_y='center',
                                          font_size=13)
        w, h = cocos.director.director.get_window_size()
        self.waveLabel.position = w / 2 - 50, h - 30
        self.add(self.waveLabel)
        self.timeLabel = cocos.text.Label(
            'Time until next Wave: ' + str(self.time) + ' Seconds', bold=True,
            anchor_x='center', anchor_y='center', font_size=13)
        self.timeLabel.position = w / 2 - 300, h - 30
        self.add(self.timeLabel)
        self.liveLabel = cocos.text.Label('Remaining Lives: 15', bold=True,
                                          anchor_x='center', anchor_y='center',
                                          font_size=13)
        self.liveLabel.position = w / 2 + 150, h - 30
        self.add(self.liveLabel)
        self.currentCurrency = 300
        self.currencyLabel = cocos.text.Label('$' + str(self.currentCurrency),
                                              anchor_x='center',
                                              bold=True, anchor_y='center',
                                              font_size=13)
        self.currencyLabel.position = w / 2 + 300, h - 30
        self.add(self.currencyLabel)

    def update_live_number(self, liveNumber):
        """Updates the number of current lives displayed in the Statusbar"""
        self.liveLabel.element.text = ("Remaining Lives: " + str(liveNumber))

    def update_wave_number(self, waveNumber):
        """Updates the number of the current Wave displayed in the Statusbar"""
        self.waveLabel.element.text = ('Current Wave: ' + str(waveNumber))

    def update_currency_number(self, currencyNumber):
        """Updates the number of current Cash displayed in the Statusbar"""
        self.currencyLabel.element.text = '$' + str(int(currencyNumber))
        self.currentCurrency = currencyNumber

    def start_next_wave_timer(self):
        """Starts the countdown timer to trigger the next wave"""
        self.schedule_interval(self._update_next_wave_timer, 1)

    def _update_next_wave_timer(self, dt):
        self.time -= dt
        self.timeLabel.element.text = ('Time until next Wave: ' +
                                       str(round(self.time)) + ' Seconds')
        if (self.time <= 0):
            self.timeLabel.element.text = ('GO')
            self.unschedule(self._update_next_wave_timer)
            self.dispatch_event('on_next_wave_timer_finished')
            self.time = self.timeBetweenWaves

    def _add_cell_selector_sprite(self):
        self.cellSelectorSpriteRed = cocos.sprite.Sprite(
            resources.selector1)
        self.cellSelectorSpriteGreen = cocos.sprite.Sprite(
            resources.selector0)
        self.cellSelectorSpriteGreen.visible = False
        self.cellSelectorSpriteRed.visible = False
        self.add(self.cellSelectorSpriteRed)
        self.add(self.cellSelectorSpriteGreen)

    def _add_tower_texts(self):
        labels = []
        for i in range(0, 5):
            labels.append(cocos.text.Label(" ", bold=True, anchor_x='right',
                          anchor_y='center', color=(255, 0, 0, 255)))
        self.towerCostTexts = [labels[0], labels[1], labels[2], labels[3],
                               labels[4]]
        self.towerUpgradeText = cocos.text.Label(
            " ", bold=True, anchor_x='center', anchor_y='center',
            color=(255, 0, 0, 255))

    def _remove_tower_building_hud(self):
        if not self.buildingHudDisplayed:
            return
        for picture in range(0, len(self.towerThumbnails)):
            self.remove(self.towerThumbnails[picture])
            self.remove(self.towerCostTexts[picture])
            if self.noCashOverlayDisplayed[picture]:
                self.remove(self.noCashOverlays[picture])
                self.noCashOverlayDisplayed[picture] = False
        self.rangeIndicator.visible = False
        self.buildingHudDisplayed = False

    def _remove_tower_upgrade_hud(self):
        if self.upgradeHudDisplayed == 0:
            return
        self.remove(self.destroyTowerIcon)
        self.rangeIndicator.visible = False
        if self.upgradeHudDisplayed > 0.5:
            upgradeLevel = self.upgradeHudDisplayed
            if upgradeLevel < 3:
                self.remove(self.towerUpgradeThumbnail)
                self.remove(self.towerUpgradeText)
                for i in range(0, len(self.noCashOverlayDisplayed)):
                    if self.noCashOverlayDisplayed[i]:
                        self.remove(self.noCashOverlays[i])
                        self.noCashOverlayDisplayed[i] = False
                        break
        elif self.upgradeHudDisplayed == 0.5:
            self.remove(self.noTowerUpgradeIcon)
        self.upgradeHudDisplayed = 0

    def _build_tower(self, towerNumber):
        # clicked_x = int(self.clicked_x / 60) * 60 + 30
        # clicked_y = int(self.clicked_y / 60) * 60 + 30
        (clicked_x, clicked_y) = self.cellSelectorSpriteGreen.position
        self.dispatch_event('on_build_tower', towerNumber,
                            clicked_x, clicked_y)

    def _upgrade_tower(self):
        self.dispatch_event('on_upgrade_tower',
                            self.cellSelectorSpriteGreen.position)

    def _destroy_tower(self):
        self.dispatch_event('on_destroy_tower',
                            self.cellSelectorSpriteGreen.position)

    def _display_range_indicator(self, nextUpgrade=False, towerNumber=None,
                                 upgradeLevel=None):
        if towerNumber is None:
            towerNumber = int(str(self.clickedCellStatus)[1])
        if not nextUpgrade:
            if upgradeLevel is not None:
                upgradeLevel = int(str(self.clickedCellStatus)[2])
            else:
                upgradeLevel = 1
        else:
            upgradeLevel = int(str(self.clickedCellStatus)[2]) + 1
        pos_x = int(self.clicked_x / 60) * 60 + 30
        pos_y = int(self.clicked_y / 60) * 60 + 30
        self.rangeIndicator.position = (pos_x, pos_y)
        towerRange = (resources.tower[towerNumber][upgradeLevel]['range'])
        self.rangeIndicator.scale = towerRange / 960
        self.rangeIndicator.opacity = 100  # value between 0 and 255
        self.rangeIndicator.visible = True

    def _display_tower_hud(self, kind, x, y):
        # displays the HUD to chose between towers to build
        self.menuMin_x = self.clicked_x + 5
        # only half subtracted because function is being called with
        # one half already subtracted
        # due to cocos2d assigning the sprite's center to specified location
        self.menuMin_y = y - self.towerThumbnails[0].height / 2
        self.menuMax_y = y

        # draw buildable tower array
        if kind == "build":
            self.menuMax_x = (self.menuMin_x + len(self.towerThumbnails) *
                              self.towerThumbnails[0].width)
            maxX = resources.settings['window']['width']
            if self.menuMax_x > maxX:
                self.menuMax_x = maxX
                self.menuMin_x = (self.menuMax_x -
                                  (len(self.towerThumbnails) *
                                   self.towerThumbnails[0].width))
            for picture in range(0, len(self.towerThumbnails)):
                # ATTENTION, cocos2d always draws the CENTER of the
                # sprite at the specified location
                # old hud positioning: not dynamically adjusting:
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    picture * self.towerThumbnails[picture].width +
                    self.towerThumbnails[picture].width / 2, y)
                self.towerCostTexts[picture].element.text = '$' + str(
                    resources.tower[picture][1]["cost"])
                self.towerCostTexts[picture].position = (
                    self.menuMin_x + picture *
                    self.towerThumbnails[picture].width +
                    self.towerThumbnails[picture].width / 1.5 + 15,
                    y - self.towerThumbnails[picture].width * 0.55)
                self.add(self.towerThumbnails[picture])
                self.add(self.towerCostTexts[picture])
                if (self.currentCurrency <
                        resources.tower[picture][1]['cost']):
                    self.add(self.noCashOverlays[picture])
                    self.noCashOverlays[picture].position = (
                        self.menuMin_x +
                        picture * self.towerThumbnails[picture].width +
                        self.towerThumbnails[picture].width / 2, y)
                    self.noCashOverlays[picture].opacity = 127
                    self.noCashOverlayDisplayed[picture] = True
            self.buildingHudDisplayed = True

        elif kind == "upgrade":
            self.menuMax_x = self.menuMin_x + 2 * self.destroyTowerIcon.width
            maxX = resources.settings['window']['width']
            if self.menuMax_x > maxX:
                self.menuMax_x = maxX
                self.menuMin_x = self.menuMax_x - (2 *
                                                   self.destroyTowerIcon.width)
            self.clickedCellStatus = self.currentCellStatus
            towerNumber = int(str(self.clickedCellStatus)[1])
            upgradeLevel = int(str(self.clickedCellStatus)[2])
            self._display_range_indicator(upgradeLevel=upgradeLevel)
            if upgradeLevel < 3:
                self.towerUpgradeThumbnail = cocos.sprite.Sprite(
                    resources.tower
                    [towerNumber][upgradeLevel + 1]["image"])
                self.add(self.towerUpgradeThumbnail)
                self.towerUpgradeThumbnail.position = (
                    self.menuMin_x + self.towerUpgradeThumbnail.width / 2, y)
                self.add(self.destroyTowerIcon)
                self.destroyTowerIcon.position = (
                    self.menuMin_x + self.towerUpgradeThumbnail.width * 1.5, y)
                self.upgradeHudDisplayed = upgradeLevel
                self.towerUpgradeText.element.text = str(
                    resources.tower
                    [towerNumber][upgradeLevel + 1]["cost"]) + '$'
                self.towerUpgradeText.position = (
                    self.menuMin_x +
                    self.towerUpgradeThumbnail.width / 1.5,
                    y - self.towerUpgradeThumbnail.width * 0.55)
                self.add(self.towerUpgradeText)
                if (self.currentCurrency <
                        resources.tower[towerNumber]
                        [upgradeLevel + 1]['cost']):
                    self.add(self.noCashOverlays[towerNumber])
                    self.noCashOverlays[towerNumber].position = (
                        self.menuMin_x +
                        self.towerThumbnails[towerNumber].width / 2, y)
                    self.noCashOverlays[towerNumber].opacity = 127
                    self.noCashOverlayDisplayed[towerNumber] = True
            else:
                self.add(self.noTowerUpgradeIcon)
                self.noTowerUpgradeIcon.position = (
                    self.menuMin_x + self.noTowerUpgradeIcon.width / 2, y)
                self.add(self.destroyTowerIcon)
                self.destroyTowerIcon.position = (
                    self.menuMin_x + self.destroyTowerIcon.width * 1.5, y)
                self.upgradeHudDisplayed = 0.5

    def _mouse_on_tower_hud_item(self, x, y):
        # check if player clicked on an area where no tower can be built
        # check if player clicked on a menu item
        # if yes, carry out the attached action (build/upgrade/cash-in tower)
        if self.buildingHudDisplayed:
            if (y < self.menuMax_y + self.towerThumbnails[0].height / 2 and
                    y > self.menuMin_y):
                if x > self.menuMin_x and x < self.menuMax_x:
                    for i in range(0, len(self.towerThumbnails)):
                        if (x > self.menuMin_x + i *
                                self.towerThumbnails[i].width and
                                x < self.menuMax_x -
                                (len(self.towerThumbnails) - i - 1) *
                                self.towerThumbnails[i].width):
                            return i
        elif self.upgradeHudDisplayed > 0:
            if (y < self.menuMax_y + self.destroyTowerIcon.height / 2 and
                    y > self.menuMin_y):
                # a max of two items.
                # need to manually change number incase a 3rd is needed
                if x > self.menuMin_x and x < self.menuMax_x:
                    for i in range(0, 2):
                        if (x > self.menuMin_x + i *
                                self.destroyTowerIcon.width and
                                x < self.menuMin_x + (i + 1) *
                                self.destroyTowerIcon.width):
                            return i
        return -1

    def on_mouse_release(self, x, y, buttons, modifiers):
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        # check if user clicked on tower
        if (self.currentCellStatus > 3 and not self.buildingHudDisplayed and
                self.upgradeHudDisplayed == 0):
            self.clicked_x = x
            self.clicked_y = y
            self._display_tower_hud(
                "upgrade", self.clicked_x + len(self.towerThumbnails) / 2 *
                self.towerThumbnails[0].width + 5, self.clicked_y -
                self.towerThumbnails[0].height / 2 - 5)
        elif (not self.buildingHudDisplayed and
                self.currentCellStatus == 3 and self.upgradeHudDisplayed == 0):
            self.clicked_x = x
            self.clicked_y = y
            self._display_tower_hud(
                "build", self.clicked_x + len(self.towerThumbnails) / 2 *
                self.towerThumbnails[0].width + 5, self.clicked_y -
                self.towerThumbnails[0].height / 2 - 5)
        elif self.upgradeHudDisplayed > 0 or self.buildingHudDisplayed:
            hudItem = self._mouse_on_tower_hud_item(x, y)
            if hudItem != -1:
                if self.buildingHudDisplayed:
                    self._build_tower(hudItem)
                    self._remove_tower_building_hud()
                elif self.upgradeHudDisplayed > 0:
                    if hudItem == 0:
                        self._upgrade_tower()
                    elif hudItem == 1:
                        self._destroy_tower()
                    self._remove_tower_upgrade_hud()
            elif hudItem == -1:
                if self.buildingHudDisplayed:
                    self._remove_tower_building_hud()
                elif self.upgradeHudDisplayed > 0:
                    self._remove_tower_upgrade_hud()
        # self.on_mouse_motion(x, y, x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        # selector to highlight currently selected cell
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.dispatch_event('on_user_mouse_motion', x, y)
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        if not self.buildingHudDisplayed and self.upgradeHudDisplayed == 0:
            if self.currentCellStatus <= 2:
                self.cellSelectorSpriteGreen.visible = False
                self.cellSelectorSpriteRed.position = (grid_x * 60 + 30,
                                                       grid_y * 60 + 30)
                self.cellSelectorSpriteRed.visible = True
            elif self.currentCellStatus > 2:
                self.cellSelectorSpriteRed.visible = False
                self.cellSelectorSpriteGreen.position = (grid_x * 60 + 30,
                                                         grid_y * 60 + 30)
                self.cellSelectorSpriteGreen.visible = True
        elif self.upgradeHudDisplayed > 0.5:
            if self._mouse_on_tower_hud_item(x, y) == 0:
                self._display_range_indicator(nextUpgrade=True)
            else:
                upLevel = int(str(self.clickedCellStatus)[2])
                self._display_range_indicator(upgradeLevel=upLevel)
        elif self.buildingHudDisplayed:
            towerOrderNumber = self._mouse_on_tower_hud_item(x, y)
            if towerOrderNumber == 0:
                self._display_range_indicator(towerNumber=0)
            elif towerOrderNumber == 1:
                self._display_range_indicator(towerNumber=1)
            elif towerOrderNumber == 2:
                self._display_range_indicator(towerNumber=2)
            elif towerOrderNumber == 3:
                self._display_range_indicator(towerNumber=3)
            elif towerOrderNumber == 4:
                self._display_range_indicator(towerNumber=4)
            else:
                self.rangeIndicator.visible = False


PyFenseHud.register_event_type('on_build_tower')
PyFenseHud.register_event_type('on_destroy_tower')
PyFenseHud.register_event_type('on_upgrade_tower')
PyFenseHud.register_event_type('on_next_wave_timer_finished')
PyFenseHud.register_event_type('on_user_mouse_motion')
