"""
Manages highscore
"""
import cocos
from cocos import layer
from cocos import menu
from cocos.director import director


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
