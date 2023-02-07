


import random
from Header import SnakeBoard
from enum import Enum
from collections import namedtuple

from pygame.locals import *
import pygame
pygame.init()
pygame.display.list_modes()

if __name__ == '__main__':
	game = SnakeBoard()
	#game loop
	while True:
		game_over, score = game.play_step()

		if game_over == True:
				break
	print('Final score: ', score)
	#break when game_over
	

	pygame.quit()
	exit()
