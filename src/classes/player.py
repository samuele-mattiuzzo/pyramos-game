# -*- coding: utf-8 -*-


class Player:

	def __init__(self):
		self.__name = 'Player'
		self.__pos = (0, 0)
		self.__moves = 0
		self.__deaths = 0
		self.__best = {}

	def new_start(self, pos):
		self.__pos = pos

	def update_pos(self, np):
		self.__pos = np
		self.add_move()

	def add_move(self):
		self.__moves += 1

	def add_death(self):
		self.__deaths += 1

	def update_best_score(self, id, name, new_score):
		write_score = (name, new_score)

		if self.__best.get(id, None):
			write_score = (self.__best[id][0],
				new_score if new_score < self.__best[id][1] else self.__best[id][1]
			)

		self.__best.update({
			id: (name, new_score)
		})

	def get_best_scores(self):
		return self.__best

	# getters
	@property
	def name(self):
		return self.__name

	@property
	def pos(self):
		return self.__pos

	@property
	def moves(self):
		return self.__moves

	@property
	def deaths(self):
		return self.__deaths
