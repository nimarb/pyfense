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

from pyfense import resources
from pyfense import highscore

font.add_directory(os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'assets'))
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
        nr_towers = len(resources.tower)
        y_pos = h / 2. + 300  # moves the lower bound of settings description

        text = []
        text.append(Label(
            '+++ Game Paused +++',
            font_name=_font_,
            font_size=30,
            anchor_x='center',
            anchor_y='center'))
        self.key_font = {
            'font_name': _font_,
            'font_size': 20,
            'anchor_x': 'center',
                        'anchor_y': 'center'
        }
        text.append(Label('Press Esc to resume game',
                          **self.key_font))
        text.append(Label('Press Q to quit game',
                          **self.key_font))
        text.append(Label('Press F to toggle Fullscreen',
                          **self.key_font))
        text.append(Label('Press V to toggle Vsync',
                          **self.key_font))
        text.append(Label('Press X to toggle FPS',
                          **self.key_font))
        text.append(Label('Press S to toggle Sound',
                          **self.key_font))

        text[0].position = w / 2., y_pos + 50
        self.add(text[0])

        text[1].position = w / 2., y_pos - 1 * (self.key_font['font_size'] + 8)
        text[2].position = w / 2., y_pos - 2 * (self.key_font['font_size'] + 8)
        text[3].position = w / 2., y_pos - 3 * (self.key_font['font_size'] + 8)
        text[4].position = w / 2., y_pos - 4 * (self.key_font['font_size'] + 8)
        text[5].position = w / 2., y_pos - 5 * (self.key_font['font_size'] + 8)
        text[6].position = w / 2., y_pos - 6 * (self.key_font['font_size'] + 8)

        for ele in text:
            # not working because pyglet raises a TypeError
            # in its event dispatcher:
            # ele.position = 400
            self.add(ele)

        # tower information

        self.damage_pic = resources.picto_damage
        self.rate_pic = resources.picto_rate

        for l in range(1, 4):  # loop over all upgrade levels
            self.towerDamagePic = []
            self.towerFireratePic = []
            self.towerThumbnails = []
            # add different tower thubnails
            try:
                for i in range(nr_towers):
                    self.towerThumbnails.append(cocos.sprite.Sprite(
                        resources.tower[i][l]["image"]))
            except KeyError:
                print("check your tower naming, first tower should start " +
                      "with 0 and no number should be left out.")
                nr_towers = 0
                break

            text_font = {
                'bold': True,
                'font_name': _font_,
                'anchor_x': "left",
                'anchor_y': 'center',
                'font_size': 16,
                'color': (255, 70, 0, 255)
            }

            # make labels for damage
            damage_label = []
            for i in range(nr_towers):
                damage_label.append(Label(" ", **text_font))
            self.towerDamageTexts = [n for n in damage_label]

            # make labels for firerate
            text_font['color'] = (0, 124, 244, 255)
            firerate_label = []
            for i in range(nr_towers):
                firerate_label.append(Label(" ", **text_font))
            self.towerFirerateTexts = [n for n in firerate_label]

            self.menuMin_x = (
                w / 2. - nr_towers / 2. * (
                    self.towerThumbnails[0].width + 40) +
                self.towerThumbnails[0].width / 4.)
            self.menuMin_y = 550

            for picture in range(0, nr_towers):
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
                    str(resources.tower[picture][l]["damage"]))
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
                    str(resources.tower[picture][l]["firerate"]))
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
            resources.sounds = not resources.sounds
            if(resources.music_player.playing):
                resources.music_player.pause()
            else:
                resources.music_player.play()
            return True
        elif k == key.Q:
            director.pop()
            director.replace(highscore.PyFenseLost())
            return True

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
