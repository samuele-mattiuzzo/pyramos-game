# -*- coding: utf-8 -*-
try:
	import os
	import pygame
	from resources import config as conf
	from pygame.locals import *
except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


class System:
	'''
		Class for handling:
		- [X] screen init based on parameters
		- [ ] load mode
		- [ ] save/load game
		- [ ] game config
		- [ ] credits
	'''
	def __init__(self):
		self.__res = self.__window_width, self.__window_height = conf.WINDOW_SIZE
		self.__tile_size = self.__tile_width, self.__tile_height = conf.TILE_SIZE
		self.__mode = "classic"

	@property
	def res(self):
		return self.__res

	@property
	def tile_size(self):
		return self.__tile_size

	def get_properties(self):
		'''
			Gets system propeties
			NotYetImplemented: may be done in __init__()?
		'''
		video = pygame.display.Info()

	def get_screen(self):
		'''
			Creates and returns a new screen
		'''
		return pygame.display.set_mode(
			self.__res)

	def get_screen_origin(self):
		return (
			(self.__window_width//2) - (self.__tile_width//2),
			(self.__window_height//2) - (self.__tile_height//2),
		)

	def load_mode(self, mode):
		'''
			Used to change mode (other than default for "classic")
			NotYetImplemented
		'''
		self.__mode = mode

	def load_images(self):
		'''
			Preloads all the images based on mod selected
			@returns all the images, scaled based on the system configuration
		'''

		wa_spr = self.load_png("tile_wall.png")
		p_spr = self.load_png("tile_player.png")
		wlk_spr = self.load_png("tile_walk.png")
		s_spr = self.load_png("tile_start.png")
		e_spr = self.load_png("tile_end.png")

		return wa_spr, p_spr, wlk_spr, s_spr, e_spr

	## utilities functions
	def load_png(self, name):
		"""
			Load image and return image object
			(utility, slightly modified, from http://www.pygame.org/docs/tut/tom/games3.html - 3.2)
		"""
		fullname = os.sep.join([os.getcwd(), "resources", "imgs", self.__mode, name])
		try:
			image = pygame.image.load(fullname)
			if image.get_alpha() is None:
				image = image.convert()
			else:
				image = image.convert_alpha()

		except pygame.error as message:
				print('Cannot load image: %s' % fullname)
				print(message)
				raise SystemExit

		return pygame.transform.scale(image, (self.__tile_width, self.__tile_height))
