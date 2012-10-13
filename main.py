import pygame, sys,os
from pygame.locals import *
from resources.config import *
from resources.levels import *
from main_game.level import *
from main_game.player import *
from main_game.square import *
from main_game.gui import *

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

# utility variables 

UNCOVERED = {
	#            x  y
	"top" : 	(7, 0) ,
	"right" : 	(8, 1) ,
	"bottom" : 	(9, 0),
	"left" : 	(8, -1),
}

# pygame init + image preloading
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

WALL_SPRITE = pygame.image.load(wa_spr).convert()
PLAYER_SPRITE = pygame.image.load(p_spr).convert()
WALK_SPRITE = pygame.image.load(wlk_spr).convert()
START_SPRITE = pygame.image.load(s_spr).convert()
END_SPRITE = pygame.image.load(e_spr).convert()


# draws single square (pox * 32 px on screen)
def drawSquare(scr, pos, stype):
	pos = (pos[1]*TILE_HEIGHT, pos[0]*TILE_WIDTH)

	if stype == 0: # wall
		scr.blit(WALL_SPRITE, pos)

	elif stype == 1: # walking
		scr.blit(WALK_SPRITE, pos)

	elif stype == 2: # start
		scr.blit(START_SPRITE, pos)

	elif stype == 3: # end
		scr.blit(END_SPRITE, pos)

	elif stype == 5: # player
		scr.blit(PLAYER_SPRITE, pos)

# global
def firstDraw(player, level, scr):

	# draws all squares covered + player
	for i in range(LEVEL_HEIGHT): # row
		for j in range(LEVEL_WIDTH): # column
			if (i,j) != player.pos:
				drawSquare(scr, (i,j), stype=0) # draw covered square
			
			else:
				drawSquare(scr, (i,j), stype=5) # draw player on start position

	# uncovers seen squares (around player)
	updateUncovered(player.pos, level.design, scr) # uncovers squares around player

# graphical: resets back to WALL_SPRITE
def resetUncovered(scr, pos):
	if UNCOVERED["top"][0] > -1 and not UNCOVERED["top"] == pos:
		drawSquare(scr, UNCOVERED["top"], stype=0)

	if UNCOVERED["right"][1] < 10 and not UNCOVERED["right"] == pos:
		drawSquare(scr, UNCOVERED["right"], stype=0)

	if UNCOVERED["bottom"][0] < 10 and not UNCOVERED["bottom"] == pos:
		drawSquare(scr, UNCOVERED["bottom"], stype=0)

	if UNCOVERED["left"][1] > -1 and not UNCOVERED["left"] == pos:
		drawSquare(scr, UNCOVERED["left"], stype=0)


# updates the new coordinates and uncovers them
def updateUncovered(player_pos, lmap, scr):
	# control top
	UNCOVERED["top"] = (player_pos[0]-1, player_pos[1])
	if UNCOVERED["top"][0] > -1:
		drawSquare(scr, 
			UNCOVERED["top"], # pos * tile size
			stype=lmap[UNCOVERED["top"][0]][UNCOVERED["top"][1]]) # square type from map

	# control right
	UNCOVERED["right"] = (player_pos[0], player_pos[1]+1)
	if UNCOVERED["right"][1] < 10:
		drawSquare(scr, 
			UNCOVERED["right"], # pos * tile size
			stype=lmap[UNCOVERED["right"][0]][UNCOVERED["right"][1]]) # square type from map

	# control bottom
	UNCOVERED["bottom"] = (player_pos[0]+1, player_pos[1])
	if UNCOVERED["bottom"][0] < 10:
		drawSquare(scr, 
			UNCOVERED["bottom"], # pos * tile size
			stype=lmap[UNCOVERED["bottom"][0]][UNCOVERED["bottom"][1]]) # square type from map

	# control left
	UNCOVERED["left"] = (player_pos[0], player_pos[1]-1)
	if UNCOVERED["left"][0] > -1:
		drawSquare(scr, 
			UNCOVERED["left"], # pos * tile size
			stype=lmap[UNCOVERED["left"][0]][UNCOVERED["left"][1]]) # square type from map

	screen.blit(scr, (0, 0))
	pygame.display.flip()

# loads up a new level: tiles and render
def loadLevel(lid):
	return Level(lid)

# tbd
def newGame():
	pygame.display.set_caption('Pyramos - a game written in python and pygame (Samuele Mattiuzzo - samumatt@gmail.com)') 

# checks the end square
def checkEndLevel(player_pos, end):
	return player_pos == end

# actually moves the player tile
def movePlayer(player, pos, scr):
	drawSquare(scr, pos, stype=5) # moves the player

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

	PLAYER_MOVES = 0
	# pygame.init
	game_area = pygame.Surface(screen.get_size())


	level = loadLevel(0)
	player = Player(level.start)

	#time is specified in milliseconds
	#fixed simulation step duration
	step_size = 1000
	#max duration to render a frame
	max_frame_time = 100
	now = pygame.time.get_ticks()

	firstDraw(player, level, game_area)

	screen.blit(game_area, (0, 0))
	pygame.display.flip()

	valid = False
	is_dead = False
	tmp_pos = player.pos
	pressed = ""

	while(True):
		#handle events

		for event in pygame.event.get():
			if event.type == QUIT:
				print "Bye!"
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
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
			print "Your score is: " + str(PLAYER_MOVES)
			print "Bye!"
			sys.exit()

		else:
			if valid:
				# actually moves the player
				valid = False
				movePlayer(player, tmp_pos, game_area)
				player.updatePos(tmp_pos)

				if checkEndLevel(player.pos, level.end):
					print "YOU WON!"
					if PLAYER_MOVES == level.completion:
						print "CHAMPION SCORE! You made " + str(PLAYER_MOVES) + " step and you're a champion!"
					else:
						print "Not bad, it took you more than we expected..."
					print "Bye!"
					sys.exit()

				PLAYER_MOVES += 1

				# reset - uncover
				resetUncovered(game_area, player.pos)
				updateUncovered(player.pos, level.design, game_area)
				screen.blit(game_area, (0, 0))
				pygame.display.flip()

				# check for game end

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
			pygame.display.set_caption(level.name + "("+str(level.completion)+") | " + player.name + "("+str(PLAYER_MOVES)+")") 
			#save old game state, update new game state based on step_size
			now += step_size
		else:
			pygame.time.wait(10)

		#render game state. use 1.0/(step_size/(T-now)) for interpolation

if __name__ == "__main__":
	main()