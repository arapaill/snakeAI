


import random
from enum import Enum
from collections import namedtuple

from pygame.locals import *
import pygame
pygame.init()
pygame.display.list_modes()


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
		self.snake = [self.head, 
                      	Point(self.head.x-BLOCK_SIZE, self.head.y),
                      	Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
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
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.direction = Direction.LEFT
				elif event.key == pygame.K_RIGHT:
					self.direction = Direction.RIGHT
				elif event.key == pygame.K_UP:
					self.direction = Direction.UP
				elif event.key == pygame.K_DOWN:
					self.direction = Direction.DOWN
		# move
		self._move(self.direction) #update the head
		self.snake.insert(0, self.head)
		#check result of the move
		game_over = False
		if self._is_collision():
			game_over = True
			return(game_over, self.score)
		# place new food or not

		#if there is no food then we remove the last snake chain since we just added one
		# if there is food, no need to do anything
		if self.head == self.food:
			self.score += 1
			self._place_food()
		else:
			self.snake.pop()
		#update UI and Clock
		self._updateUI()
		self.clock.tick(SPEED)
		# return game_over and score
		
		return(game_over, self.score)

	def	_is_collision(self):
		# hits boudary
		if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.h < 0:
			return True
		# hits body
		if self.head in self.snake[1:]: #exclude the head in the check
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
	def _move(self, direction):
		x = self.head.x
		y = self.head.y
		if direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif direction == Direction.UP:
			y -= BLOCK_SIZE
		elif direction == Direction.DOWN:
			y += BLOCK_SIZE
		self.buff= Point(x, y)


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
