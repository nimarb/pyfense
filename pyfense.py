"""
Mainfile, draws Menu including Level Select, Highscore, Options and About page.
Reads settings from /data/settings.txt #TODO, About from /data/about.txt #TODO
and gets Highscore data from pyfense_highscore. Level Select starts game with
selected level from pyfense_game.
"""

import pyglet
from pyglet.window import key
from pyglet import font

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


font.add_directory('data/Orbitron')
_font_ = 'Orbitron Light'


class MainMenu(Menu):
    def __init__(self):
        super().__init__('')
        self.font_title['font_name'] = _font_
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
        self.schedule(self.scaleLogo)

    def on_level_select(self):
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(1)

    def on_settings(self):
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(2)

    def on_scores(self):
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(3)

    def on_help(self):
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(4)

    def on_about(self):
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(5)

    def on_quit(self):
        pyglet.app.exit()

    def scaleLogo(self, dt):
        if self.parent.enabled_layer == 0:
            logo.position = (w / 2 + 20, h - 175)
            logo.scale = 0.5


class LevelSelectMenu(Menu):
    def __init__(self):
        super().__init__(' ')
        self.font_title['font_name'] = _font_
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
        Back.y -= 30
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
        self.parent.switch_to(3)
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

        self.table = None

    def on_enter(self):
        super().on_enter()
        score = pyfense_highscore.get_score()
        if self.table:
            self.remove_old()
        self.table = []

        self.font_top = {}
        self.font_top['font_size'] = self.fontsize
        self.font_top['bold'] = True
        self.font_top['font_name'] = _font_

        self.font_label = {}
        self.font_label['font_size'] = self.fontsize
        self.font_label['bold'] = False
        self.font_label['font_name'] = _font_

        Head_Pos = Label('',
                         anchor_x='right',
                         anchor_y='top',
                         **self.font_top)
        Head_Name = Label('Name',
                          anchor_x='left',
                          anchor_y='top',
                          **self.font_top)
        Head_Wave = Label('Wave',
                          anchor_x='right',
                          anchor_y='top',
                          **self.font_top)
        self.table.append((Head_Pos, Head_Name, Head_Wave))
        self.table.append((Label(''), Label(''), Label('')))

        for i, entry in enumerate(score):
            pos = Label('%i.    ' % (i+1),
                        anchor_x='right',
                        anchor_y='top',
                        **self.font_label)
            try:
                name = Label(entry[1].strip(),
                             anchor_x='left',
                             anchor_y='top',
                             **self.font_label)
            except IndexError:
                print("highscore file broken")
                name = Label("Error",
                             anchor_x='left',
                             anchor_y='top',
                             **self.font_label)
            wave = Label(entry[0],
                         anchor_x='right',
                         anchor_y='top',
                         **self.font_label)
            self.table.append((pos, name, wave))
        self.process_table()

    def remove_old(self):
        for item in self.table:
            pos, name, wave = item
            self.remove(pos)
            self.remove(name)
            self.remove(wave)
        self.table = None

    def process_table(self):
        w, h = director.get_window_size()
        for i, item in enumerate(self.table):
            pos, name, wave = item
            pos_y = h - 200 - (self.fontsize + 15) * i
            pos.position = (w/2 - 400., pos_y)
            name.position = (w/2 - 380., pos_y)
            wave.position = (w/2 + 130., pos_y)
            self.add(pos, z=2)
            self.add(name, z=2)
            self.add(wave, z=2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


class OptionsMenu(Menu):
    def __init__(self):
        super().__init__(' ')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        items = []
        items.append(ToggleMenuItem('Show FPS: ', self.on_show_fps,
                     pyfense_resources.settings["general"]["showFps"]))
        items.append(ToggleMenuItem('Fullscreen: ', self.on_fullscreen,
                     False))
        items.append(ToggleMenuItem('Vsync: ', self.on_vsync,
                     pyfense_resources.settings["window"]["vsync"]))
        items.append(ToggleMenuItem('Sounds: ', self.on_sounds,
                     pyfense_resources.settings["general"]["sounds"]))
        items.append(MenuItem('Back', self.on_quit))
        self.create_menu(items)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_fullscreen(self, value):
        director.window.set_fullscreen(value)

    def on_vsync(self, value):
        director.window.set_vsync(value)

    def on_sounds(self, value):
        pyfense_resources.sounds = not pyfense_resources.sounds

    def on_quit(self):
        self.parent.switch_to(0)


class HelpLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h-86)

    def on_enter(self):
        super().on_enter()
        w, h = director.get_window_size()
        text = Label('Press Q to quit the running level',
                     font_name=_font_,
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

    def on_enter(self):
        super().on_enter()
        w, h = director.get_window_size()

        text = Label('PyFense ist geil und wir lieben Nippel! Und Matthias ' +
                     'ist der Mitarbeiter des monats wenn die testklassen' +
                     ' laufen :D',  # LOL
                     font_name=_font_,
                     font_size=20,
                     anchor_x='center',
                     anchor_y='center')
        text.element.width = w * 0.3
        text.element.multiline = True
        text.element.wrap_lines = True
        text.position = w/2., h/2.
        self.add(text)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True

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

    logo = cocos.sprite.Sprite(pyfense_resources.logo)
    scene.add(logo, z=2)
    director.run(scene)
