try:
	import os
	import pygame
	from pygame.locals import *

	from main_game.level import *
	from main_game.player import *
	from main_game.square import *
	from main_game.gui import *
	from main_game.system import *

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class Game:

	def __init__(self, level_id=0, all_levels=[]):
		self.player = None
		self.level_id = level_id
		self.level = None
		self.levels = all_levels
		self.settings = {}

		self.init()

	def init(self):
		self.level = Level(self.level_id)
		self.player = Player()
		self.player.new_start(self.level.start)

	def start(self):
		pass

	def end(self):
		pass

	def update(self):
		pass

	def next_level(self):
		self.level_id += 1
		self.level = Level(self.level_id)

	def _get_settings(self):
		pass

	def _get_level(self):
		pass

	def _get_player(self):
		pass

	def _check_end(self):
		return self.player.pos == self.level.end

	def _check_has_more_levels(self):
		return self.level_id + 1 == len(self.levels)
