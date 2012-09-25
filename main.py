import pygame, sys,os
from pygame.locals import *
from resources.config import *
from resources.levels import *
from main_game import gui, level, player, square 
 
def main():
	pygame.init()
	pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption(LEVEL_1['name']) 

	#time is specified in milliseconds
	#fixed simulation step duration
	step_size = 20

	#max duration to render a frame
	max_frame_time = 100

	now = pygame.time.get_ticks()

	while(True):
		#handle events
		if QUIT in [e.type for e in pygame.event.get()]:
			break

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