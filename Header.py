import pygame
from enum import Enum

class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4

class SnakeBoard:
	def __init__(self, w=640, h=480):
		self.w = w
		self.h = h

		#init display
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Snake: The Game')
		self.clock = pygame.time.Clock()

		#init game state
		self.direction = ""
	def play_step(self):
		pass