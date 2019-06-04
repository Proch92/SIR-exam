import random


class Replay_buffer(object):
    """docstring for Replay_buffer"""

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.reset()

    def add(self, experience):
        self.idx = (self.idx + 1) % self.buffer_size
        self.filled = min(self.filled + 1, self.buffer_size)

        self.replays[self.idx] = experience

    def sample(self, quantity):
        return random.sample(self.replays, quantity)

    def reset(self):
        self.idx = 0
        self.filled = 0
        self.replays = [None] * self.buffer_size
