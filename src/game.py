# -*- coding: utf-8 -*-
try:
	import os
	import pygame
	from pygame.locals import *

	from src.game_stages import LEVELS
	from src.level import Level
	from src.player import Player
	from src.game_ui import GameUi
	from src.game_graphics import GameGraphics

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

	def new_game(self):
		self.init()
		self.__ui.start_screen()
		self.execute()

	def end(self):
		pass

	def on_event(self, event):
		if event.type == QUIT:
			self.cleanup()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.cleanup()
			else:
				self.__move = self._new_valid_pos(event.key)

	def cleanup(self):
		self.__running = False
		print("Bye!")
		pygame.quit()

	def execute(self):
		#time is specified in milliseconds
		#fixed simulation step duration
		#max duration to render a frame
		step_size, max_frame_time = 500, 100
		now = pygame.time.get_ticks()
		self.__running = True

		self._draw_level()

		while(self.__running):
			# main game loop
			for event in pygame.event.get():
				self.on_event(event)
			self.update()

			#get the current real time
			T = pygame.time.get_ticks()

			#if elapsed time since last frame is too longame.GUI...
			if T-now > max_frame_time:
				now = T - step_size  #slow the game down by resetting clock

			#this code will run only when enough time has passed, and will
			#catch up to wall time if needed.
			while(T-now >= step_size):
				now += step_size  #save old game state, update new game state based on step_size
			else:
				pygame.time.wait(10)

		self.cleanup()

	def update(self):
		if self.__move:
			valid, tmp_pos = self.__move
			if not valid:
				self._handle_death()
			else:
				self._draw_move(tmp_pos)
				self._handle_move()

	# internal utilities
	def _new_valid_pos(self, key_pressed):
		valid = False
		pos = x, y = self.__player.pos

		if key_pressed == pygame.K_LEFT and y>0:
			if self.__level.design[x][y-1] != 0:
				pos = (x, y-1)
				valid = True

		if key_pressed == pygame.K_RIGHT and y<9:
			if self.__level.design[x][y+1] != 0:
				pos = (x, y+1)
				valid = True

		if key_pressed == pygame.K_UP and x>0:
			if self.__level.design[x-1][y] != 0:
				pos = (x-1, y)
				valid = True

		if key_pressed == pygame.K_DOWN and x<9:
			if self.__level.design[x+1][y] != 0:
				pos = (x+1, y)
				valid = True

		return valid, pos

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
		self.__g.update_game(self.__player, self.__level, pos)

	def _draw_level(self):
		self.__g.display_game(self.__player, self.__level)

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
