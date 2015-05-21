## File Names

 - pyfense.py : contains main function
 - pyfense_menu.py : contains PyFenseMenu class (scene)
 - pyfense_settings.py : contains PyFenseSettings class (scene)
 - pyfsnse_about.py : contains PyFenseAbout class (scene)
 - pyfense_highscore.py : contains PyFenseHighscore (scene)
 - pyfense_level.py : contains PyFenseLevel class (level selector) (scene)
 - pyfense_game.py : contains actual gameplay class PyFenseGame (scene)
 - pyfense_tower.py : contains PyFenseTower class (Sprite?)
 - pyfense_projectile.py : SINNVOLL?
 - pyfense_enemy.py : contains PyFenseEnemy class (Sprite?)

### include structure

 - pyfense.py includes pyfense_menu
 - pyfense_menu includes all scenes except for PyFenseGame
 - pyfense_level includes PyFenseGame
 - pyfense_game includes PyFenseTower, PyFenseEnemy

### scene structure
 - shall new scenes replace old scene or push onto stack?
