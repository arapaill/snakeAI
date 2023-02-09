


import random
from enum import Enum
from collections import namedtuple
import pygame
import numpy as np


pygame.init()
pygame.display.list_modes()

#Todo:
#reset function that reopen a game after a defeat
# reward systeme for the AI
# play(action) - > direction
# game_iteration : keeps track of all the games

#to help having better direction in the code
class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4


Point = namedtuple('Point', ['x', 'y'])
font = pygame.font.Font('games/Games.ttf', 25)

#size of a block = 20 pixels
BLOCK_SIZE = 20
SPEED =20 

#RGB color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 100, 255)
BLUE2 = (0, 0, 255)
BLACK = (0, 0, 0)
#this class represent the whole board, snake too
class SnakeGameAI:
	def __init__(self, w=640, h=480):
		self.w = w
		self.h = h

		#init display
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Snake: The Game')
		self.clock = pygame.time.Clock()
		self.reset()

	def reset(self):
		#init game state
		self.direction = Direction.RIGHT
		#where the head of the snake is at the start
		self.head = Point(self.w/2, self.h/2)
		# size of the snake at the start
		self.snake = [self.head, 
                      	Point(self.head.x-BLOCK_SIZE, self.head.y),
                      	Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
		self.score = 0
		self.food = None
		self._place_food()
		self.frame_iterations = 0

		#randomly put food on the board when called
	def _place_food(self):
		x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		self.food = Point(x, y)
		#if the food is in the snake, we try again
		if self.food in self.snake:
			self._place_food()

	#
	def play_step(self, action):
		# collect user inupt
		self.frame_iterations += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		# move
		self._move(action) #update the head
		self.snake.insert(0, self.head)

		#check result of the move
		reward = 0
		game_over = False
		if self.is_collision() or self.frame_iterations > 100 * len(self.snake): #if the snake touch border or if too much time passes without anything happening
			game_over = True
			reward = -10
			return(reward, game_over, self.score)
		# place new food or not

		#if there is no food then we remove the last snake chain since we just added one
		# if there is food, no need to do anything
		if self.head == self.food:
			reward = 10
			self.score += 1
			self._place_food()
		else:
			self.snake.pop()
		#update UI and Clock
		self._updateUI()
		self.clock.tick(SPEED)
		# return game_over and score
		
		return(reward, game_over, self.score)

	def	is_collision(self, pt=None):

		if pt == None:
			pt = self.head
		# hits boudary
		if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or self.h < 0:
			return True
		# hits body
		if pt in self.snake[1:]: #exclude the head in the check
			return True
		return False

	def _updateUI(self):
		self.display.fill(BLACK)
		for pt in self.snake:
			pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
			pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
		
		pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

		text = font.render("Score: " + str(self.score), True, WHITE)
		self.display.blit(text, [0,0])
		pygame.display.flip()
	def _move(self, action):
		#depending on the curent direction,
		#[1,0,0] = straight
		#[0,1,0] = turn right
		#[0,0,1] = turn left
		clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
		idx = clock_wise.index(self.direction)

		if np.array_equal(action, [1, 0, 0]):
			new_dir = clock_wise[idx] #no change
		elif np.array_equal(action, [0, 1, 0]):
			next_idx = (idx + 1) %4 #goes back at the begining if head was up
			new_dir = clock_wise[next_idx] #turn right
		else: #[0, 0, 1]
			next_idx = (idx + 1) %4 #goes back at the end if head was up
			new_dir = clock_wise[next_idx] #turn left
		self.direction = new_dir
		x = self.head.x
		y = self.head.y
		if self.direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif self.direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif self.direction == Direction.UP:
			y -= BLOCK_SIZE
		elif self.direction == Direction.DOWN:
			y += BLOCK_SIZE
		self.head = Point(x, y)
