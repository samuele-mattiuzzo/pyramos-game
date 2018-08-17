try:
	import pygame
	from pygame.locals import *

	from main_game.system import *
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

	def __init__(self):
		self._SYS = System()
		self.on_init()

	def on_init(self):
		self._SYS.get_properties()

		self.SCREEN = self._SYS.get_screen()
		self.GAME_AREA = pygame.Surface(self.SCREEN.get_size())

		(self.WALL_SPRITE,
		self.PLAYER_SPRITE,
		self.WALK_SPRITE,
		self.START_SPRITE,
		self.END_SPRITE) = self._SYS.load_images()

		self.TILE_HEIGHT, self.TILE_WIDTH = self._SYS.get_images_properties()

		self.TILE_MAP = {
			0: self.WALL_SPRITE,
			1: self.WALK_SPRITE,
			2: self.START_SPRITE,
			3: self.END_SPRITE,
			5: self.PLAYER_SPRITE
		}

		self.UNCOVERED = {
			#"dir":	 x,y
			"top" : 	(),
			"right" : 	(),
			"bottom" : 	(),
			"left" : 	(),
		}

	def draw_square(self, pos, stype):
		'''
			Draws a single square of type=stype in pos=pos
		'''

		self.GAME_AREA.blit(
			self.TILE_MAP[stype],
			(pos[1]*self.TILE_HEIGHT, pos[0]*self.TILE_WIDTH)
		)

	def display_game(self, level, player):
		'''
			Draws the level for the first time
		'''

		for i in range(10): # row
			for j in range(10): # column
				if (i, j) != player.pos:
					self.draw_square((i, j), stype=0) # draw covered square
				else:
					self.draw_square((i, j), stype=5) # draw player on start position

		# uncovers seen squares (around player)
		self.update_uncovered(level, player) # uncovers squares around player

	def display_gui(self):
		pass

	def update_game(self, player, level, new_pos):
		'''
			Reset uncovered -> update uncovered
		'''
		self.reset_uncovered(player)
		self.update_player(new_pos)
		player.update_pos(new_pos)
		self.update_uncovered(level, player)
		self.SCREEN.blit(self.SCREEN, (0, 0))
		pygame.display.flip()

	def update_gui(self):
		'''
			Updates messages on the GUI
		'''
		pass

	def update_player(self, pos):
		'''
			Moves the player square
		'''
		self.draw_square(pos, stype=5) # moves the player
		self.SCREEN.blit(self.GAME_AREA, (0, 0))

	def update_uncovered(self, level, player):
		'''
			Uncovers squares around the player
		'''
		lmap = level.design
		player_pos = player.pos

		# control top
		self.UNCOVERED["top"] = (player_pos[0]-1, player_pos[1])
		if self.UNCOVERED["top"][0] > -1:
			self.draw_square(
				self.UNCOVERED["top"], # pos * tile size
				stype=lmap[self.UNCOVERED["top"][0]][self.UNCOVERED["top"][1]]) # square type from map

		# control right
		self.UNCOVERED["right"] = (player_pos[0], player_pos[1]+1)
		if self.UNCOVERED["right"][1] < 10:
			self.draw_square(
				self.UNCOVERED["right"], # pos * tile size
				stype=lmap[self.UNCOVERED["right"][0]][self.UNCOVERED["right"][1]]) # square type from map

		# control bottom
		self.UNCOVERED["bottom"] = (player_pos[0]+1, player_pos[1])
		if self.UNCOVERED["bottom"][0] < 10:
			self.draw_square(
				self.UNCOVERED["bottom"], # pos * tile size
				stype=lmap[self.UNCOVERED["bottom"][0]][self.UNCOVERED["bottom"][1]]) # square type from map

		# control left
		self.UNCOVERED["left"] = (player_pos[0], player_pos[1]-1)
		if self.UNCOVERED["left"][0] > -1:
			self.draw_square(
				self.UNCOVERED["left"], # pos * tile size
				stype=lmap[self.UNCOVERED["left"][0]][self.UNCOVERED["left"][1]]) # square type from map

		self.SCREEN.blit(self.GAME_AREA, (0, 0))

	def reset_uncovered(self, player):
		'''
			Resets lastly seen squares
		'''

		pos = player.pos
		if self.UNCOVERED["top"][0] > -1 and not self.UNCOVERED["top"] == pos:
			self.draw_square(self.UNCOVERED["top"], stype=0)

		if self.UNCOVERED["right"][1] < 10 and not self.UNCOVERED["right"] == pos:
			self.draw_square(self.UNCOVERED["right"], stype=0)

		if self.UNCOVERED["bottom"][0] < 10 and not self.UNCOVERED["bottom"] == pos:
			self.draw_square(self.UNCOVERED["bottom"], stype=0)

		if self.UNCOVERED["left"][1] > -1 and not self.UNCOVERED["left"] == pos:
			self.draw_square(self.UNCOVERED["left"], stype=0)

		self.SCREEN.blit(self.GAME_AREA, (0, 0))
