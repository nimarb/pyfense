# pyfense_hud.py
# contains head up display, takes care of displaying lose/win
# current wave number and other information intented for the player

import cocos

class PyFenseHud(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.currentWave = 1
        self.displayWaveNumber()
        
    def displayWaveNumber(self):
        self.waveLabel = cocos.text.Label('Current Wave: ' + str(self.currentWave), 
                anchor_x='center', anchor_y='center')
        w, h = cocos.director.director.get_window_size()
        self.waveLabel.position = w / 2, h - 30
        self.add(self.waveLabel)
