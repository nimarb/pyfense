import pyglet
from pyglet.window import key

import cocos
from cocos.director import director
from cocos.actions import *
from cocos.scene import Scene
from cocos.menu import *
from cocos.layer import *
from cocos.text import *

from pyfense_game import *

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
        
        items.append( ImageMenuItem('assets/lvl1.png', 
                                    lambda: self.on_start(1)) )        
        items.append( MenuItem('Back', self.on_quit) )
        
        width, height = director.get_window_size()
        self.create_menu( items )
        
    def on_start( self, lvl ):
        director.push( PyFenseGame( lvl ), duration = 1 )
        
    def on_quit( self ):
        self.parent.switch_to( 0 )
        

class OptionsMenu( Menu ):
    
    def __init__( self ):
        
        super( OptionsMenu, self ).__init__('PyFense')

        self.font_title['font_size'] = 72
        
        self.menu_anchor_x = CENTER
        self.menu_anchor_y = CENTER
        
        items = []
        
        items.append( ToggleMenuItem( 'Show FPS' , self.on_show_fps,
                     director.show_FPS) )
        items.append( MenuItem( 'Back' , self.on_quit) )
        
        self.create_menu( items )
         
    def on_show_fps( self, value ):
        director.show_FPS = value
    
    def on_quit( self ):
        self.parent.switch_to( 0 )
        

class ScoresLayer( ColorLayer ):
        
    is_event_handler = True
    
    def __init__( self ):
        
        w, h = director.get_window_size()
        super( ScoresLayer, self ).__init__( 0,0,0,1, width = w, height = h-86 )
        
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
        
        if self.table:
            self.remove_old()

        self.table=[]
        name = Label('Hier könnte Ihr Name stehen!',
        font_name = 'Arial',
        font_size = 20,
        anchor_x = 'left',
        anchor_y = 'top')
        
        self.table.append( (name) )
        self.process_table()
        
    def remove_old( self ):
        for item in self.table:
            name = item
            self.remove( name )
        self.table = None
        
    def process_table( self ):
        
        w, h = director.get_window_size()
        for idx, item in enumerate( self.table ):
            name = item
            name.position = ( 48, 100 )
            
            self.add( name, z = 2 )
        
        
    def on_key_press( self, k, m ):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            self.parent.switch_to( 0 )
            return True

    def on_mouse_release( self, x, y, b, m ):
        self.parent.switch_to( 0 )
        return True
    
    
class AboutLayer( ColorLayer ):
    
    FONT_SIZE = 30
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

        text = Label('PyFense ist geil und wir lieben Nippel!',
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
    



# settings (later to be read from cfg file)
# some values might/will change during the course of the game
# for those values, only starting values are being defined here
settings = {
	"window": {
		"width": 1024,
		"height": 768,
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
