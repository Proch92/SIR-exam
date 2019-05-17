import random
import numpy as np
import utils
import dill


EXPLORATION = 0.3
MIN_EXPLORATION = 0.1
EXPLORATION_DEC = 0.00001
QUANTA = 200
GAMMA = 0.8


class Markov_QL(object):
    """docstring for Markov_QL"""

    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space

        q_shape = [QUANTA for _ in range(observation_space.shape[0])]
        q_shape.append(action_space.n)

        self.q = np.random.rand(*q_shape)
        print('q matrix shape: {}'.format(self.q.shape))

        self.exploration_p = EXPLORATION

    def action(self, state, train=True):
        if train and (random.random() < self.exploration_p):
            return self.action_space.sample()

        self.exploration_p -= EXPLORATION_DEC
        if self.exploration_p < MIN_EXPLORATION:
            self.exploration_p = MIN_EXPLORATION

        discrete = utils.discretize(state, self.observation_space, QUANTA)
        return np.argmax(self.q[tuple(discrete)])

    def reward(self, state, action, reward, new_state):
        state = utils.discretize(state, self.observation_space, QUANTA)
        new_state = utils.discretize(new_state, self.observation_space, QUANTA)

        self.q[tuple(state)][action] = reward + GAMMA * max(self.q[tuple(new_state)])

    def save(self, filename):
        with open(filename, 'wb') as f:
            dill.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return dill.load(f)
