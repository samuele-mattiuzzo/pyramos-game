try:
	import os
	import pygame
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
		self.res = (800,600)
		self.surface_size = (320,320)
		self.tile_size = self.tile_x, self.tile_y = (32,32)
		self.mode = "classic"

	def get_properties(self):
		'''
			Gets system propeties
			NotYetImplemented: may be done in __init__()?
		'''
		video = pygame.display.Info()
		self.res = (video.current_w//2, video.current_h//2)
		self.surface_size = (self.res[1], self.res[1])
		self.tile_size = self.tile_x, self.tile_y = (int(self.res[1]/10), int(self.res[1]/10))

	def get_screen(self):
		'''
			Creates and returns a new screen
		'''
		return pygame.display.set_mode(self.res)

	def load_mode(self, mode):
		'''
			Used to change mode (other than default for "classic")
			NotYetImplemented
		'''
		self.mode = mode

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

	def get_images_properties(self):
		'''
			X, Y size of the tiles
		'''
		return self.tile_x, self.tile_y

	## utilities functions
	def load_png(self, name):
		"""
			Load image and return image object
			(utility, slightly modified, from http://www.pygame.org/docs/tut/tom/games3.html - 3.2)
		"""
		fullname = os.sep.join([os.getcwd(), "resources", "imgs", self.mode, name])
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

		return pygame.transform.scale(image, (self.tile_x, self.tile_y))
