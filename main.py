try:

	# pygame + general imports
	import pygame, sys,os
	from pygame.locals import *

	# resource imports
	from resources.config import *
	from resources.levels import *

	# main game classes imports
	from main_game.level import *
	from main_game.player import *
	from main_game.square import *
	from main_game.gui import *
	from main_game.system import *

except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)

## GLOBAL VARIABLES
UNCOVERED = {
	#"dir":     x,y
	"top" : 	(),
	"right" : 	(),
	"bottom" : 	(),
	"left" : 	(),
}

# pygame init and screen global variable
pygame.init()
game_sys = System()
game_sys.get_properties()
screen = game_sys.get_screen()

# tiles preloading
WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE = game_sys.load_images()
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = game_sys.get_images_properties()

# gui elements preloading (NotYetImplemented)
# LEVEL_NAME, LEVEL_TOP_SCORE, LEVEL ID+1, GAME_MODE, PLAYER_MOVES, PLAYER_DEATHS, PLAYER_TOP

# gui creation
g = Graphics(TILE_HEIGHT, TILE_WIDTH, WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE)

# loads up a new level: tiles and render
def loadLevel(lid):
	return Level(lid)

# tbd
def newGame():
	pygame.display.set_caption('Pyramos - a game written in python and pygame (Samuele Mattiuzzo - samumatt@gmail.com)') 

# checks the end square
def checkEndLevel(player_pos, end):
	return player_pos == end

# checks for the new player move and returns the new position. false if it's not (player dies!)
def newValidPos(player_pos, keyName, lmap):
	valid = False
	is_dead = False
	pos = player_pos

	if keyName == "LEFT" and player_pos[1]>0:
		if lmap[player_pos[0]][player_pos[1]-1] != 0:
			pos = (pos[0], pos[1]-1)
			valid = True
		else:
			is_dead = True

	if keyName == "RIGHT" and player_pos[1]<9:
		if lmap[player_pos[0]][player_pos[1]+1] != 0:
			pos = (pos[0], pos[1]+1)
			valid = True
		else:
			is_dead = True

	if keyName == "UP" and player_pos[0]>0:
		if lmap[player_pos[0]-1][player_pos[1]] != 0:
			pos = (pos[0]-1, pos[1])
			valid = True
		else:
			is_dead = True

	if keyName == "DOWN" and player_pos[0]<9:
		if lmap[player_pos[0]+1][player_pos[1]] != 0:
			pos = (pos[0]+1, pos[1])
			valid = True
		else:
			is_dead = True

	return valid, is_dead, pos



def main():

	# pygame.init, level loading and player creation
	game_area = pygame.Surface(screen.get_size())
	level = loadLevel(0)
	player = Player(level.start)

	#time is specified in milliseconds
	#fixed simulation step duration
	step_size = 1000
	#max duration to render a frame
	max_frame_time = 100
	now = pygame.time.get_ticks()

	# first draw
	g.display_game(game_area, level, player, UNCOVERED)

	screen.blit(game_area, (0, 0))
	pygame.display.flip()

	valid = is_dead = False
	tmp_pos = player.pos
	pressed = ""

	while(True):
		#handle events

		for event in pygame.event.get():
			if event.type == QUIT:
				print "Bye!"
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()

				elif event.key == pygame.K_UP:
					pressed = "UP"

				elif event.key == pygame.K_DOWN:
					pressed = "DOWN"

				elif event.key == pygame.K_RIGHT:
					pressed = "RIGHT"

				elif event.key == pygame.K_LEFT:
					pressed = "LEFT"

				valid, is_dead, tmp_pos = newValidPos(player.pos, pressed, level.design)

		if is_dead:
			print "You touched a poisonous wall! You are dead!"
			print "Your score is: " + str(player.moves)
			print "Bye!"
			sys.exit()

		else:
			if valid:
				# actually moves the player
				valid = False
				g.update_game(game_area, player, level, UNCOVERED)
				player.updatePos(tmp_pos)

				if checkEndLevel(player.pos, level.end):
					print "YOU WON!"
					if player.moves <= level.completion:
						print "CHAMPION SCORE! You made " + str(player.moves) + " step and you're a champion!"
					else:
						print "Not bad, it took you more than we expected..."
					print "Bye!"
					sys.exit()

				# reset - uncover
				
				screen.blit(game_area, (0, 0))
				pygame.display.flip()

		#get the current real time
		T = pygame.time.get_ticks()

		#if elapsed time since last frame is too long...
		if T-now > max_frame_time:
			#slow the game down by resetting clock
			now = T - step_size
			#alternatively, do nothing and frames will auto-skip, which
			#may cause the engine to never render!

		#this code will run only when enough time has passed, and will
		#catch up to wall time if needed.
		while(T-now >= step_size):
			pygame.display.set_caption(level.name + "("+str(level.completion)+") | " + player.name + "("+str(player.moves)+")") 
			#save old game state, update new game state based on step_size
			now += step_size
		else:
			pygame.time.wait(10)

		#render game state. use 1.0/(step_size/(T-now)) for interpolation

if __name__ == "__main__":
	main()