import pyglet
from pyglet.window import key

import cocos
from cocos.director import director
from cocos.actions import *
from cocos.scene import Scene
from cocos.menu import *
from cocos.layer import *
from cocos.text import *
from cocos.menu import BaseMenuItem
from six import string_types

import pyfense_game
import pyfense_highscore
from pyfense_resources import *

"""
Mainfile, draws Menu including Level Select, Highscore, Options and About page.
Reads settings from /data/settings.txt #TODO, About from /data/about.txt #TODO 
and gets Highscore data from pyfense_highscore. Level Select starts game with
selected level from pyfense_game.
"""

class MainMenu( Menu ):
    
    def __init__( self ):
        
        super( MainMenu, self ).__init__('PyFense')
        
        self.font_title['font_size'] = 72        
        
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        
        items = []
        
        items.append( MenuItem('Start Game', self.on_level_select) )
        items.append( MenuItem('Scores', self.on_scores) )
        items.append( MenuItem('Settings', self.on_settings) )
        items.append( MenuItem('About', self.on_about) )
        items.append( MenuItem('Exit', self.on_quit) )
        
        self.create_menu( items )
        
    def on_level_select( self ):
        self.parent.switch_to(1)
        
        
    def on_settings( self ):
        self.parent.switch_to(2)

        
    def on_scores( self ):
        self.parent.switch_to(3)        

        
    def on_about( self ):
        self.parent.switch_to(4)
        
        
    def on_quit( self ):
        pyglet.app.exit()
        
        
class LevelSelectMenu( Menu ):
    
    def __init__(self):
        
        super( LevelSelectMenu, self ).__init__('PyFense')
        
        self.font_title['font_size'] = 72        
        
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        
        items = []
        
        items.append( LevelMenuItem('assets/lvl1.png', 
                                    lambda: self.on_start(1)) )        
        items.append( MenuItem('Back', self.on_quit) )
        
#        for entry in items:
#                entry.scale = 5
        
        width, height = director.get_window_size()
        self.create_menu( items )
        
    def on_start( self, lvl ):
        director.push( pyfense_game.PyFenseGame( lvl ) )
        
    def on_quit( self ):
        self.parent.switch_to( 0 )
        

class ScoresLayer( ColorLayer ):
        
    is_event_handler = True
    fontsize = 40
    
    def __init__( self ):
        
        w, h = director.get_window_size()
        super( ScoresLayer, self ).__init__( 0,0,0,1, 
                                            width = w, height = h-86 )
        
        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] ='top'
        self.font_title['anchor_x'] ='center'
        title = Label( 'PyFense', **self.font_title )
        title.position = ( w/2. , h )
        self.add( title, z=1 )
        self.table = None
        
    def on_enter ( self ):
        
        super( ScoresLayer, self ).on_enter()
        score = pyfense_highscore.get_score()
        
        if self.table:
            self.remove_old()

        self.table=[]
       
        Head_Pos = Label( '',
                         bold = True,
                         font_name = 'Arial',
                         font_size = self.fontsize,
                         anchor_x = 'right',
                         anchor_y = 'top')
        Head_Name = Label('Name',
                          bold = True,
                         font_name = 'Arial',
                         font_size = self.fontsize,
                         anchor_x = 'left',
                         anchor_y = 'top')
        Head_Score = Label('Score',
                           bold = True,
                           font_name = 'Arial',
                           font_size = self.fontsize,
                           anchor_x = 'right',
                           anchor_y = 'top')
        Head_Level = Label('Reached Level',
                         bold = True,
                         font_name = 'Arial',
                         font_size = self.fontsize,
                         anchor_x = 'center',
                         anchor_y = 'top')
        self.table.append( ( Head_Pos, Head_Name, Head_Score, Head_Level ) )
        self.table.append( ( Label(''), Label(''), Label(''), Label('') ) )
      
        for i, entry in enumerate(score):
            
            pos = Label( '%i.    ' %(i+1),
                     font_name = 'Arial',
                     font_size = self.fontsize,
                     anchor_x = 'right',
                     anchor_y = 'top')
            name = Label(entry[0],
                     font_name = 'Arial',
                     font_size = self.fontsize,
                     anchor_x = 'left',
                     anchor_y = 'top')
            score = Label(entry[1],
                     font_name = 'Arial',
                     font_size = self.fontsize,
                     anchor_x = 'right',
                     anchor_y = 'top')
            level = Label(entry[2].strip(),
                     font_name = 'Arial',
                     font_size = self.fontsize,
                     anchor_x = 'right',
                     anchor_y = 'top')
            self.table.append( (pos, name, score, level) )
            
        self.process_table()
        
    def remove_old( self ):
        for item in self.table:
            pos, name, score, level = item
            self.remove( pos )
            self.remove( name )
            self.remove( score )
            self.remove( level )
        self.table = None
        
    def process_table( self ):
        
        w, h = director.get_window_size()
        
        for i, item in enumerate( self.table ):
            
            pos, name, score, level = item
            pos_y = h-200 - ( self.fontsize + 15 ) * i
            
            pos.position = ( w/2 - 400. , pos_y )
            name.position = ( w/2 - 380. , pos_y )
            score.position = ( w/2 + 130. , pos_y )
            level.position = ( w/2 + 430 , pos_y )
            
            self.add( pos, z = 2 )
            self.add( name, z = 2 )
            self.add( score, z = 2 )
            self.add( level, z = 2 )
        
        
    def on_key_press( self, k, m ):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            self.parent.switch_to( 0 )
            return True

    def on_mouse_release( self, x, y, b, m ):
        self.parent.switch_to( 0 )
        return True
        

class OptionsMenu( Menu ):
    
    def __init__( self ):
        
        super( OptionsMenu, self ).__init__('PyFense')

        self.font_title['font_size'] = 72
        
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        
        items = []
        
        items.append( ToggleMenuItem( 'Show FPS: ' , self.on_show_fps,
                     director.show_FPS) )
        items.append( MenuItem( 'Back' , self.on_quit) )
        
        self.create_menu( items )
         
    def on_show_fps( self, value ):
        director.show_FPS = value
    
    def on_quit( self ):
        self.parent.switch_to( 0 )
        

class AboutLayer( ColorLayer ):
    
    is_event_handler = True
    
    def __init__( self ):
        
        w, h = director.get_window_size()
        super( AboutLayer, self ).__init__( 0,0,0,1, width = w, height = h-86 )
        
        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] ='top'
        self.font_title['anchor_x'] ='center'
        title = Label( 'PyFense', **self.font_title )
        title.position = ( w/2. , h )
        self.add( title, z=1 )
        self.table = None
        
    def on_enter ( self ):
        
        super( AboutLayer, self ).on_enter()
        w, h = director.get_window_size()

        text = Label('PyFense ist geil und wir lieben Nippel!', #LOL
        font_name = 'Arial',
        font_size = 20,
        anchor_x = 'center',
        anchor_y = 'center')
        
        text.position = w/2. , h/2.
        self.add(text)        
        
    def on_key_press( self, k, m ):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            self.parent.switch_to( 0 )
            return True

    def on_mouse_release( self, x, y, b, m ):
        self.parent.switch_to( 0 )
        return True    
        
        
class LevelMenuItem (BaseMenuItem):
    def __init__(self, image, callback_func, *args, **kwargs):
        if isinstance(image, string_types):
            image = loadImage(image)
        self.image = image
        Menu(ImageMenuItem, self).__init__(callback_func, *args, **kwargs)
    def generateWidgets(self, pos_x, pos_y, font_item, font_item_selected):
        anchors = {'left': 0, 'center': 0.5, 'right': 1, 'top': 1, 'bottom': 0}
        anchor = (anchors[font_item['anchor_x']] * self.image.width,
                  anchors[font_item['anchor_y']] * self.image.height)
        self.item = Sprite(self.image, anchor=anchor, opacity=255,
                           color=font_item['color'][:3])
        self.item.scale = font_item['font_size'] / float(self.item.height)
        self.item.position = int(pos_x), int(pos_y)
        self.selected_item = Sprite(self.image, anchor=anchor,
                                    color=font_item_selected['color'][:3])
        self.selected_item.scale = (font_item_selected['font_size'] /
                                    float(self.selected_item.height))
        self.selected_item.position = int(pos_x), int(pos_y)

    def draw(self):
        glPushMatrix()
        self.transform()
        if self.is_selected:
            self.selected_item.draw()
        else:
            self.item.draw()
        glPopMatrix()


# settings (later to be read from cfg file)
# some values might/will change during the course of the game
# for those values, only starting values are being defined here
settings = {
	"window": {
		"width": 1920,
		"height": 1080,
		"caption": "PyFense",
		"vsync": True,
		"fullscreen": False,
		#ATTENTION: misspelling intentional, pyglet fcked up
		"resizable": True
	}, 
	"world": {
		"gameSpeed": 1.0
	},
	"player": {
		"currency": 200	
	},
	"general": {
		"showFps" : True
	}
}

if __name__ == '__main__':
    director.init(**settings['window'])
    scene = Scene()
    scene.add( MultiplexLayer(
        MainMenu(),
        LevelSelectMenu(),
        OptionsMenu(),
        ScoresLayer(),
        AboutLayer()
        ),
        z = 1 )
    director.set_show_FPS(settings["general"]["showFps"])
        
    director.run( scene )
