"""
Manages highscore
"""
import pyglet
from pyglet.window import key

import cocos
from cocos.layer import Layer
from cocos.director import director
from cocos.text import *
from cocos.scene import Scene
from cocos.menu import *

import pyfense


def new_score(name, score, level):
    highscore = readFile("data/highscore.txt")
    for i, entry in enumerate(highscore):
        if entry[0][0] == "#":
            continue
        else:
            if entry[1] <= score:
                continue
            else:
                #TODO write file to be implemented
                return True
    return False


def get_score():

    highscore = readFile("data/highscore.txt")
    return highscore


def readFile(fileName):

    with open(fileName, "r") as openedFile:
        openedFile.readline()
        fileData = openedFile.readlines()
        splittedData = [row.split(", ") for row in fileData]
    return splittedData


class PyFenseLost(Scene):

    def __init__(self, reachedWave):
        super().__init__()
        self.wave = reachedWave
        self.add(LostLayer(self.wave), z=1)


class LostLayer(Layer):

    is_event_handler = True

    def __init__(self, wave):
        super().__init__()
        self.wave = wave

        w, h = director.get_window_size()
        text1 = Label('+++ You Lost! +++',
                      font_name='Arial',
                      font_size=20,
                      anchor_x='center',
                      anchor_y='center')
        text1.position = w/2., h/2. + 25
        text2 = Label('You reached wave %d' % wave,
                      font_name='Arial',
                      font_size=20,
                      anchor_x='center',
                      anchor_y='center')
        text2.position = w/2., h/2.
        self.add(text1)
        self.add(text2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            director.replace(Scene(SubmitScore(self.wave)))
            return True

    def on_mouse_release(self, x, y, b, m):
        director.replace(Scene(SubmitScore(self.wave)))
        return True


class SubmitScore(Menu):

    def __init__(self, wave):
        super().__init__('PyFense')
        self.font_title['font_size'] = 72
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        items = []
        name = ""
        items.append(EntryMenuItem('Name', self.on_submit,
                                   name, max_length=15))
        self.create_menu(items)

    def on_submit(self, name):
        director.push(Scene(pyfense.ScoresLayer()))
