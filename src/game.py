# -*- coding: utf-8 -*-
try:
	import os
	import pygame
	import datetime
	from pygame.locals import *

	from .classes.player import Player
	from .classes.level import Level
	from .engine.controller import ControllerMixin
	from .engine.stages import LEVELS
	from .engine.ui import GameUi
	from .engine.game_graphics import GameGraphics

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class Game(ControllerMixin):

	def __init__(self, level_id=0):
		# the Game class' attributes are all private
		super(Game, self).__init__()
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

	def reset(self):
		self.__level_id = 0
		self.__move = None

		self.__level = Level(self.__level_id)
		self.__player.reset()
		self.__player.new_start(self.__level.start)

		self.__g.reset()
		self.__ui.reset()

		self._draw_level()

		self.__CLOCK = pygame.time.Clock()

	def end(self):
		pass

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.cleanup()

		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_ESCAPE]:
				self.cleanup()
				pygame.quit()
			else:
				self.handle_input(
					self.__ui.ui_screen,
					event.key
				)

	def _handle_ui_input(self, ui_screen=None, input=None):
		if input == pygame.K_SPACE:
			if ui_screen == "start":
				self._draw_level()
				self.__ui.toggle()
				self.__g.toggle()
			elif ui_screen == "end_level":
				self._next_level()
				self.__ui.toggle()
				self.__g.toggle()
			elif ui_screen in ["end_game", "defeat"]:
				self.__ui.cleanup()
				self.__ui.toggle()

		elif input in [pygame.K_q, pygame.K_ESCAPE]:
			self.cleanup()
			pygame.quit()
		else:
			pass

	def _handle_game_input(self, input=None):
		self.__move = self._new_valid_pos(input)

	def cleanup(self):
		self.__ui.cleanup()
		self.__g.cleanup()
		self.__running = False

	def execute(self):
		self.__running = True
		self._draw_level()

		start_ticks = pygame.time.get_ticks()

		while(self.__running):
			# main game loop

			self.__ui.overlay(
				self.__player, self.__level,
				self._elapsed_time(start_ticks)
			)
			self.update()

			for event in pygame.event.get():
				self.on_event(event)

			self.__CLOCK.tick(60)
		self.cleanup()

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

	def _handle_death(self):
		self._handle_end_game()

	def _draw_move(self, pos):
		self.__g.update_game(self.__level, pos)

	def _draw_level(self):
		self.__g.update_game(self.__level, self.__level.start)

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
		self.__ui.toggle()
		self.__g.toggle()
		self.__ui.end_level_screen(self.__player, self.__level)

	def _handle_end_game(self, victory=False):
		self.__player.update_best_score(
			self.__level_id,
			self.__level.name,
			self.__player.moves
		)
		self.__ui.toggle()
		self.__g.toggle()
		self.__ui.end_game_screen(self.__player, victory)

	def _elapsed_time(self, ticks):
		elapsed = (pygame.time.get_ticks()-ticks)/1000
		return str(datetime.timedelta(seconds=int(elapsed)))

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
