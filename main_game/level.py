# -*- coding: utf-8 -*-
from resources.levels import *


class Level:

	def __init__(self, id):
		self.id = LEVELS[id]['id']
		self.name = LEVELS[id]['name']
		self.design = LEVELS[id]['design']
		self.start = LEVELS[id]['start']
		self.end = LEVELS[id]['end']
		self.music = LEVELS[id]['background_music']
		self.completion = LEVELS[id]['top_score']
