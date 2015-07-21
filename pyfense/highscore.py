"""
Manages highscore
"""
import os

from pyglet.window import key
from pyglet import font

from cocos.layer import Layer
from cocos.director import director
from cocos.text import Label
from cocos.scene import Scene

# name and path of the highscore file
HS_FILENAME = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), "data") + "/highscore.data"
font.add_directory(os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'assets/'))
_font_ = 'Orbitron Light'

currentWave = 0


def new_score(name, wave):
    """
    New score with name "name" and reached wave "wave" will be written to
    HS_FILENAME, if the score is high enough and True or False will be
    returned
    """
    try:
        highscore = _readFile(HS_FILENAME)
    except IOError:
        print("new " + HS_FILENAME + " will be created")
        for l in name:
            if not l.isalnum():
                name = name.replace(l, '_')
        highscore = [[wave, name]]
        _writeFile(HS_FILENAME, highscore)
        return True
    for i, entry in enumerate(highscore):
        if i == 10:
            return False
        else:
            if int(entry[0]) >= wave:
                continue
            else:
                for l in name:
                    if not l.isalnum():
                        name = name.replace(l, '_')
                new_entry = [wave, name]
                highscore.append(new_entry)
                new_highscore = sorted(highscore, key=lambda s: int(s[0]))
                new_highscore.reverse()
                new_highscore = new_highscore[0:10]
                _writeFile(HS_FILENAME, new_highscore)
                return True
    if i < 9:
        for l in name:
            if not l.isalnum():
                name = name.replace(l, '_')
        new_entry = [wave, name]
        highscore.append(new_entry)
        new_highscore = sorted(highscore, key=lambda s: int(s[0]))
        new_highscore.reverse()
        new_highscore = new_highscore[0:10]
        _writeFile(HS_FILENAME, new_highscore)
        return True
    else:
        return False  # if no lower score is found


def check_score(wave):
    """
    It is checked, if the reached wave "wave" is high enogh to make a new score
    and the place or False will be returned
    """
    try:
        highscore = _readFile(HS_FILENAME)
    except IOError:
        # file not found, new highscore will be created
        return 1
    for i, entry in enumerate(highscore):
        if i == 10:
            return False
        else:
            if int(entry[0]) >= wave:
                continue
            else:
                return (i + 1)
    if i < 9:
        return (i + 2)  # score will be appended
    else:
        return False  # no lower score found


def get_score():
    """
    returns HS_FILENAME or if not present an empty score
    """
    try:
        highscore = _readFile(HS_FILENAME)
        return highscore
    except IOError:
        return [['0', 'no highscore']]


def _readFile(fileName):
    with open(fileName, "r") as openedFile:
        fileData = []
        for line in openedFile:
            if line.startswith('#'):
                continue
            else:
                fileData.append(line)
        splittedData = [row.split(", ") for row in fileData]
    return splittedData


def _writeFile(fileName, writeFile):
    try:
        with open(fileName, "w") as openedFile:
            openedFile.write('#wave, user\n')
            for entry in writeFile:
                openedFile.write('%d, %s\n'
                                 % (int(entry[0]), entry[1].strip()))
    except Exception as e:
        print("An error while writing occured:")
        print(e)


class PyFenseLost(Scene):
    def __init__(self):
        super().__init__()
        self.wave = currentWave
        self.add(LostLayer(self.wave), z=1)


class LostLayer(Layer):
    is_event_handler = True

    def __init__(self, wave):
        super().__init__()
        self.wave = wave
        if check_score(wave) is False:
            self.in_highscore = False
        else:
            self.place = check_score(wave)
            self.in_highscore = True
        w, h = director.get_window_size()
        text1 = Label('+++ Game Over! +++',
                      font_name=_font_,
                      font_size=30,
                      anchor_x='center',
                      anchor_y='center')
        text1.position = w/2., h/2. + 65
        if self.in_highscore:
            text2 = Label(
                'You reached wave %d ' % wave +
                'and place %d of the highscore' % self.place,
                font_name=_font_,
                font_size=20,
                anchor_x='center',
                anchor_y='center')
        else:
            text2 = Label(
                'You reached wave %d' % wave,
                font_name=_font_,
                font_size=20,
                anchor_x='center',
                anchor_y='center')
        text2.position = w/2., h/2.
        self.add(text1)
        self.add(text2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            if self.in_highscore:
                director.replace(Scene(SubmitScore(self.wave)))
            else:
                director.pop()
            return True

    def on_mouse_release(self, x, y, b, m):
            if self.in_highscore:
                director.replace(Scene(SubmitScore(self.wave)))
            else:
                director.pop()
            return True


class SubmitScore(Layer):

    is_event_handler = True

    def __init__(self, wave):
        super().__init__()
        w, h = director.get_window_size()
        self.wave = wave
        self.font_title = {
            'font_name': _font_,
            'font_size': 72,
            'anchor_y': 'top',
            'anchor_x': 'center'
        }
        title = Label('GameOver', **self.font_title)
        title.position = (w/2., h)
        self.add(title, z=1)
        self.font_label = {
            'font_name': _font_,
            'font_size': 40,
            'anchor_y': 'top',
            'anchor_x': 'center'
        }
        label = Label('Enter your name:', **self.font_label)
        label.position = (w/2., 600.)
        self.add(label)
        self.name = Label('', color=(192, 192, 192, 255), **self.font_label)
        self.name.position = (w/2., 530.)
        self.add(self.name)

    def on_key_press(self, k, m):
        if k == key.BACKSPACE:
            self.name.element.text = self.name.element.text[0:-1]
            return True
        elif k == key.ENTER:
            if len(self.name.element.text) <= 2:
                w, h = director.get_window_size()
                label_s = Label(
                    'Name too short! Choose at least 3 characters',
                    font_name=_font_,
                    font_size=20,
                    anchor_y='top',
                    anchor_x='center')
                label_s.position = (w/2., 700.)
                self.add(label_s)
            elif len(self.name.element.text) >= 15:
                w, h = director.get_window_size()
                label_l = Label(
                    'Name too long! Not more than 15 characters allowed',
                    font_name=_font_,
                    font_size=20,
                    anchor_y='top',
                    anchor_x='center')
                label_l.position = (w/2., 750.)
                self.add(label_l)
            else:
                new_score(self.name.element.text, self.wave)
                director.pop()
            return True
        elif k == key.ESCAPE:
            director.pop()
            return True
        return False

    def on_text(self, t):
        if t == '\r':
            return True
        self.name.element.text += t
