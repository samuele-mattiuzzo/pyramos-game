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
		self.__CLOCK = pygame.time.Clock()

	def new_game(self):
		self.init()
		self.__ui.start_screen()
		self.execute()

	def end(self):
		pass

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.cleanup()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.cleanup()
			else:
				self.__move = self._new_valid_pos(event.key)

	def cleanup(self):
		self.__running = False
		pygame.quit()

	def execute(self):
		self.__running = True

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
		self.cleanup()

	def update(self):
		if self.__move:
			valid, tmp_pos, fluke = self.__move
			if not fluke:
				if not valid:
					self._handle_death()
				else:
					self._draw_move(tmp_pos)
					if self.__player.pos != tmp_pos:
						self.__player.update_pos(tmp_pos)
					self._handle_move()

	# internal utilities
	def _new_valid_pos(self, key_pressed):
		valid = False
		fluke = False
		pos = x, y = self.__player.pos

		if key_pressed == pygame.K_LEFT and y>0:
			if self.__level.design[x][y-1] != 0:
				pos = (x, y-1)
				valid = True

		elif key_pressed == pygame.K_RIGHT and y<9:
			if self.__level.design[x][y+1] != 0:
				pos = (x, y+1)
				valid = True

		elif key_pressed == pygame.K_UP and x>0:
			if self.__level.design[x-1][y] != 0:
				pos = (x-1, y)
				valid = True

		elif key_pressed == pygame.K_DOWN and x<9:
			if self.__level.design[x+1][y] != 0:
				pos = (x+1, y)
				valid = True
		else:
			fluke = True

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

	def _handle_death(self):
		self._handle_end_game()
		self.__running = False

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
			self.new_game()

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
