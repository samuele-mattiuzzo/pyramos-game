# -*- coding: utf-8 -*-


# game config
class UiText:
	GAME_TITLE = "Pyramos"
	COPY_TEXT = "samumatt@gmail.com | &copy; 2018"

	GAME_NEW = "Press SPACEBAR to start a new game"
	GAME_CONT = "Press SPACEBAR to continue..."
	GAME_END = "Press SPACEBAR to return to main menu"
	GAME_OPTIONS = "[H]elp	[S]ound on/off	[L]eaderboards	[Q]uit"

	SUBMENU_HELP_TITLE = "[H]ELP"
	SUBMENU_LEADERBOARD_TITLE = "[L]EADERBOARD"
	SUBMENU_HELP_TEXT = """
		Press the arrow keys
		Don't hit the walls
		Don't die
	"""
	SUBMENU_PLACEHOLDER = "Coming Soon"
	SUBMENU_BACK = "<- [B]ack to main menu"

	GAME_FONT_LARGE = 50
	GAME_FONT_MEDIUM = 25
	GAME_FONT_SMALL = 18

	STATS_END_GAME = "You completed %s stages totalling %s moves and %s deaths"
	STATS_PER_LEVEL = "%s: %s - %s steps"

	LEVEL_COMPLETE = "%s completed"
	LEVEL_SCORE_TEXT = "Score"
	LEVEL_MOVES_TEXT = "Moves: %s"
	LEVEL_DEATHS_TEXT = "Deaths: %s"

	OVERLAY_LEVEL_TEXT = "Level %s - %s"
	OVERLAY_PLAYER_STATS = "Moves: %s | Lives: %s"
	OVERLAY_EXPIRED_TIME = "Time: %s"
	OVERLAY_FONT_SIZE = 20

	@staticmethod
	def get_victory_text(victory=False):
		return "YOU BEAT THE GAME" if victory else "YOU WERE DEFEATED"

	@staticmethod
	def get_overlay_player_best(level, player):
		score = player.get_best_scores().get(level.id, None)
		res = "None" if not score else "%s m | %s d" % (score[0], score[1])

		return "Best: %s" % res

	@classmethod
	def get_overlay_player_stats(cls, player):
		lives_deaths = "".join(["[x]" for i in range(player.lives - player.deaths)])
		lives_deaths += "".join(["[ ]" for i in range(player.deaths)])

		return cls.OVERLAY_PLAYER_STATS % (player.moves, lives_deaths)

# window size
WINDOW_SIZE = (600, 600)

# size of each tile
TILE_SIZE = TILE_HEIGHT, TILE_WIDTH = (96, 96)

# font name
FONT_NAME = "VT323-Regular.ttf"

# folders
RESOURCES_FOLDER = "resources"
TILE_FOLDER = "tilesets"
FONT_FOLDER = "fonts"
ICON_PATH = '%s/game_icon.png' % RESOURCES_FOLDER
