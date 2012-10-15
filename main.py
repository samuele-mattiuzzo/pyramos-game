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

# pygame init and screen global variable
pygame.init()
game_sys = System()
game_sys.get_properties()
screen = game_sys.get_screen()

# tiles preloading
WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE = game_sys.load_images()
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = game_sys.get_images_properties()

# level preconfiguration
LEVEL_ID = 0 # beginning of the game
LEVEL = Level(LEVEL_ID)
PLAYER = Player()
PLAYER.newStart(LEVEL.start)
GAME_AREA = pygame.Surface(screen.get_size())
UNCOVERED = {
	#"dir":     x,y
	"top" : 	(),
	"right" : 	(),
	"bottom" : 	(),
	"left" : 	(),
}

# gui elements preloading (NotYetImplemented)
# LEVEL_NAME, LEVEL_TOP_SCORE, LEVEL ID+1, GAME_MODE, PLAYER_MOVES, PLAYER_DEATHS, PLAYER_TOP

# graphics creation
g = Graphics(TILE_HEIGHT, TILE_WIDTH, WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE)

def nextLevel():
	global LEVEL, PLAYER, GAME_AREA
	if not LEVEL_ID == LEVEL.id:	
		LEVEL = Level(LEVEL_ID)
		PLAYER.newStart(LEVEL.start)

	g.display_game(screen, GAME_AREA, LEVEL, PLAYER, UNCOVERED)
	screen.blit(GAME_AREA, (0, 0))
	pygame.display.flip()

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
	#time is specified in milliseconds
	#fixed simulation step duration
	step_size = 500
	#max duration to render a frame
	max_frame_time = 100
	now = pygame.time.get_ticks()

	# first draw
	nextLevel()

	__cycle = True
	valid = is_dead = False
	tmp_pos = PLAYER.pos
	pressed = ""

	while(__cycle):
		#handle events

		for event in pygame.event.get():
			if event.type == QUIT:
				print "Bye!"
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				else:
					if event.key == pygame.K_UP:
						pressed =  "UP"  
					elif event.key == pygame.K_DOWN: 
						pressed =  "DOWN" 
					elif event.key == pygame.K_RIGHT:
						pressed =  "RIGHT" 
					elif event.key == pygame.K_LEFT:
						pressed =  "LEFT" 

				valid, is_dead, tmp_pos = newValidPos(PLAYER.pos, pressed, LEVEL.design)

		if is_dead:
			print "You touched a poisonous wall! You are dead!"
			print "Your score is: " + str(PLAYER.moves)
			print "Bye!"
			sys.exit()

		else:
			if valid:
				# actually moves the player
				valid = False
				g.update_game(screen, GAME_AREA, PLAYER, LEVEL, tmp_pos, UNCOVERED)
				# reset - uncover
				screen.blit(GAME_AREA, (0, 0))
				pygame.display.flip()

				if checkEndLevel(PLAYER.pos, LEVEL.end):
					global LEVEL_ID
					LEVEL_ID += 1
					if LEVEL_ID < len(LEVELS):
						nextLevel() # continue
					else:
						print "YOU WON!"
						print "You completed " + str(LEVEL_ID) + " stages with a total of " + str(PLAYER.moves) + " steps"
						__cycle = False

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
			#save old game state, update new game state based on step_size
			now += step_size
		else:
			pygame.time.wait(10)

		#render game state. use 1.0/(step_size/(T-now)) for interpolation

if __name__ == "__main__":
	main()