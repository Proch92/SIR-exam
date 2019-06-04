import gym
from ddqn import DDQN
import numpy as np
import sys
from replay_buffer import Replay_buffer

GYM = "CartPole-v0"


def main():
    if len(sys.argv) != 2:
        print('usage: python ' + sys.argv[0] + ' epochs')
        exit(0)

    epochs = int(sys.argv[1])

    env = gym.make(GYM)
    input_shape = env.observation_space.shape[0]
    output_shape = env.action_space.n
    print('environment: in: ({}) out: ({})'.format(input_shape, output_shape))

    ddqn = DDQN(input_shape, output_shape)

    #  init training
    replay_buffer = Replay_buffer(1000)
    target_network = DDQN(input_shape, output_shape)
    target_network.set_weights(ddqn.get_weights())
    state = env.reset()
    print('initial state: {}'.format(state))

    for epc in range(epochs):
        a = ddqn.predict(state)
        action = np.argmax(a)
        next_state, reward, done, info = env.step(action)
        replay_buffer.add((state, a, reward, next_state))


if __name__ == '__main__':
    main()
