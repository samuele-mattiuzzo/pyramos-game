from main_game import square
from resources.levels import *
from resources.config import *

class Level:

	def __init__(self, id):
		self.name = LEVELS[id]['name']
		self.design = LEVELS[id]['design']
		self.start = LEVELS[id]['start']
		self.end = LEVELS[id]['end']
		self.music = LEVELS[id]['background_music']
		self.completion = LEVELS[id]['top_score']

		
		

