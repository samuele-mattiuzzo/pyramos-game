# -*- coding: utf-8 -*-
try:
	# pygame + general imports
	import pygame, sys, os
	from pygame.locals import *

	# main game classes imports
	from src.game import Game

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)


# pygame init
pygame.init()


if __name__ == "__main__":
	game = Game()
	game.new_game()
