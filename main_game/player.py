from main_game import square
from resources.levels import *
from resources.config import *

class Player:

	def __init__(self, start_pos):
		self.name = 'King Tut'
		self.pos = start_pos

	def updatePos(self, np):
		self.pos = np