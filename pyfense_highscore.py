"""
Manages highscore
"""
import pyglet

import cocos
from cocos.layer import Layer
from cocos.director import director
from cocos.text import *


def new_score( name, score, level ):
    highscore = readFile( "data/highscore.txt" )
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

    highscore = readFile( "data/highscore.txt" )
    return highscore


def readFile( fileName ):

    with open( fileName, "r" ) as openedFile:
        openedFile.readline()
        fileData = openedFile.readlines()
        splittedData = [row.split( ", " ) for row in fileData]
    return splittedData


class GameLostLayer( Layer, pyglet.event.EventDispatcher ):
    
        is_event_handler = True
        
        def __init__( self ):
            super().__init__()
            w, h = director.get_window_size()
            text = Label('Game Over',
                         font_name = 'Arial',
                         font_size = 20,
                         anchor_x = 'center',
                         anchor_y = 'center')

            text.position = w/2. , h/2.
            self.add(text)