"""
Mainfile, draws Menu including Level Select, Highscore, Options and About page.
Reads settings from /data/settings.txt #TODO, About from /data/about.txt #TODO
and gets Highscore data from pyfense_highscore. Level Select starts game with
selected level from pyfense_game.
"""

import pyglet
from pyglet.window import key

import cocos
from cocos.director import director
from cocos.actions import *
from cocos.scene import Scene
from cocos.layer import *
from cocos.text import *

import os

from pyfense_modmenu import *
import pyfense_game
import pyfense_mapBuilder
import pyfense_highscore
import pyfense_resources


class MainMenu(Menu):
    def __init__(self):
        super().__init__('PyFense')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        items = []
        items.append(MenuItem('Start Game', self.on_level_select))
        items.append(MenuItem('Scores', self.on_scores))
        items.append(MenuItem('Settings', self.on_settings))
        items.append(MenuItem('Help', self.on_help))
        items.append(MenuItem('About', self.on_about))
        items.append(MenuItem('Exit', self.on_quit))
        self.create_menu(items)

    def on_level_select(self):
        self.parent.switch_to(1)

    def on_settings(self):
        self.parent.switch_to(2)

    def on_scores(self):
        self.parent.switch_to(3)

    def on_help(self):
        self.parent.switch_to(4)

    def on_about(self):
        self.parent.switch_to(5)

    def on_quit(self):
        pyglet.app.exit()


class LevelSelectMenu(Menu):
    def __init__(self):
        super().__init__('PyFense')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        items = []
        image_lvl1 = pyfense_resources.background["lvl1"]
        lvl1 = ImageMenuItem(image_lvl1, lambda: self.on_start(1))
        lvl1.scale = 0.28
        lvl1.y = 0
        items.append(lvl1)
        MapBuilder = MenuItem('MapBuilder', self.on_mapBuilder)
        MapBuilder.y -= 20
        Back = MenuItem('Back', self.on_quit)
        Back.y -= 20
        if(os.path.isfile("assets/lvlcustom.png")):
            customImage = pyfense_resources.loadImage('assets/lvlcustom.png')
            customItem = ImageMenuItem(customImage,
                                       lambda: self.on_start("custom"))
            customItem.scale = 0.4
            customItem.y -= 300
            items.append(customItem)
            MapBuilder.y -= 320
            Back.y -= 320
            # custom map has to be position correctly in Menu
        items.extend([MapBuilder, Back])
        width, height = director.get_window_size()
        self.create_menu(items)

    def on_start(self, lvl):
        director.push(pyfense_game.PyFenseGame(lvl))

    def on_mapBuilder(self):
        director.push(pyfense_mapBuilder.PyFenseMapBuilder())

    def on_quit(self):
        self.parent.switch_to(0)


class ScoresLayer(ColorLayer):
    is_event_handler = True
    fontsize = 40

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h-86)
        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] = 'top'
        self.font_title['anchor_x'] = 'center'
        title = Label('PyFense', **self.font_title)
        title.position = (w/2., h)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super().on_enter()
        score = pyfense_highscore.get_score()
        if self.table:
            self.remove_old()
        self.table = []
        Head_Pos = Label('',
                         bold=True,
                         font_name='Arial',
                         font_size=self.fontsize,
                         anchor_x='right',
                         anchor_y='top')
        Head_Name = Label('Name',
                          bold=True,
                          font_name='Arial',
                          font_size=self.fontsize,
                          anchor_x='left',
                          anchor_y='top')
        Head_Score = Label('Score',
                           bold=True,
                           font_name='Arial',
                           font_size=self.fontsize,
                           anchor_x='right',
                           anchor_y='top')
        Head_Level = Label('Reached Level',
                           bold=True,
                           font_name='Arial',
                           font_size=self.fontsize,
                           anchor_x='center',
                           anchor_y='top')
        self.table.append((Head_Pos, Head_Name, Head_Score, Head_Level))
        self.table.append((Label(''), Label(''), Label(''), Label('')))

        for i, entry in enumerate(score):
            pos = Label('%i.    ' % (i+1),
                        font_name='Arial',
                        font_size=self.fontsize,
                        anchor_x='right',
                        anchor_y='top')
            name = Label(entry[0],
                         font_name='Arial',
                         font_size=self.fontsize,
                         anchor_x='left',
                         anchor_y='top')
            score = Label(entry[1],
                          font_name='Arial',
                          font_size=self.fontsize,
                          anchor_x='right',
                          anchor_y='top')
            level = Label(entry[2].strip(),
                          font_name='Arial',
                          font_size=self.fontsize,
                          anchor_x='right',
                          anchor_y='top')
            self.table.append((pos, name, score, level))
        self.process_table()

    def remove_old(self):
        for item in self.table:
            pos, name, score, level = item
            self.remove(pos)
            self.remove(name)
            self.remove(score)
            self.remove(level)
        self.table = None

    def process_table(self):
        w, h = director.get_window_size()
        for i, item in enumerate(self.table):
            pos, name, score, level = item
            pos_y = h-200 - (self.fontsize + 15) * i
            pos.position = (w/2 - 400., pos_y)
            name.position = (w/2 - 380., pos_y)
            score.position = (w/2 + 130., pos_y)
            level.position = (w/2 + 430, pos_y)
            self.add(pos, z=2)
            self.add(name, z=2)
            self.add(score, z=2)
            self.add(level, z=2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True

class OptionsMenu(Menu):
    def __init__(self):
        super().__init__('PyFense')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        items = []
        items.append(ToggleMenuItem('Show FPS: ', self.on_show_fps,
                     director.show_FPS))
        items.append(ToggleMenuItem('Sounds', self.on_sounds, True))
        items.append(MenuItem('Back', self.on_quit))
        self.create_menu(items)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_sounds(self, value):
        pyfense_resources.sounds = not pyfense_resources.sounds

    def on_quit(self):
        self.parent.switch_to(0)


class HelpLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h-86)
        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] = 'top'
        self.font_title['anchor_x'] = 'center'
        title = Label('PyFense', **self.font_title)
        title.position = (w/2., h)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super().on_enter()
        w, h = director.get_window_size()
        text = Label('Press Q to quit the running level',
                     font_name='Arial',
                     font_size=20,
                     anchor_x='center',
                     anchor_y='center')
        text.position = w/2., h/2.
        self.add(text)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


class AboutLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h-86)
        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] = 'top'
        self.font_title['anchor_x'] = 'center'
        title = Label('PyFense', **self.font_title)
        title.position = (w/2., h)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super(ou).on_enter()
        w, h = director.get_window_size()
        text = Label('PyFense ist geil und wir lieben Nippel!',  # LOL
                     font_name='Arial',
                     font_size=20,
                     anchor_x='center',
                     anchor_y='center')
        text.position = w/2., h/2.
        self.add(text)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


def to_menu(item):
    scene = Scene()
    scene.add(MultiplexLayer(
        MainMenu(),
        LevelSelectMenu(),
        OptionsMenu(),
        ScoresLayer(),
        HelpLayer(),
        AboutLayer()
        ),
        z=1)
    director.replace(scene)

if __name__ == '__main__':
    director.init(**pyfense_resources.settings['window'])
    scene = Scene()
    scene.add(MultiplexLayer(
        MainMenu(),
        LevelSelectMenu(),
        OptionsMenu(),
        ScoresLayer(),
        HelpLayer(),
        AboutLayer()
        ),
        z=1)
    director.set_show_FPS(pyfense_resources.settings["general"]["showFps"])
    w, h = director.get_window_size()
    # Music
    # 1st Try - doesnt play anything
    # scene.load_music("assets/music.wav")
    # scene.play_music()

    # 2nd Try - static noise louder than music
    # music = pyglet.resource.media("assets/music.wav", streaming = True)
    # music.play()

    # 3rd Try - music stops after ca. 1 min (even when piece was longer)
    # and doesnt repeat as it should
    # music_player = pyglet.medi    a.Player()
    # music = pyglet.resource.media("assets/music.wav", streaming = False)
    # music_player.queue(music)
    # music_player.eos_action = music_player.EOS_LOOP
    # music_player.play()

    logo = pyfense_resources.logo
    scene.add(cocos.sprite.Sprite(logo, position=(w/2, h-75), scale=0.3),
              z=2)
    director.run(scene)
