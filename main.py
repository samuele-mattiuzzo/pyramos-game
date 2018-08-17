try:

	# pygame + general imports
	import pygame, sys,os
	from pygame.locals import *

	# resource imports
	from resources.config import *
	from resources.levels import *

	# main game classes imports
    from main_game.game import *
	from main_game.level import *
	from main_game.player import *
	from main_game.square import *
	from main_game.gui import *
	from main_game.system import *

except ImportError as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)

## GLOBAL VARIABLES

# pygame init and screen global variable
pygame.init()
game_sys = System()
game_sys.get_properties()
screen = game_sys.get_screen()

# tiles preloading
WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE = game_sys.load_images()
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = game_sys.get_images_properties()

# level preconfiguration
LEVEL_ID = 0 # beginning of the game
game = Game(
    level_id=LEVEL_ID
    levels=LEVELS
)

GAME_AREA = pygame.Surface(screen.get_size())

UNCOVERED = {
	#"dir":	 x,y
	"top" : 	(),
	"right" : 	(),
	"bottom" : 	(),
	"left" : 	(),
}

# gui elements preloading (NotYetImplemented)
# LEVEL_NAME, LEVEL_TOP_SCORE, LEVEL ID+1, GAME_MODE, PLAYER_MOVES, PLAYER_DEATHS, PLAYER_TOP

# graphics creation
g = Graphics(TILE_HEIGHT, TILE_WIDTH, WALL_SPRITE, PLAYER_SPRITE, WALK_SPRITE, START_SPRITE, END_SPRITE)

def next_level():
	g.display_game(screen, GAME_AREA, game.level, game.player, UNCOVERED)
	screen.blit(GAME_AREA, (0, 0))
	pygame.display.flip()


# checks for the new player move and returns the new position. false if it's not (player dies!)
def new_valid_pos(player_pos, keyName, lmap):
	valid = False
	is_dead = False
	pos = player_pos

	if keyName == pygame.K_LEFT and player_pos[1]>0:
		if lmap[player_pos[0]][player_pos[1]-1] != 0:
			pos = (pos[0], pos[1]-1)
			valid = True
		else:
			is_dead = True

	if keyName == pygame.K_RIGHT and player_pos[1]<9:
		if lmap[player_pos[0]][player_pos[1]+1] != 0:
			pos = (pos[0], pos[1]+1)
			valid = True
		else:
			is_dead = True

	if keyName == pygame.K_UP and player_pos[0]>0:
		if lmap[player_pos[0]-1][player_pos[1]] != 0:
			pos = (pos[0]-1, pos[1])
			valid = True
		else:
			is_dead = True

	if keyName == pygame.K_DOWN and player_pos[0]<9:
		if lmap[player_pos[0]+1][player_pos[1]] != 0:
			pos = (pos[0]+1, pos[1])
			valid = True
		else:
			is_dead = True

	return valid, is_dead, pos



def main():
	#time is specified in milliseconds
	#fixed simulation step duration
	step_size = 500
	#max duration to render a frame
	max_frame_time = 100
	now = pygame.time.get_ticks()

	# first draw
	game.next_level()

	__cycle = True
	valid = is_dead = False
	tmp_pos = PLAYER.pos
	pressed = ""

	while(__cycle):
		#handle events

		for event in pygame.event.get():
			if event.type == QUIT:
				print("Bye!")
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				else:
					valid, is_dead, tmp_pos = new_valid_pos(
                        game.player.pos,
                        event.key,
                        game.level.design
                    )

		if is_dead:
			print("You touched a poisonous wall! You are dead!")
			print("Your score is: %s" % str(game.player.moves))
			print("Bye!")
			sys.exit()

		else:
			if valid:
				# actually moves the player
				valid = False
				g.update_game(
                    screen, GAME_AREA,
                    game.player, game.level,
                    tmp_pos, UNCOVERED
                )

                # reset - uncover
				screen.blit(GAME_AREA, (0, 0))
				pygame.display.flip()

				if game._check_end():
					global LEVEL_ID
					game.player.update_best_score(
                        game.level_id,
                        game.level["name"],
                        game.player.moves
                    )
                    if game._check_has_more_levels()
                        game.next_level()
					else:
						print("YOU WON!")
						print("You completed %s stages with a total of %s steps" % (str(game.level_id), str(game.player.moves)))
						print("\nScores:")
						scores = game.player.get_best_scores()
						for i in scores:
							print("%s: %s - %s steps" % (str(i), str(scores[i][0]), str(scores[i][1])))
						__cycle = False

		#get the current real time
		T = pygame.time.get_ticks()

		#if elapsed time since last frame is too long...
		if T-now > max_frame_time:
			#slow the game down by resetting clock
			now = T - step_size
			#alternatively, do nothing and frames will auto-skip, which
			#may cause the engine to never render!

		#this code will run only when enough time has passed, and will
		#catch up to wall time if needed.
		while(T-now >= step_size):
			#save old game state, update new game state based on step_size
			now += step_size
		else:
			pygame.time.wait(10)

		#render game state. use 1.0/(step_size/(T-now)) for interpolation

if __name__ == "__main__":
	main()
