"""
Mainfile, draws Menu including Level Select, Highscore, Options and About page.
Reads settings from /data/settings.txt. Level Select starts game with
selected level from pyfense_game.
"""

import pyglet
from pyglet.window import key
from pyglet import font

import cocos
import cocos.menu
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ColorLayer, MultiplexLayer
from cocos.text import Label

import os  # for loading custom image
import sys

from pyfense import pyfense_modmenu
from pyfense import pyfense_game
from pyfense import pyfense_mapBuilder
from pyfense import pyfense_highscore
from pyfense import pyfense_resources

font.add_directory(os.path.join(
                os.path.dirname(
                os.path.abspath(__file__)), 'data/Orbitron'))
_font_ = 'Orbitron Light'


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__('')
        self.font_title['font_name'] = _font_
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = _font_
        self.font_item['font_size'] = 35

        self.font_item_selected['font_name'] = _font_
        self.font_item_selected['font_size'] = 41

        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER
        items = []
        items.append(cocos.menu.MenuItem('Start Game', self.on_level_select))
        items.append(cocos.menu.MenuItem('Scores', self.on_scores))
        items.append(cocos.menu.MenuItem('Settings', self.on_settings))
        items.append(cocos.menu.MenuItem('Help', self.on_help))
        items.append(cocos.menu.MenuItem('About', self.on_about))
        items.append(cocos.menu.MenuItem('Exit', self.on_quit))
        self.create_menu(items)
        self.schedule(self._scaleLogo)

    def on_level_select(self):
        w, h = director.get_window_size()
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(1)

    def on_settings(self):
        w, h = director.get_window_size()
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(2)

    def on_scores(self):
        w, h = director.get_window_size()
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(3)

    def on_help(self):
        w, h = director.get_window_size()
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(4)

    def on_about(self):
        w, h = director.get_window_size()
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        logo.scale = 0.25
        logo.position = (w/2+20, h-90)
        self.parent.switch_to(5)

    def on_quit(self):
        pyglet.app.exit()

    def _scaleLogo(self, dt):
        logo = cocos.sprite.Sprite(pyfense_resources.logo)
        w, h = director.get_window_size()
        if self.parent.enabled_layer == 0:
            logo.position = (w / 2 + 20, h - 175)
            logo.scale = 0.5


class LevelSelectMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__(' ')
        self.font_title['font_name'] = _font_
        self.font_title['font_size'] = 72
        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER
        items = []
        image_lvl1 = pyfense_resources.background["lvl1"]
        lvl1 = pyfense_modmenu.ImageMenuItem(image_lvl1,
                                             lambda: self.on_start(1))
        Back = cocos.menu.MenuItem('Back', self.on_quit)
        Back.y -= 30

        image_lvl2 = pyfense_resources.background["lvl2"]
        lvl2 = pyfense_modmenu.ImageMenuItem(image_lvl2,
                                             lambda: self.on_start(2))
        mapBuilderActivated = "nobuilder"
        try:
            mapBuilderActivated = sys.argv[1]
        except:
            mapBuilderActivated = "nobuilder"

        if(mapBuilderActivated == "builder"):
            MapBuilder = cocos.menuMenuItem('MapBuilder', self.on_mapBuilder)
            MapBuilder.y -= 20

        if(
            os.path.isfile(os.path.join(
                os.path.dirname(
                os.path.abspath(__file__)), "assets/lvlcustom.png"))):
                    customImage = pyfense_resources.lvlcustom
                    lvl1.scale = 0.18
                    lvl1.y = 30
                    items.append(lvl1)
                    lvl2.scale = 0.18
                    lvl2.y -= 150
                    items.append(lvl2)
                    customItem = (
                        pyfense_modmenu.ImageMenuItem(
                            customImage, lambda: self.on_start("custom")))
                    customItem.scale = 0.22
                    customItem.y -= 300
                    items.append(customItem)
                    if(mapBuilderActivated == "builder"):
                        MapBuilder.y -= 340
                        Back.y -= 20
                    Back.y -= 320
                # custom map has to be position correctly in Menu
        else:
            lvl1.scale = 0.28
            lvl1.y = 0
            items.append(lvl1)
            lvl2.scale = 0.28
            lvl2.y -= 300
            items.append(lvl2)
            if(mapBuilderActivated == "builder"):
                MapBuilder.y -= 320
                Back.y -= 20
            Back.y -= 300
        if(mapBuilderActivated == "builder"):
            items.append(MapBuilder)

        items.append(Back)
        width, height = director.get_window_size()
        self.create_menu(items)

    def on_start(self, lvl):
        """
        Starts the game with the selected level "lvl"
        """
        self.parent.switch_to(3)
        director.push(pyfense_game.PyFenseGame(lvl))

    def on_mapBuilder(self):
        """
        Starts the Mapbuilder
        """
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
            self._remove_old()
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
        self._process_table()

    def _remove_old(self):
        for item in self.table:
            pos, name, wave = item
            self.remove(pos)
            self.remove(name)
            self.remove(wave)
        self.table = None

    def _process_table(self):
        w, h = director.get_window_size()
        for i, item in enumerate(self.table):
            pos, name, wave = item
            pos_y = h - 200 - (self.fontsize + 15) * i
            pos.position = (w/2 - 330., pos_y)
            name.position = (w/2 - 300., pos_y)
            wave.position = (w/2 + 350., pos_y)
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


class OptionsMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__(' ')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER
        items = []
        items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.on_show_fps,
                     pyfense_resources.settings["general"]["showFps"]))
        items.append(cocos.menu.ToggleMenuItem('Fullscreen: ',
                                               self.on_fullscreen, False))
        items.append(cocos.menu.ToggleMenuItem('Vsync: ', self.on_vsync,
                     pyfense_resources.settings["window"]["vsync"]))
        items.append(cocos.menu.ToggleMenuItem('Sounds: ', self.on_sounds,
                     pyfense_resources.settings["general"]["sounds"]))
        items.append(cocos.menu.MenuItem('Back', self.on_quit))
        self.create_menu(items)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_fullscreen(self, value):
        director.window.set_fullscreen(value)

    def on_vsync(self, value):
        director.window.set_vsync(value)

    def on_sounds(self, value):
        pyfense_resources.sounds = not pyfense_resources.sounds
        if(pyfense_resources.music_player.playing):
            pyfense_resources.music_player.pause()
        else:
            pyfense_resources.music_player.play()

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
        text = Label('Press Q to quit the running level or Esc to enter the ' +
                     'Pause Menu',
                     font_name=_font_,
                     font_size=20,
                     anchor_x='center',
                     anchor_y='center')
        text.element.width = w * 0.3
        text.element.multiline = True
        text.element.wrap_lines = True
        text.position = w/2., h/2. + 300
        self.add(text)

        # tower information
        self.damage_pic = pyfense_resources.picto_damage
        self.rate_pic = pyfense_resources.picto_rate
        pic_width = pyfense_resources.tower[1][1]["image"].width
        self.menuMin_x = (w/2. - pic_width * (4 / 3) - 55)
        self.menuMin_y = 550
        towername_font = {
            'bold': True,
            'anchor_x': "right",
            'anchor_y': 'center',
            'font_size': 18,
            'color': (193, 249, 255, 255)
        }
        caption_font = {
            'bold': True,
            'anchor_x': "left",
            'anchor_y': 'center',
            'font_size': 15,
            }

        label1 = cocos.text.Label("Rapidfire Tower", **towername_font)
        label2 = cocos.text.Label("Range Tower", **towername_font)
        label3 = cocos.text.Label("Plasma Tower", **towername_font)
        price_label = cocos.text.Label("$  Price",
                                       color=(255, 0, 0, 255), **caption_font)
        dam_pic = cocos.sprite.Sprite(self.damage_pic)
        dam_label = cocos.text.Label("Damage per second",
                                     color=(255, 70, 0, 255), **caption_font)
        rate_pic = cocos.sprite.Sprite(self.rate_pic)
        rate_label = cocos.text.Label("Firerate",
                                      color=(0, 124, 244, 255), **caption_font)

        label1.position = (self.menuMin_x - 80, self.menuMin_y)
        label2.position = (self.menuMin_x - 80, self.menuMin_y -
                           pic_width - 15)
        label3.position = (self.menuMin_x - 80, self.menuMin_y -
                           2 * (pic_width + 15))
        price_label.position = (self.menuMin_x - 60,
                                self.menuMin_y - (3 * (pic_width + 15)))
        dam_pic.position = (self.menuMin_x + 73,
                            self.menuMin_y - (3 * (pic_width + 15)))
        dam_label.position = (self.menuMin_x + 105,
                              self.menuMin_y - (3 * (pic_width + 15)))
        rate_pic.position = (self.menuMin_x + 380,
                             self.menuMin_y - (3 * (pic_width + 15)))
        rate_label.position = (self.menuMin_x + 412,
                               self.menuMin_y - (3 * (pic_width + 15)))

        self.add(label1)
        self.add(label2)
        self.add(label3)
        self.add(price_label)
        self.add(dam_pic)
        self.add(dam_label)
        self.add(rate_pic)
        self.add(rate_label)
        for l in range(1, 4):  # loop over upgrade levels
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
                'font_size': 15,
                'color': (255, 70, 0, 255)
                }
            label4 = cocos.text.Label(" ", **text_font)
            label5 = cocos.text.Label(" ", **text_font)
            label6 = cocos.text.Label(" ", **text_font)
            self.towerDamageTexts = [label4, label5, label6]

            text_font['color'] = (0, 124, 244, 255)
            label7 = cocos.text.Label(" ", **text_font)
            label8 = cocos.text.Label(" ", **text_font)
            label9 = cocos.text.Label(" ", **text_font)
            self.towerFirerateTexts = [label7, label8, label9]

            text_font['color'] = (255, 0, 0, 255)
            label10 = cocos.text.Label(" ", **text_font)
            label11 = cocos.text.Label(" ", **text_font)
            label12 = cocos.text.Label(" ", **text_font)
            self.towerCostTexts = [label10, label11, label12]

            for picture in range(0, len(self.towerThumbnails)):
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100),
                    -picture * (self.towerThumbnails[picture].width + 15)+
                    self.menuMin_y)

                self.towerDamagePic.append(
                    cocos.sprite.Sprite(self.damage_pic))
                self.towerDamagePic[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y)

                self.towerDamageTexts[picture].element.text = (
                    str(pyfense_resources.tower[picture][l]["damage"] *
                        pyfense_resources.tower[picture][l]["firerate"] / 1.))
                self.towerDamageTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 35,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y)

                self.towerFireratePic.append(
                    cocos.sprite.Sprite(self.rate_pic))
                self.towerFireratePic[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y - 25)

                self.towerFirerateTexts[picture].element.text = (
                    str(pyfense_resources.tower[picture][l]["firerate"]))
                self.towerFirerateTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 35,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y - 25)

                self.towerCostTexts[picture].element.text = (
                    '$ ' + str(pyfense_resources.tower[picture][l]["cost"]))
                self.towerCostTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y + 25)

                self.add(self.towerThumbnails[picture])
                self.add(self.towerDamageTexts[picture])
                self.add(self.towerFirerateTexts[picture])
                self.add(self.towerDamagePic[picture])
                self.add(self.towerFireratePic[picture])
                self.add(self.towerCostTexts[picture])

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

def main():
# if __name__ == '__main__':
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

    # Music - moved to resources
    # 1st Try - doesnt play anything
    # scene.load_music("assets/music.wav")
    # scene.play_music()

    # 2nd Try - static noise louder than music
    # music = pyglet.resource.media("assets/music.wav", streaming = True)
    # music.play()

    # 3rd Try - music stops after ca. 1 min (even when piece was longer)
    # and doesnt repeat as it should
#    music_player = pyglet.media.Player()
#    music = pyglet.resource.media("assets/music.wav", streaming = False)
#    music_player.queue(music)
#    music_player.eos_action = music_player.EOS_LOOP

    logo = cocos.sprite.Sprite(pyfense_resources.logo)
    scene.add(logo, z=2)
    director.run(scene)

# if __name__ == '__main__':
#     main()
