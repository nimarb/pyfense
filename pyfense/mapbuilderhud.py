import os
import cocos
import pyglet

from pyfense import resources
from cocos import director

root = os.path.dirname(os.path.abspath(__file__))
pathjoin = lambda x: os.path.join(root, x)


class PyFenseMapBuilderHud(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self._add_cell_selector_sprite()
        self.currentCellStatus = 0

    def _add_cell_selector_sprite(self):

        self.cellSelectorSpriteRed = cocos.sprite.Sprite(
            resources.selector0)
        self.cellSelectorSpriteBlue = cocos.sprite.Sprite(
            resources.selector1)
        self.cellSelectorSpriteRed.position = 960, 540
        self.cellSelectorSpriteBlue.position = 960, 540
        self.cellSelectorSpriteBlue.visible = False
        self.cellSelectorSpriteRed.visible = False
        self.add(self.cellSelectorSpriteRed)
        self.add(self.cellSelectorSpriteBlue)

    def _buildpath(self):
        clicked_x = int(self.clicked_x / 60) * 60 + 30
        clicked_y = int(self.clicked_y / 60) * 60 + 30
        self.dispatch_event("on_build_path", clicked_x, clicked_y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        self.clicked_x = x
        self.clicked_y = y
        self._buildpath()

    def on_key_press(self, key, modifiers):
        """
        Save the map by pressing Enter, restart the game afterwards to play
        the created map
        """
        if(key == 65293):  # == Enter
            self._save_map()

    def _save_map(self):
        """
        Creates a screenshot of the current image, which can be used as
        the background for a custom lvl
        """
        self.cellSelectorSpriteBlue.visible = False
        director.show_FPS = False
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            pathjoin('assets/lvlcustom.png'))
        self.dispatch_event("on_save")
        self.cellSelectorSpriteBlue.visible = True
        director.show_FPS = True

    def on_mouse_motion(self, x, y, dx, dy):
        """
        highlight the currently hovered cell with the cellSelector Sprite
        """
        (x, y) = cocos.director.director.get_virtual_coordinates(x, y)
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self.cellSelectorSpriteBlue.position = (
            grid_x * 60 + 30, grid_y * 60 + 30)
        self.cellSelectorSpriteBlue.visible = True

PyFenseMapBuilderHud.register_event_type('on_build_path')
PyFenseMapBuilderHud.register_event_type('on_save')
