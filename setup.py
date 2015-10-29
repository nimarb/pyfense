#from distutils.core import setup
from setuptools import setup

setup(
    name = 'PyFense',
    version = '0.9.4',
    license = 'GPLv3',
    packages = ['pyfense'],
    package_data = {
        'pyfense': [
            'assets/*.*',
            'data/*.*']
    },

    install_requires = ['pyglet>=1.2.3', 'cocos2d>=0.6.0', 'numpy>=1.9.2'],

    maintainer = 'nimar b',
    maintainer_email = 'l.nimar.b@gmail.com',

    description = 'PyFense is a tower defense game built in using Python 3, \
        the cocos2d and pyglet frameworks. If you want to contribute in any way (art, code, balancing, bug reporting) \
        you can do so here: https://github.com/likyng/pyfense/ . Thank you!',

    entry_points = {
        'console_scripts': ['pyfense = pyfense.pyfense:main']
    },
    keywords = "pyfense tower defense td game",
    classifiers = [
        'Programming Language :: Python',
        'Topic :: Games/Entertainment']
)
