import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.nb_game = 0
        self.epsilon = 0    #randomness
        self.gamma = 0      #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #erase from the begining when too much memory
        #TODO: model, trainer

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)
        
    def remember(self, state, action, reward, next_state, game_over):
        pass
    def train_long_memory(self):
        #replay all the moves done on the short memory and try different move each step
        pass
    def train_short_memory(self, state, action, reward, next_state, game_over):
        pass
    def get_action(self, state):
        pass

def train():
    plot_score = []
    mean_score = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while(True):
        #get old state
        old_state = agent.get_state(game)

        # move based of state
        final_move = agent.get_action(old_state)

        #performe move and get new state
        reward, game_over, score = game.play_step(final_move)
        new_state = agent.get_state(game)

        #train short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, game_over)
        agent.remember(old_state, final_move, reward, new_state, game_over)

        if game_over:
            #train long memory and plot result
            game.reset()
            agent.nb_game += 1
            agent.train_long_memory()
            if score > best_score:
                best_score = score
                #agent.model.save()
            print('Game n°', agent.nb_game, 'Score: ', score, 'Best score: ', best_score)
            #plot

if __name__ == '__main__':
    train()
