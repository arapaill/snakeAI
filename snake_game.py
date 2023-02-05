import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import random
from Header import SnakeBoard

pygame.init()
pygame.display.list_modes()
if __name__ == '__main__':
	game = SnakeBoard()
	#game loop
	while True:
		game.play_step()
	
	#break when game_over
	

	pygame.quit()