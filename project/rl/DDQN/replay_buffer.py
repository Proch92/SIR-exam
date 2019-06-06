import random
import numpy as np


class Replay_buffer(object):
    """docstring for Replay_buffer"""

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.reset()

    def add(self, experience):
        self.idx = (self.idx + 1) % self.buffer_size

        if self.filled < self.buffer_size:
            self.replays.append(experience)
        else:
            self.replays[self.idx] = experience

        self.filled = min(self.filled + 1, self.buffer_size)

    def sample(self, quantity):
        samples = random.sample(self.replays, min(quantity, self.filled))

        (s0, _, _, _, _) = samples[0]

        batch_states = np.empty([0, s0.shape[1]])
        batch_actions = []
        batch_s_t1 = np.empty([0, s0.shape[1]])
        batch_rewards = []
        batch_final = []

        for (s, a, r, s_t1, final) in samples:
            batch_states = np.append(batch_states, s, axis=0)
            batch_actions.append(a)
            batch_s_t1 = np.append(batch_s_t1, s_t1, axis=0)
            batch_rewards.append(r)
            batch_final.append(final)

        return (batch_states, batch_actions, batch_s_t1, batch_rewards, batch_final)

    def reset(self):
        self.idx = -1
        self.filled = 0
        self.replays = []
