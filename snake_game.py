import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame
import random
from header import SnakeBoard

pygame.init()
if __name__ == '__main__':
	game = SnakeBoard()
	#game loop
	while True:
		game.play_step()
	
	#break when game_over
	

	pygame.quit()