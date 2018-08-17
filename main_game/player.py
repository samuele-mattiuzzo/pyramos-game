from main_game import square
from resources.levels import *
from resources.config import *

class Player:

	def __init__(self):
		self.name = 'Player'
		self.pos = (0,0)
		self.moves = 0
		self.deaths = 0
		self.best = {}

	def new_start(self, pos):
		self.pos = pos

	def update_pos(self, np):
		self.pos = np
		self.add_move()

	def add_move(self):
		self.moves += 1

	def add_death(self):
		self.deaths += 1

	def update_best_score(self, id, name, new_score):
		if self.best.has_key(id):
			if new_score < self.best[id]:
				self.best[id][1] = new_score
		else:
			self.best[id] = (name, new_score)

	def get_best_scores(self):
		return self.best
