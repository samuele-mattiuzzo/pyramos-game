try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)


class Square:
	'''
		Main class for handling Square
	'''
	pass