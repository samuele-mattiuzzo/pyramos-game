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
		self.__ORIGIN = self.__SYS.get_screen_origin()

		self.__ON_UI = False
		self.__CLOCK = pygame.time.Clock()

	def start_screen(self):
		self.__SCREEN.fill((0,0,0))

		# game title
		self._draw_text(message="PYRAMOS",
			pos=(self.__ORIGIN[0] + 50, self.__ORIGIN[1] - 150))

		# new game
		self._draw_text(message="Press SPACEBAR to start a new game",
			size=25, pos=(self.__ORIGIN[0] + 25, self.__ORIGIN[1]))

		# other options
		self._draw_text(message="[S]ound on/off",
			size=18, pos=(self.__ORIGIN[0] - 100, self.__ORIGIN[1] + 150))
		self._draw_text(message="[L]eaderboards",
			size=18, pos=(self.__ORIGIN[0] + 50, self.__ORIGIN[1] + 150))
		self._draw_text(message="[Q]uit",
			size=18, pos=(self.__ORIGIN[0] + 200, self.__ORIGIN[1] + 150))

		self._ui_key_listener()


	def end_level_screen(self, player, level):
		self.__SCREEN.fill((0,0,0))

		level_title = "%s completed" % level.name
		self._draw_text(message=level_title,
			pos=(self.__ORIGIN[0] - len(level_title)//2, self.__ORIGIN[1] - 150))

		score_header = "Score"
		self._draw_text(message=score_header,
			size=18, pos=(self.__ORIGIN[0] - len(score_header)//2, self.__ORIGIN[1]))

		moves_text = "Moves: %s" % player.moves
		deaths_text = "Deaths: %s" % player.deaths
		self._draw_text(message=moves_text,
			size=18, pos=(self.__ORIGIN[0] - len(moves_text)//2, self.__ORIGIN[1] + 50))

		self._draw_text(message=deaths_text,
			size=18, pos=(self.__ORIGIN[0] - len(moves_text)//2, self.__ORIGIN[1] + 100))

		# new game
		spacebar = "Press SPACEBAR to continue"
		self._draw_text(message=spacebar,
			size=25, pos=(self.__ORIGIN[0] - len(spacebar)//2, self.__ORIGIN[1] + 150))

		self._ui_key_listener()

	def end_game_screen(self, player, victory=False):
		self.__SCREEN.fill((0,0,0))

		scores = player.get_best_scores()
		beat_levels = len(scores)

		final_message = "YOU BEAT THE GAME" if victory else "YOU WERE DEFEATED"
		self._draw_text(message=final_message,
			pos=(self.__ORIGIN[0] - len(final_message)//2, self.__ORIGIN[1] - 150))

		completion_message = "You completed %s stages totalling %s moves and %s deaths" % (
			beat_levels, player.moves, player.deaths)
		self._draw_text(message=completion_message,
			size=25, pos=(self.__ORIGIN[0] - len(completion_message)//2, self.__ORIGIN[1] - 125))

		for i in scores:
			score = "%s: %s - %s steps" % (str(i), str(scores[i][0]), str(scores[i][1]))
			self._draw_text(message=score,
				size=18, pos=(self.__ORIGIN[0] - len(score)//2, self.__ORIGIN[1] + i*18))

		# new game
		self._draw_text(message="Press SPACEBAR to continue",
			size=25, pos=(self.__ORIGIN[0] + 25, self.__ORIGIN[1] + (len(scores)*18)+25))

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

	def _draw_text(self, message, pos, size=conf.FONT_SIZE):
		font = self.__SYS.load_font(size)
		TextSurf, TextRect = self._text_objects(message, font)
		TextRect.center = pos
		self.__SCREEN.blit(TextSurf, TextRect)
		pygame.display.update()
