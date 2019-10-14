#from distutils.core import setup
from setuptools import setup
from pathlib import Path
from os import path

this_dir = Path(__file__).resolve().parent
with open(this_dir / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'PyFense',
    version = '0.9.5',
    license = 'GPLv3',
    packages = ['pyfense'],
    package_data = {
        'pyfense': [
            'assets/*.*',
            'data/*.*']
    },

    install_requires = ['pyglet>=1.3.0', 'cocos2d>=0.6.5', 'numpy>=1.9.2'],

    maintainer = 'nimar b',
    maintainer_email = 'l.nimar.b@gmail.com',
    url = "https://github.com/nimarb/pyfense",

    description = 'PyFense is a tower defense game built using Python 3, \
        the cocos2d and pyglet frameworks. If you want to contribute in any way (art, code, balancing, bug reporting) \
        you can do so here: https://github.com/nimarb/pyfense/ . Thank you!',

    entry_points = {
        'console_scripts': ['pyfense = pyfense.pyfense:main']
    },
    keywords = "pyfense tower defense td game",
    classifiers = [
        'Programming Language :: Python',
        'Topic :: Games/Entertainment'],

    long_description = long_description,
    long_description_content_type='text/markdown'
)
