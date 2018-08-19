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
		self.__ON_UI = True

		# game title
		self._draw_text(
			message="PYRAMOS", pos=(self.__ORIGIN[0] + 50, self.__ORIGIN[1] - 150)
		)

		# new game
		self._draw_text(
			message="Press SPACEBAR to start a new game",
			size=25, pos=(self.__ORIGIN[0] + 25, self.__ORIGIN[1])
		)

		# other options
		self._draw_text(
			message="[S]ound on/off",
			size=20, pos=(self.__ORIGIN[0] - 100, self.__ORIGIN[1] + 150)
		)
		self._draw_text(
			message="[L]eaderboards",
			size=20, pos=(self.__ORIGIN[0] + 50, self.__ORIGIN[1] + 150)
		)
		self._draw_text(
			message="[Q]uit",
			size=20, pos=(self.__ORIGIN[0] + 200, self.__ORIGIN[1] + 150)
		)

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

			self.__CLOCK.tick(15)

	def end_level_screen(self):
		self.__ON_UI = True
		while self.__ON_UI:
			self.__CLOCK.tick(15)

	def end_game_screen(self):
		self.__ON_UI = True
		while self.__ON_UI:
			self.__CLOCK.tick(15)

	def overlay(self):
		pass

	# utilities
	def _text_objects(self, text, font):
		textSurface = font.render(text, True, (255,255,255))
		return textSurface, textSurface.get_rect()

	def _draw_text(self, message, pos, size=conf.FONT_SIZE):
		font = self.__SYS.load_font(size)
		TextSurf, TextRect = self._text_objects(message, font)
		TextRect.center = pos
		self.__SCREEN.blit(TextSurf, TextRect)
		pygame.display.update()
