# Roadmap

## User Stories

- User opens program and is greeted by a welcome screen
- User can click on the start button on the welcome screen and enter his name
- User sees the map with the path that the enemies are going to take
- The user can place towers on predefined areas on the map, which do not interfere with the enemy's path
- Building towers cost currency, depending on the tower.
- User has 30 seconds to start building his first towers, he starts off with a fixed amount of currency
- The user knows when the next wave of enemys will come due to the countdown displayed on the screen
- To build towers, the user clicks on a cell (area of the map) and a menu will pop-up, presenting the player the available towers to build
- The towers attack the first enemy in range until he is dead and then proceeds to attack the second in line
- Whenever the User's tower kill an enemy, he will gain currency depending on the killed enemy type
- If the user clicks on a cell which is already occupied by a tower, he is prompted to upgrade or tear down the selected tower
- The user can see the number of the current wave, displayed as a counter
- Whenever an enemy makes it across the map alive, the user loses one live and said enemy is gone
- If the user loses all his lives (e.g. 50), he loses the game and it is over
- If the user manages to kill all waves of enemies (e.g. 50) before losing all his lives, he wins the game
- After a game is finished, the user's high score (last wave #) is saved to a file including his entered name
- In the statusbar, the following values are being displayed: current wave #, remaining lives, currency, next wave countdown

## Development Plan / Milestones

- Show 2D world (basically an image)
- Show 2D world with tower placeholders, which can be build
- Additionally display enemies (no functionality yet, just moving) and tower projectiles
- Enemies can die due to towers
- Enemies and Towers get nice sprites, menus are visually pleasing to look at

## Internal and external Interface

- extern: load settings and enemy waves from text configuration file and maps, user-input from keyboard and mouse, output on screen
- intern: communication between enemy/towers-modules and the main-routine 

## Git

- master branch is always the last "stable" version
- active dev work should be done on beta branch or personal branches (to discuss)

## Assets

- textures/images are to be saved as *.png files 
- textrues/assets are to be stored in the assets/ directory

## To-Do

- zeitplan für milestones festlegen (direkt in git?)
- geschosse zeichnen
