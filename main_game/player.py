from main_game import square
from resources.levels import *
from resources.config import *

class Player:

	def __init__(self):
		self.name = 'King Tut'
		self.pos = (0,0)
		self.moves = 0
		self.deaths = 0
		self.best = {}

	def newStart(self, pos):
		self.pos = pos

	def updatePos(self, np):
		self.pos = np
		self.addMove()

	def addMove(self):
		self.moves += 1

	def resetMoves(self):
		self.moves = 0

	def addDeath(self):
		self.deaths += 1

	def resetDeaths(self):
		self.deaths = 0

	def updateBestScore(self, id, new_score):
		self.best[id] = new_score