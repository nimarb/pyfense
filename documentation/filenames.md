## File Names

 - pyfense.py : contains main function
 - pyfense_menu.py : contains PyFenseMenu class (layer)
 - pyfense_settings.py : contains PyFenseSettings class (layer)
 - pyfsnse_about.py : contains PyFenseAbout class (layer)
 - pyfense_highscore.py : contains PyFenseHighscore (layer)
 - pyfense_level.py : contains PyFenseLevel class (level selector) (layer)
 - pyfense_game.py : contains actual gameplay class PyFenseGame (layer)
 - pyfense_tower.py : contains PyFenseTower class (Sprite)
 - pyfense_projectile.py : contains PyFenseProjectile class (Sprite)
 - pyfense_enemy.py : contains PyFenseEnemy class (Sprite)
 - pyfense_entities.py : contains on screen Entities (Enemies, Towers, Projectiles) (layer)
 - pyfense_map.py : contains PyFenseMap class, draws the background image (map) (layer)
 - pyfene_hud.py : contains PyFenseHud class, draws the HUD (onscreen display of status information) on the screen (layer)

### include structure

 - pyfense.py includes pyfense_menu
 - pyfense_menu includes all Menu layers
 - pyfense_level includes PyFenseGame
 - pyfense_game includes PyFenseMap, PyFenseEntities, PyFenseHud
 - pyfense_entities includes PyFenseTower, PyFenseEnemy, PyFenseProjectile 

### scene structure
 - menu class creates scenes by calling Scene(PyFenseSettings())
 - shall new scenes replace old scene or push onto stack?
