try:
	import pygame
	from pygame.locals import *
	#import pgu
except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class Graphics:
	'''
		Main class for handling GUI and on-screen messages
		- [X] draw level
		- [X] update level
		- [ ] level info
		- [X] player moves
		- [X] player deathcounts
		- [ ] scores and online charts
	'''

	def __init__(self, TILE_HEIGHT, TILE_WIDTH, WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE):
        self.GAME_AREA = pygame.Surface(screen.get_size())

        self.WALK_SPRITE = WALK_SPRITE
		self.PLAYER_SPRITE = PLAYER_SPRITE
		self.WALL_SPRITE = WALL_SPRITE
		self.START_SPRITE = START_SPRITE
		self.END_SPRITE = END_SPRITE
		self.TILE_HEIGHT = TILE_HEIGHT
		self.TILE_WIDTH = TILE_WIDTH

        self.TILE_MAP = {
			0: self.WALL_SPRITE,
			1: self.WALK_SPRITE,
			2: self.START_SPRITE,
			3: self.END_SPRITE,
			5: self.PLAYER_SPRITE
		}

	def draw_square(self, scr, pos, stype):
		'''
			Draws a single square of type=stype in pos=pos
		'''
		pos = (pos[1]*self.TILE_HEIGHT, pos[0]*self.TILE_WIDTH)

		scr.blit(
			self.TILE_MAP[stype],
			pos
		)

	def display_game(self, screen, game_area, level, player, uncv):
		'''
			Draws the level for the first time
		'''
		for i in range(10): # row
			for j in range(10): # column
				if (i,j) != player.pos:
					self.draw_square(game_area, (i,j), stype=0) # draw covered square

				else:
					self.draw_square(game_area, (i,j), stype=5) # draw player on start position

		# uncovers seen squares (around player)
		self.update_uncovered(screen, game_area, level, player, uncv) # uncovers squares around player

	def display_gui(self, screen):
		pass

	def update_game(self, screen, game_area, player, level, new_pos, uncv):
		'''
			Reset uncovered -> update uncovered
		'''
		self.reset_uncovered(screen, game_area, player, uncv)
		self.update_player(screen, game_area, new_pos)
		player.update_pos(new_pos)
		self.update_uncovered(screen, game_area, level, player, uncv)
		screen.blit(screen, (0, 0))
		pygame.display.flip()

	def update_gui(self, screen):
		'''
			Updates messages on the GUI
		'''
		pass

	def update_player(self, screen, game_area, pos):
		'''
			Moves the player square
		'''
		self.draw_square(game_area, pos, stype=5) # moves the player
		screen.blit(game_area, (0, 0))

	def update_uncovered(self, screen, game_area, level, player, UNCOVERED):
		'''
			Uncovers squares around the player
		'''
		lmap = level.design
		player_pos = player.pos

		# control top
		UNCOVERED["top"] = (player_pos[0]-1, player_pos[1])
		if UNCOVERED["top"][0] > -1:
			self.draw_square(game_area,
				UNCOVERED["top"], # pos * tile size
				stype=lmap[UNCOVERED["top"][0]][UNCOVERED["top"][1]]) # square type from map

		# control right
		UNCOVERED["right"] = (player_pos[0], player_pos[1]+1)
		if UNCOVERED["right"][1] < 10:
			self.draw_square(game_area,
				UNCOVERED["right"], # pos * tile size
				stype=lmap[UNCOVERED["right"][0]][UNCOVERED["right"][1]]) # square type from map

		# control bottom
		UNCOVERED["bottom"] = (player_pos[0]+1, player_pos[1])
		if UNCOVERED["bottom"][0] < 10:
			self.draw_square(game_area,
				UNCOVERED["bottom"], # pos * tile size
				stype=lmap[UNCOVERED["bottom"][0]][UNCOVERED["bottom"][1]]) # square type from map

		# control left
		UNCOVERED["left"] = (player_pos[0], player_pos[1]-1)
		if UNCOVERED["left"][0] > -1:
			self.draw_square(game_area,
				UNCOVERED["left"], # pos * tile size
				stype=lmap[UNCOVERED["left"][0]][UNCOVERED["left"][1]]) # square type from map

		screen.blit(game_area, (0, 0))

	def reset_uncovered(self, screen, game_area, player, UNCOVERED):
		'''
			Resets lastly seen squares
		'''

		pos = player.pos
		if UNCOVERED["top"][0] > -1 and not UNCOVERED["top"] == pos:
			self.draw_square(game_area, UNCOVERED["top"], stype=0)

		if UNCOVERED["right"][1] < 10 and not UNCOVERED["right"] == pos:
			self.draw_square(game_area, UNCOVERED["right"], stype=0)

		if UNCOVERED["bottom"][0] < 10 and not UNCOVERED["bottom"] == pos:
			self.draw_square(game_area, UNCOVERED["bottom"], stype=0)

		if UNCOVERED["left"][1] > -1 and not UNCOVERED["left"] == pos:
			self.draw_square(game_area, UNCOVERED["left"], stype=0)

		screen.blit(game_area, (0, 0))
