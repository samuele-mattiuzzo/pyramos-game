try:
	import pygame
	from pygame.locals import *
	import pgu
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)


class Graphics:
	'''
		Main class for handling GUI and on-screen messages
		- [X] draw level
		- [X] update level
		- [ ] level info
		- [ ] player moves
		- [ ] player deathcounts
		- [ ] scores and online charts
	'''

	def __init__(self, TILE_HEIGHT, TILE_WIDTH, WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE):
		self.WALK_SPRITE = WALK_SPRITE
		self.PLAYER_SPRITE = PLAYER_SPRITE
		self.WALL_SPRITE = WALL_SPRITE
		self.START_SPRITE = START_SPRITE
		self.END_SPRITE = END_SPRITE
		self.TILE_HEIGHT = TILE_HEIGHT
		self.TILE_WIDTH = TILE_WIDTH

	def drawSquare(self, scr, pos, stype):
		'''
			Draws a single square of type=stype in pos=pos
		'''
		pos = (pos[1]*self.TILE_HEIGHT, pos[0]*self.TILE_WIDTH)

		if stype == 0: # wall
			scr.blit(self.WALL_SPRITE, pos)

		elif stype == 1: # walking
			scr.blit(self.WALK_SPRITE, pos)

		elif stype == 2: # start
			scr.blit(self.START_SPRITE, pos)

		elif stype == 3: # end
			scr.blit(self.END_SPRITE, pos)

		elif stype == 5: # player
			scr.blit(self.PLAYER_SPRITE, pos)

	def display_game(self, screen, level, player, uncv):
		'''
			Draws the level for the first time
		'''
		for i in range(10): # row
			for j in range(10): # column
				if (i,j) != player.pos:
					self.drawSquare(screen, (i,j), stype=0) # draw covered square
			
				else:
					self.drawSquare(screen, (i,j), stype=5) # draw player on start position

		# uncovers seen squares (around player)
		self.update_uncovered(screen, level, player, uncv) # uncovers squares around player

	def display_gui(self, screen):
		pass

	def update_game(self, screen, player, level, uncv):
		'''
			Reset uncovered -> update uncovered
		'''
		self.reset_uncovered(screen, player, uncv)
		self.update_player(screen, player.pos)
		self.update_uncovered(screen, level, player, uncv)
		#screen.blit(screen, (0, 0))
		#pygame.display.flip()

	def update_gui(self, screen):
		'''
			Updates messages on the GUI
		'''
		pass

	def update_player(self, screen, pos):
		'''
			Moves the player square
		'''
		self.drawSquare(screen, pos, stype=5) # moves the player
		#screen.blit(screen, (0, 0))
		#pygame.display.flip()
	
	def update_uncovered(self, screen, level, player, UNCOVERED):
		'''
			Uncovers squares around the player
		'''
		lmap = level.design
		player_pos = player.pos

		# control top
		UNCOVERED["top"] = (player_pos[0]-1, player_pos[1])
		if UNCOVERED["top"][0] > -1:
			self.drawSquare(screen, 
				UNCOVERED["top"], # pos * tile size
				stype=lmap[UNCOVERED["top"][0]][UNCOVERED["top"][1]]) # square type from map

		# control right
		UNCOVERED["right"] = (player_pos[0], player_pos[1]+1)
		if UNCOVERED["right"][1] < 10:
			self.drawSquare(screen, 
				UNCOVERED["right"], # pos * tile size
				stype=lmap[UNCOVERED["right"][0]][UNCOVERED["right"][1]]) # square type from map

		# control bottom
		UNCOVERED["bottom"] = (player_pos[0]+1, player_pos[1])
		if UNCOVERED["bottom"][0] < 10:
			self.drawSquare(screen, 
				UNCOVERED["bottom"], # pos * tile size
				stype=lmap[UNCOVERED["bottom"][0]][UNCOVERED["bottom"][1]]) # square type from map

		# control left
		UNCOVERED["left"] = (player_pos[0], player_pos[1]-1)
		if UNCOVERED["left"][0] > -1:
			self.drawSquare(screen, 
				UNCOVERED["left"], # pos * tile size
				stype=lmap[UNCOVERED["left"][0]][UNCOVERED["left"][1]]) # square type from map

		#screen.blit(screen, (0, 0))
		#pygame.display.flip()

	def reset_uncovered(self, screen, player, UNCOVERED):
		'''
			Resets lastly seen squares
		'''

		pos = player.pos
		if UNCOVERED["top"][0] > -1 and not UNCOVERED["top"] == pos:
			self.drawSquare(screen, UNCOVERED["top"], stype=0)

		if UNCOVERED["right"][1] < 10 and not UNCOVERED["right"] == pos:
			self.drawSquare(screen, UNCOVERED["right"], stype=0)

		if UNCOVERED["bottom"][0] < 10 and not UNCOVERED["bottom"] == pos:
			self.drawSquare(screen, UNCOVERED["bottom"], stype=0)

		if UNCOVERED["left"][1] > -1 and not UNCOVERED["left"] == pos:
			self.drawSquare(screen, UNCOVERED["left"], stype=0)

		#screen.blit(screen, (0, 0))
		#pygame.display.flip()
