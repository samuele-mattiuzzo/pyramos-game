import os, sys
# size of the viewport (10 x 10 tiles)
# C:\Python\27\python.exe .\main.py
# cd .\Documents\GitHub\pyramos-game
WINDOW_SIZE = (960, 960)

# size of each square (32 x 32 pixels)
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = (96, 96)

# size of the level (10 x 10 squares)
LEVEL_SIZE = LEVEL_WIDTH, LEVEL_HEIGHT = (10, 10)

# sprite names
wa_spr = os.sep.join([os.getcwd(), "resources", "imgs", 	"tile_wall.png"])
p_spr = os.sep.join([os.getcwd(), "resources", "imgs", 		"tile_player.png"])
wlk_spr = os.sep.join([os.getcwd(), "resources", "imgs",	"tile_walk.png"])
s_spr = os.sep.join([os.getcwd(), "resources", "imgs",		"tile_start.png"])
e_spr = os.sep.join([os.getcwd(), "resources", "imgs",		"tile_end.png"])