# -*- coding: utf-8 -*-
try:
	import pygame
	from pygame.locals import *

	from src import config as conf
	from src.system import System

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class GameUi:

	def __init__(self):
		self.__SYS = System()

		self.on_init()

	def on_init(self):
		self.__SYS.get_properties()

		self.__SCREEN = self.__SYS.get_screen()
		self.__GAME_AREA = pygame.Surface(self.__SCREEN.get_size())
		#self.__FONT = pygame.font.Font('freesansbold.ttf',115)
		self.__ORIGIN = self.__SYS.get_screen_origin_no_offset()

		self.__ON_UI = False
		self.__CLOCK = pygame.time.Clock()

	def start_screen(self):
		self.__SCREEN.fill((0,0,0))

		# game title
		game_title = "PYRAMOS"
		self._draw_text(message=game_title, y=-150)

		# new game
		spacebar = "Press SPACEBAR to start a new game"
		self._draw_text(message=spacebar, size=25)

		# other options
		sound_text = "[S]ound on/off"
		leaderboard_text = "[L]eaderboards"
		quit_text = "[Q]uit"

		options_text = sound_text + leaderboard_text + quit_text
		self._draw_text(message=options_text, size=18, y=100)

		copy_text = "samumatt@gmail.com | &copy; 2018"
		self._draw_text(message=copy_text, size=18, y=200)

		self._ui_key_listener()


	def end_level_screen(self, player, level):
		self.__SCREEN.fill((0,0,0))

		level_title = "%s completed" % level.name
		self._draw_text(message=level_title, y=-150)

		score_header = "Score"
		self._draw_text(message=score_header, size=18)

		moves_text = "Moves: %s" % player.moves
		deaths_text = "Deaths: %s" % player.deaths
		self._draw_text(message=moves_text, size=18, y=50)
		self._draw_text(message=deaths_text, size=18, y=100)

		# new game
		spacebar = "Press SPACEBAR to continue..."
		self._draw_text(message=spacebar, size=25, y=150)

		self._ui_key_listener()

	def end_game_screen(self, player, victory=False):
		self.__SCREEN.fill((0,0,0))

		scores = player.get_best_scores()
		beat_levels = len(scores)

		final_message = "YOU BEAT THE GAME" if victory else "YOU WERE DEFEATED"
		self._draw_text(message=final_message, y=-150)

		completion_message = "You completed %s stages totalling %s moves and %s deaths" % (
			beat_levels, player.moves, player.deaths)
		self._draw_text(message=completion_message, size=25, y=-125)

		for i in scores:
			score = "%s: %s - %s steps" % (str(i), str(scores[i][0]), str(scores[i][1]))
			self._draw_text(message=score, size=18, y=i*18)

		# new game
		spacebar = "Press SPACEBAR return to main menu"
		self._draw_text(message=spacebar, size=25, y=(len(scores)*18)+25)

		self._ui_key_listener()

	def overlay(self):
		pass

	# utilities
	def _ui_key_listener(self):
		self.__ON_UI = True
		while self.__ON_UI:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.__ON_UI = False
					if event.key in [pygame.K_q, pygame.K_ESCAPE]:
						self.__ON_UI = False
						pygame.quit()
					if event.key == pygame.K_l:
						self.__ON_UI = False
					if event.key == pygame.K_m:
						self.__ON_UI = False

			self.__CLOCK.tick(15)


	def _text_objects(self, text, font):
		textSurface = font.render(text, True, (255,255,255))
		return textSurface, textSurface.get_rect()

	def _draw_text(self, message, x=0, y=0, size=conf.FONT_SIZE):
		font = self.__SYS.load_font(size)
		TextSurf, TextRect = self._text_objects(message, font)
		TextRect.center = self._get_offset_pos(x, y)
		self.__SCREEN.blit(TextSurf, TextRect)
		pygame.display.update()

	def _get_offset_pos(self, offset_x, offset_y):
		return (self.__ORIGIN[0] + offset_x, self.__ORIGIN[1] + offset_y)
