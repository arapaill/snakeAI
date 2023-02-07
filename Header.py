import pygame
import random
from enum import Enum
from collections import namedtuple

#to help having better direction in the code
class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4


Point = namedtuple('Point', ['x', 'y'])

#size of a block = 20 pixels
BLOCK_SIZE = 20

#this class represent the whole board, snake too
class SnakeBoard:
	def __init__(self, w=640, h=480):
		self.w = w
		self.h = h

		#init display
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Snake: The Game')
		self.clock = pygame.time.Clock()

		#init game state
		self.direction = Direction.RIGHT
		#where the head of the snake is at the start
		self.head = Point(self.w/2, self.h/2)
		# size of the snake at the start
		self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
						Point(self.head.x-(2+BLOCK_SIZE), self.head.y)]
		self.score = 0
		self.food = None
		self._place_food()

		#randomly put food on the board when called
	def _place_food(self):
		x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		self.food = Point(x, y)
		#if the food is in the snake, we try again
		if self.food in self.snake:
			self._place_food()

	#
	def play_step(self):
		# collect user inupt

		# move

		#check result of the move

		# place new food or not

		#update UI and Clock

		# return game_over and score
		game_over = False
		return(game_over, self.score)
