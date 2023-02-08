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
        self.model = None
        self.trainer = None

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
        self.memory.append((state, action, reward, next_state, game_over)) #popleft when MAX_MEMORY # ONE Tuple
    def train_long_memory(self):
        #replay all the moves done on the short memory and try different move each step
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, games_over = zip(*mini_sample) 
        #zip assemble every element of all the memory by their order:
        #[(state1, action1, reward1, next_state1, game_over1), (state2, action2, reward2, next_state2, game_over2), ...]
        self.trainer.train_step(states, actions, rewards, next_states, games_over)
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    def get_action(self, state):
        #trade of between exploration / explotation
        # use some randomness in the first moves and gradually remove it
        self.epsilon = 80 - self.nb_game #epsilon is the indicator of randomness, here 80 games is hardcoded
        final_move = [0,0,0] #one of the 0 has to be true
        if random.randint(0, 200) < self.epsilon: #there is a small chance that a random move is selected, as the epsilon gets smaller, the chance get smaller too
            move = random.randint(0,2)
            final_move[move] = 1 #this means that one of the 0's in final_move shall become a 1. it is define by move = random.randint(0,2)
        else: #in this case, we are not using a random move but a move based on the AI "reflexion"
            state0= torch.tensor(state, dtype = torch.float) #creat a tensor state0 for pytorch to use
            prediction = self.model.predict(state0) #the AI process the tensor and give a prediction based on experience
            move = torch.argmax(prediction).item() # move = index of the maximum value (in this case, a 1)
            final_move[move] = 1
        return final_move

            

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
                agent.model.save()
            print('Game n°', agent.nb_game, 'Score: ', score, 'Best score: ', best_score)
            #plot

if __name__ == '__main__':
    train()
