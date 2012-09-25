from main_game import square

class Level:

	def __init__(self, settings):
		self.name = settings['name']
		self.tiles = settings['design']
		self.completion = settings['top_score']

	def renderTiles(self):
		pass
		

