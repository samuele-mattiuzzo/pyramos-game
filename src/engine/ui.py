# -*- coding: utf-8 -*-
try:
	import pygame
	from pygame.locals import *

	from .. import config as conf
	from ..system import System

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class GameUi:
	'''
		Main class for handling in-game overlay and game state screens
	'''

	def __init__(self):
		self.__SYS = System()

		self.on_init()

	def on_init(self):
		self.__SYS.get_properties()

		self.__SCREEN = self.__SYS.get_screen()
		self.__ORIGIN = self.__SYS.get_screen_origin_no_offset()

		self.__CLOCK = pygame.time.Clock()

		self.__in_ui = False
		self.__ui_screen = None
		self.__show_overlay = False

	def reset(self):
		self.__SCREEN.fill((0, 0, 0))
		self.__show_overlay = False
		self.__in_ui = False

	def cleanup(self):
		self.__ui_screen = None
		self.__show_overlay = False
		self.__in_ui = False

	@property
	def in_ui(self):
		return self.__in_ui

	def toggle_overlay(self):
		self.__show_overlay = not self.__show_overlay

	def toggle(self):
		self.__in_ui = not self.__in_ui

	@property
	def ui_screen(self):
		return self.__ui_screen

	def _game_footer(self):
		# other options
		self._draw_text(message=conf.UiText.GAME_OPTIONS,
			size=conf.UiText.GAME_FONT_SMALL, y=100)

		self._draw_text(message=conf.UiText.COPY_TEXT,
			size=conf.UiText.GAME_FONT_SMALL, y=200)

	def start_screen(self):
		self.__SCREEN.fill((0,0,0))
		self.__ui_screen = "start"
		self.__in_ui = True

		# game title
		self._draw_text(message=conf.UiText.GAME_TITLE, y=-200)

		# new game
		self._draw_text(message=conf.UiText.GAME_NEW,
			size=conf.UiText.GAME_FONT_MEDIUM)

		self._game_footer()


	def end_level_screen(self, player, level):
		self.__SCREEN.fill((0,0,0))
		self.__ui_screen = "end_level"
		self.__in_ui = True

		self._draw_text(message=conf.UiText.LEVEL_COMPLETE % level.name, y=-200)

		self._draw_text(message=conf.UiText.LEVEL_SCORE_TEXT, size=conf.UiText.GAME_FONT_SMALL)

		self._draw_text(message=conf.UiText.LEVEL_MOVES_TEXT % player.moves, size=conf.UiText.GAME_FONT_SMALL, y=50)
		self._draw_text(message=conf.UiText.LEVEL_DEATHS_TEXT % player.deaths, size=conf.UiText.GAME_FONT_SMALL, y=100)

		# next level
		self._draw_text(message=conf.UiText.GAME_CONT, size=conf.UiText.GAME_FONT_MEDIUM, y=150)



	def end_game_screen(self, player, victory=False):
		self.__SCREEN.fill((0,0,0))
		self.__ui_screen = "end_game" if victory else "defeat"
		self.__in_ui = True

		scores = player.get_best_scores()
		beat_levels = len(scores)

		self._draw_text(message=conf.UiText.get_victory_text(victory), y=-200)

		stats_end_game = conf.UiText.STATS_END_GAME % (
			beat_levels, player.moves, player.deaths)
		self._draw_text(message=stats_end_game, size=conf.UiText.GAME_FONT_MEDIUM, y=-150)

		for i in scores:
			score = conf.UiText.STATS_PER_LEVEL % (i+1, scores[i][0], scores[i][1])
			self._draw_text(message=score, size=conf.UiText.GAME_FONT_SMALL, y=i*18)

		# new game
		self._draw_text(message=conf.UiText.GAME_END, size=conf.UiText.GAME_FONT_MEDIUM, y=(len(scores)*18)+25)


	def overlay(self, player, level, elapsed):
		self.__in_ui = False
		self.__ui_screen = None
		_default_offset = -25

		if self.__show_overlay:
			# top-left
			self._draw_text(message=conf.UiText.OVERLAY_LEVEL_TEXT % (level.id+1, level.name),
				size=conf.UiText.OVERLAY_FONT_SIZE,
				x=-self.__ORIGIN[0]//2 + _default_offset,
				y=-self.__ORIGIN[1]//2 + _default_offset*4
			)
			# top-left below above
			self._draw_text(message=conf.UiText.get_overlay_player_best(level, player),
				size=conf.UiText.OVERLAY_FONT_SIZE,
				x=-self.__ORIGIN[0]//2 + _default_offset,
				y=-self.__ORIGIN[1]//2 + _default_offset*4 + 25
			)
			# bottom-left
			self._draw_text(message=conf.UiText.get_overlay_player_stats(player),
				size=conf.UiText.OVERLAY_FONT_SIZE,
				x=-self.__ORIGIN[0]//2 + _default_offset,
				y=self.__ORIGIN[1]//2 - _default_offset*4
			)
			# bottom-right
			self._draw_text(message=conf.UiText.OVERLAY_EXPIRED_TIME % elapsed,
				size=conf.UiText.OVERLAY_FONT_SIZE,
				x=self.__ORIGIN[0]//2 - _default_offset,
				y=self.__ORIGIN[1]//2 - _default_offset*4
			)

			self.__SCREEN.blit(self.__SCREEN, (0, 0))
			pygame.display.update()


	# utilities
	def _ui_key_listener(self):
		self.__show_overlay = True
		valid_event_keys = [pygame.K_SPACE, pygame.K_q, pygame.K_ESCAPE, pygame.K_l, pygame.K_m]
		retval = None

		while self.__show_overlay:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cleanup()
					pygame.quit()
					break

				if event.type == pygame.KEYDOWN:
					if event.key in valid_event_keys:
						self.__show_overlay = False
						retval = event.key
					else:
						continue
					break

			self.__CLOCK.tick(15)
		return retval

	def _handle_ui_pressed_key(self, screen, key):
		if key == pygame.K_SPACE:
			if screen in ["start", "end_level"]:
				pass
			elif screen in ["end_game", "defeat"]:
				self.cleanup()
				self.__NEW_GAME = True
		elif key in [pygame.K_q, pygame.K_ESCAPE]:
			self.cleanup()
			pygame.quit()
		else:
			pass

	def _text_objects(self, text, font):
		textSurface = font.render(text, True, (255,255,255))
		return textSurface, textSurface.get_rect()

	def _draw_text(self, message, x=0, y=0, size=conf.UiText.GAME_FONT_LARGE):
		font = self.__SYS.load_font(size)
		TextSurf, TextRect = self._text_objects(message, font)
		TextRect.center = self._get_offset_pos(x, y)
		self.__SCREEN.blit(TextSurf, TextRect)
		pygame.display.update()

	def _get_offset_pos(self, offset_x, offset_y):
		return (self.__ORIGIN[0] + offset_x, self.__ORIGIN[1] + offset_y)
