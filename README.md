# pyFense
Tower Defense game written in Python 3 using cocos2d and pyglet.
For roadmap and further documentation/information on the project, check [documentation/roadmap.md]

## playing the game
If you just want to play and enjoy pyfense, you can simply install it from pypi here: https://pypi.python.org/pypi/PyFense
Alternatively you can clone this repo and run pyFense locally through virtualenv.

## about
pyFense was written by Daniel Lechner, Jakob Müller, Matthias Lutz, Nimar Blume and Robin Wachsmann as part of an university project at the Technical University of Munich.
The aim of the course was to get familiar with the Python programming language, git and distributed development.

## contributing
We welcome all contributions: code, ideas, sprites/art, balancing suggestions and other improvements. Please don't hesitate to ask, write an issue or send a pull request!
For code, please try to adhere to the PEP8 guideline to keep the code readable and uniform :).

## dependencies
python 3, pyglet>=1.2.3, cocos2d>=0.6.0, numpy>=1.9.2
earlier versions might work but were not tested against. pyglet 1.2.2 and earlier cause a segfault due to incorrect calling of gdk_pixbuf.

## how to setup the development environment
Steps to replicate the development environment:
1. clone this repo
2. initiate virtualenv in the project dir: virtualenv .
3. install pyfense in the virtualenv environment: ./bin/python setup.py develop
4. set execute permission for the executeable: chmod +x ./bin/pyfense
5. run pyfense: ./bin/pyfense
6. to modify pyfense edit the responding file in ./pyfense/
7. have fun :)

## unit tests
to be added later

## program structure
pyFense is written in an Object oriented structure.
What each file contains:
 - pyfense.py: entry point into the game, contains the game menus. for some menus a "modmenu" class is used, which is defined in
 - enemy.py: subclasses cocos2d sprite to create a class to represent a single enemy.
 - entities.py:
 - game.py:
 - highscore.py:
 - hud.py: provides the ingame HUD (announcements, tower build/upgrade menu, coursor selections etc)
 - map.py:
 - mapBuilder.py:
 - mapbuilderhud.py:
 - modmenu.py: subclasses cocos2d menuitem to display a non-scaled image as a menuitem.
 - particles.py:
 - pause.py: a cocos2d scene and layer to provide the ingame pause menu.
 - projectile.py: subclasses cocos2d sprite to create a class to represent a single projectile, fired by towers at enemies.
 - projectileParticle.py: subclasses the pyglet particle system to provide particles for projectiles.
 - resources.py: all assets used by pyFense are loaded into memory in resources.py.
 - tower.py: subclasses cocos2d sprite to create a class to represent a single tower.

## possible improvements
 - major balancing improvements
 - more exciting levels
 - online highscores
 - multiplayer (lan/internet) -> requires significant client/server rewrite