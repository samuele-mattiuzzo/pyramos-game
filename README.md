This is **PYRAMOS**, a dungeon crawling puzzle game. Help King Tut reach the end!

The game is developed using PYGAME (http://www.pygame.org/news.html)


##Requirements
- Python (ver. 3.7.0)
- PyGame (ver. 1.9.4)

##Installation
- clone the repository
- create a virtualenv `mkvirtualenv pyramos-game`
- install the requirements `pip install -r requirements.txt`
- run the app `python main.py`


##How To Play:

- use the arrows to move the adventurer
- everytime the adventurer moves, he'll see the valid steps around himself. Walls will not be uncovered. Corners can't be seen around.
- reach the end of the dungeon
- avoid hitting the walls (aka don't try to move toward one of them) or you'll die of a trap

##Dungeon Tiles:

Togheter with the Player tile, there are 4 other tile types:

- wall : don't hit one, or you'll die
- floor : there you go...
- start point : a floor tile marked with a green S
- end point : guess what?

##Author:

Samuele Mattiuzzo <samumatt@gmail.com> &copy; 2018
