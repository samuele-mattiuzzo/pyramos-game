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

	def addDeath(self):
		self.deaths += 1

	def updateBestScore(self, id, name, new_score):
		if self.best.has_key(id):
			if new_score < self.best[id]:
				self.best[id][1] = new_score
		else:
			self.best[id] = (name, new_score)

	def getBestScores(self):
		return self.best