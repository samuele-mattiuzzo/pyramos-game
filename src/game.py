# -*- coding: utf-8 -*-
try:
	import os
	import pygame
	import datetime
	from pygame.locals import *

	from .classes.player import Player
	from .classes.level import Level
	from .render.stages import LEVELS
	from .render.ui import GameUi
	from .render.engine import GameGraphics

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class Game:

	def __init__(self, level_id=0):
		# the Game class' attributes are all private
		self.__level_id = level_id
		self.__player = None
		self.__level = None
		self.__g = None
		self.__ui = None

		self.__move = None  # used to store the current move
		self.__running = False  # used to determine if the game is running or not

	def init(self):
		self.__level = Level(self.__level_id)
		self.__player = Player()
		self.__player.new_start(self.__level.start)
		self.__g = GameGraphics()
		self.__ui = GameUi()
		self.__CLOCK = None

	def new_game(self):
		self.init()
		self.__ui.start_screen()
		if self.__ui.new_game:
			self.execute()
		elif self.__ui.quit_game:
			self.cleanup()
			pygame.quit()

	def reset(self):
		self.__level_id = 0
		self.__move = None

		self.__level = Level(self.__level_id)
		self.__player.reset()
		self.__player.new_start(self.__level.start)

		self.__g.reset()
		self.__ui.reset()

	def end(self):
		pass

	def on_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.__move = self._new_valid_pos(event.key)

	def cleanup(self):
		self.__running = False

	def execute(self):
		self.__running = True
		self.__CLOCK = pygame.time.Clock()

		self._draw_level()
		start_ticks = pygame.time.get_ticks()

		while(self.__running):
			# main game loop
			for event in pygame.event.get():
				self.on_event(event)
			self.update()

			elapsed = (pygame.time.get_ticks()-start_ticks)/1000
			elapsed = str(datetime.timedelta(seconds=int(elapsed)))
			self.__ui.overlay(self.__player, self.__level, elapsed)

			self.__CLOCK.tick(60)

	def update(self):
		if self.__move:
			valid, tmp_pos, fluke = self.__move
			if not fluke:
				if not valid:
					if self.__player.is_dead:
						self._handle_death()
					else:
						self.__player.add_death()
						self.__player.update_pos(self.__level.start)
				else:
					self._draw_move(tmp_pos)
					if self.__player.pos != tmp_pos:
						self.__player.update_pos(tmp_pos)
					self._handle_move()

	# internal utilities
	def _new_valid_pos(self, key_pressed):
		fluke = False
		pos = x, y = self.__player.pos

		if key_pressed == pygame.K_LEFT and y>0:
			if self.__level.design[x][y-1] != 0:
				pos = (x, y-1)

		elif key_pressed == pygame.K_RIGHT and y<self.__level.size[1]-1:
			if self.__level.design[x][y+1] != 0:
				pos = (x, y+1)

		elif key_pressed == pygame.K_UP and x>0:
			if self.__level.design[x-1][y] != 0:
				pos = (x-1, y)

		elif key_pressed == pygame.K_DOWN and x<self.__level.size[0]-1:
			if self.__level.design[x+1][y] != 0:
				pos = (x+1, y)
		else:
			fluke = True

		valid = (pos != self.__player.pos)
		return valid, pos, fluke

	def _next_level(self):
		self.__level_id += 1
		self.__level = Level(self.level_id)
		self.__player.new_start(self.__level.start)
		self.__move = None
		self._draw_level()

	def _check_end(self):
		return self.__player.pos == self.__level.end

	def _check_has_more_levels(self):
		return self.level_id + 1 < len(LEVELS)

	def _draw_move(self, pos):
		self.__g.update_game(self.__level, pos)

	def _draw_level(self):
		self.__g.display_game(self.__level)

	def _handle_move(self):
		if self._check_end():
			self._handle_end_level()
			if self._check_has_more_levels():
				self._next_level()
			else:
				self._handle_end_game(victory=True)

	def _handle_death(self):
		self._handle_end_game()

	def _handle_end_level(self):
		self.__player.update_best_score(
			self.__level_id,
			self.__level.name,
			self.__player.moves
		)
		self.__ui.end_level_screen(self.__player, self.__level)

	def _handle_end_game(self, victory=False):
		self.__player.update_best_score(
			self.__level_id,
			self.__level.name,
			self.__player.moves
		)
		self.__ui.end_game_screen(self.__player, victory)

		if self.__ui.new_game:
			self.reset()
			self.new_game()

		elif self.__ui.quit_game:
			self.cleanup()
			pygame.quit()

	# getters
	@property
	def player(self):
		return self.__player

	@property
	def level_id(self):
		return self.__level_id

	@property
	def level(self):
		return self.__level

	@property
	def g(self):
		return self.__g
