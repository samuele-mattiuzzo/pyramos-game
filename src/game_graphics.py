# -*- coding: utf-8 -*-
try:
	import pygame
	from pygame.locals import *

	from src.system import System
	from src.tile import Tile

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class GameGraphics:
	'''
		Main class for handling in-game graphics (tiles and player)
	'''

	def __init__(self):
		self.__SYS = System()
		self.on_init()

	def on_init(self):
		self.__SYS.get_properties()

		self.__SCREEN = self.__SYS.get_screen()
		self.__GAME_AREA = pygame.Surface(self.__SCREEN.get_size())

		self._setup_tile_map()
		self._setup_game_tiles()

	def _setup_tile_map(self):
		(self.__WALL_SPRITE,
		self.__PLAYER_SPRITE,
		self.__WALK_SPRITE,
		self.__START_SPRITE,
		self.__END_SPRITE) = self.__SYS.load_images()

		self.__TILE_MAP = {
			0: self.__WALL_SPRITE,
			1: self.__WALK_SPRITE,
			2: self.__START_SPRITE,
			3: self.__END_SPRITE,
			5: self.__PLAYER_SPRITE
		}

	def _setup_game_tiles(self):

		origin = self.__SYS.get_screen_origin()
		offset_x, offset_y = self.__SYS.tile_size

		self.__GAME_TILES = {
			"top": Tile(x=origin[0], y=origin[1]-offset_y, pos="top"),
			"bottom": Tile(x=origin[0], y=origin[1]+offset_y, pos="bottom"),
			"left": Tile(x=origin[0]-offset_x, y=origin[1], pos="left"),
			"right": Tile(x=origin[0]+offset_x, y=origin[1], pos="right"),
			"player": Tile(x=origin[0], y=origin[1], pos="player")
		}

	def draw_tile(self, tile):
		'''
			Draws a single square
		'''

		self.__GAME_AREA.blit(
			self.__TILE_MAP[tile.type],
			(tile.x, tile.y)
		)

	def display_game(self, level):
		'''
			Draws the level for the first time
		'''
		self.update_game(level, level.start)

	def update_game(self, level, new_pos):
		'''
			Reset uncovered -> update uncovered
		'''
		self.__GAME_TILES = self.update_tiles(level, new_pos)
		self.draw_tiles()

		self.__SCREEN.blit(self.__SCREEN, (0, 0))
		pygame.display.flip()

	def update_tiles(self, level, new_pos):
		tiles_copy = self.__GAME_TILES.copy()
		for k in tiles_copy.keys():
			tiles_copy[k].type = self._get_tile_type(
				level, new_pos, tiles_copy[k].pos
			)
		return tiles_copy

	def draw_tiles(self):
		for _, tile in self.__GAME_TILES.items():
			self.draw_tile(tile)
			self.__SCREEN.blit(self.__GAME_AREA, (0, 0))

	def _get_tile_type(self, level, new_pos, tile_pos):
		'''
			Uncovers squares around the player
		'''

		new_type = 0

		if tile_pos == "top":
			x, y = (new_pos[0]-1, new_pos[1])
			if x > -1:
				new_type = level.design[x][y]

		elif tile_pos == "bottom":
			x, y = (new_pos[0]+1, new_pos[1])
			if x < 10:
				new_type = level.design[x][y]

		elif tile_pos == "right":
			x, y = (new_pos[0], new_pos[1]+1)
			if y < 10:
				new_type = level.design[x][y]

		elif tile_pos == "left":
			x, y = (new_pos[0], new_pos[1]-1)
			if y > -1:
				new_type = level.design[x][y]

		elif tile_pos == "player":
			return 5

		return new_type
