"""
Modified ImageMenuItem Class to show pictures in the Menu without scaling
or overlapping
"""

import pyglet

import cocos
import cocos.menu


class ImageMenuItem (cocos.menu.BaseMenuItem):
    """ A menu item that shows a selectable Image without scaling"""
    def __init__(self, image, callback_func, *args, **kwargs):
        if isinstance(image, cocos.menu.string_types):
            image = pyglet.image.load(image)
        self.image = image
        super(ImageMenuItem, self).__init__(callback_func, *args, **kwargs)

    def generateWidgets(self, pos_x, pos_y, font_item, font_item_selected):
        anchors = {'left': 0, 'center': 0.5, 'right': 1, 'top': 1, 'bottom': 0}
        anchor = (anchors[font_item['anchor_x']] * self.image.width,
                  anchors[font_item['anchor_y']] * self.image.height)
        self.item = cocos.sprite.Sprite(self.image,
                                        anchor=anchor, opacity=255,
                                        color=font_item['color'][:3])
#        self.item.scale = font_item['font_size'] / float(self.item.height)
        # position modified: addition term for pos_y
        self.item.position = int(pos_x), int(pos_y + (self.image.height/2.))
        self.selected_item = (
            cocos.sprite.Sprite(self.image, anchor=anchor,
                                color=font_item_selected['color'][:3]))
#        self.selected_item.scale = (font_item_selected['font_size'] /
#                                    float(self.selected_item.height))
        self.selected_item.position = int(pos_x), int(pos_y +
                                                      (self.image.height/2.))

    def draw(self):
        pyglet.gl.glPushMatrix()
        self.transform()
        if self.is_selected:
            self.selected_item.draw()
        else:
            self.item.draw()
        pyglet.gl.glPopMatrix()
