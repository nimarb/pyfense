
"""
pyfense_pause.py
contains class layer which is displayed when pressing esc
"""

import os

from pyglet.window import key
from pyglet import font

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import Label
from cocos.layer import Layer

from pyfense import pyfense_resources

font.add_directory(os.path.join(
                os.path.dirname(
                os.path.abspath(__file__)), 'data/Orbitron'))
_font_ = 'Orbitron Light'


class PyFensePause(scene.Scene):

    def __init__(self):
        super().__init__()
        self.add(PauseLayer(), z=1)


class PauseLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()
        y_pos = h/2. + 300

        text0 = Label(
            '+++ Game Paused +++',
            font_name=_font_,
            font_size=30,
            anchor_x='center',
            anchor_y='center')

        self.key_font = {}
        self.key_font['font_name'] = '_font_'
        self.key_font['font_size'] = 20
        self.key_font['anchor_x'] = 'center'
        self.key_font['anchor_y'] = 'center'

        text1 = Label('Press Esc to resume game',
                      **self.key_font)
        text2 = Label('Press Q to quit game',
                      **self.key_font)
        text3 = Label('Press F to toggle Fullscreen',
                      **self.key_font)
        text4 = Label('Press V to toggle Vsync',
                      **self.key_font)
        text5 = Label('Press X to toggle FPS',
                      **self.key_font)
        text6 = Label('Press S to toggle Sound',
                      **self.key_font)

        text0.position = w/2., y_pos + 50
        text1.position = w/2., y_pos - 1 * (self.key_font['font_size'] + 8)
        text2.position = w/2., y_pos - 2 * (self.key_font['font_size'] + 8)
        text3.position = w/2., y_pos - 3 * (self.key_font['font_size'] + 8)
        text4.position = w/2., y_pos - 4 * (self.key_font['font_size'] + 8)
        text5.position = w/2., y_pos - 5 * (self.key_font['font_size'] + 8)
        text6.position = w/2., y_pos - 6 * (self.key_font['font_size'] + 8)

        self.add(text0)
        self.add(text1)
        self.add(text2)
        self.add(text3)
        self.add(text4)
        self.add(text5)
        self.add(text6)

        # tower information

        self.damage_pic = pyfense_resources.picto_damage
        self.rate_pic = pyfense_resources.picto_rate

        for l in range(1, 4):  # loop over all upgrade levels
            self.towerDamagePic = []
            self.towerFireratePic = []
            self.towerThumbnails = []
            for i in range(0, 3):
                self.towerThumbnails.append(cocos.sprite.Sprite(
                    pyfense_resources.tower[i][l]["image"]))

            text_font = {
                'bold': True,
                'anchor_x': "left",
                'anchor_y': 'center',
                'font_size': 16,
                'color': (255, 70, 0, 255)
                }

            label4 = Label(" ", **text_font)
            label5 = Label(" ", **text_font)
            label6 = Label(" ", **text_font)
            self.towerDamageTexts = [label4, label5, label6]

            text_font['color'] = (0, 124, 244, 255)

            label7 = Label(" ", **text_font)
            label8 = Label(" ", **text_font)
            label9 = Label(" ", **text_font)
            self.towerFirerateTexts = [label7, label8, label9]

            self.menuMin_x = (
                w/2. - self.towerThumbnails[0].width * (4 / 3) - 60)
            self.menuMin_y = 550

            for picture in range(0, len(self.towerThumbnails)):
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    picture * (self.towerThumbnails[picture].width + 40) +
                    self.towerThumbnails[picture].width / 2,
                    -(l - 1) * (self.towerThumbnails[picture].width + 75) +
                    self.menuMin_y)

                self.towerDamagePic.append(
                    cocos.sprite.Sprite(self.damage_pic))
                self.towerDamagePic[picture].position = (
                    self.menuMin_x + picture *
                    (self.towerThumbnails[picture].width + 40) +
                    self.towerThumbnails[picture].width / 1.5 - 37,
                    self.menuMin_y -
                    self.towerThumbnails[picture].width / 2 - 10 -
                    (l - 1) * (self.towerThumbnails[picture].width + 75))

                self.towerDamageTexts[picture].element.text = (
                    str(pyfense_resources.tower[picture][l]["damage"] *
                        pyfense_resources.tower[picture][l]["firerate"] / 1.))
                self.towerDamageTexts[picture].position = (
                    self.menuMin_x + picture *
                    (self.towerThumbnails[picture].width + 40) +
                    self.towerThumbnails[picture].width / 1.5 - 19,
                    self.menuMin_y -
                    self.towerThumbnails[picture].width / 2 - 10 -
                    (l - 1) * (self.towerThumbnails[picture].width + 75))

                self.towerFireratePic.append(
                    cocos.sprite.Sprite(self.rate_pic))
                self.towerFireratePic[picture].position = (
                    self.menuMin_x + picture *
                    (self.towerThumbnails[picture].width + 40) +
                    self.towerThumbnails[picture].width / 1.5 - 37,
                    self.menuMin_y -
                    self.towerThumbnails[picture].width / 2 - 38 -
                    (l - 1) * (self.towerThumbnails[picture].width + 75))

                self.towerFirerateTexts[picture].element.text = (
                    str(pyfense_resources.tower[picture][l]["firerate"]))
                self.towerFirerateTexts[picture].position = (
                    self.menuMin_x + picture *
                    (self.towerThumbnails[picture].width + 40) +
                    self.towerThumbnails[picture].width / 1.5 - 19,
                    self.menuMin_y -
                    self.towerThumbnails[picture].width / 2 - 38 -
                    (l - 1) * (self.towerThumbnails[picture].width + 75))

                self.add(self.towerThumbnails[picture])
                self.add(self.towerDamageTexts[picture])
                self.add(self.towerFirerateTexts[picture])
                self.add(self.towerDamagePic[picture])
                self.add(self.towerFireratePic[picture])

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            director.pop()
            return True
        elif k == key.F:
            director.window.set_fullscreen(not director.window.fullscreen)
            return True
        elif k == key.V:
            director.window.set_vsync(not director.window.vsync)
            return True
        elif k == key.X:
            director.show_FPS = not director.show_FPS
            return True
        elif k == key.S:
            pyfense_resources.sounds = not pyfense_resources.sounds
            if(pyfense_resources.music_player.playing):
                pyfense_resources.music_player.pause()
            else:
                pyfense_resources.music_player.play()
            return True
        elif k == key.Q:
            director.pop()
            director.pop()
            return True

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
