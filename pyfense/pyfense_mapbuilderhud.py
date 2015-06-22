import cocos
import pyglet
import pyfense_resources
from cocos import director


class PyFenseMapBuilderHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        # load selector to highlight currently selected cell
        self.addCellSelectorSprite()
        self.currentCCellStatus = 0

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

    def buildpath(self):
        clicked_x = int(self.clicked_x / 60) * 60 + 30
        clicked_y = int(self.clicked_y / 60) * 60 + 30
        self.dispatch_event("on_build_path", clicked_x, clicked_y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.clicked_x = x
        self.clicked_y = y
        self.buildpath()

    def on_key_release(self, key, modifiers):
        if(key == 65293):  # == Enter
            # Why does this function gets called when opening Layer - bad fix ?
            # -  Have you tried on key press?
            try:
                self.first_time_called
                self.saveMap()
            except AttributeError:
                self.first_time_called = -1

    def saveMap(self):
        # TODO: hide FPS and cellSelctor doesnt work yet?
        self.cellSelectorSpriteBlue.visible = False
        director.show_FPS = False
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            'assets/lvlcustom.png')
        self.dispatch_event("on_save")
        self.cellSelectorSpriteBlue.visible = True
        director.show_FPS = True

    def on_mouse_motion(self, x, y, dx, dy):
        # class to highlight currently selected cell
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self.cellSelectorSpriteBlue.position = (
            grid_x * 60 + 30, grid_y * 60 + 30)
        self.cellSelectorSpriteBlue.visible = True

PyFenseMapBuilderHud.register_event_type('on_build_path')
PyFenseMapBuilderHud.register_event_type('on_save')
# PyFenseHud.register_event_type('on_user_mouse_motion')
