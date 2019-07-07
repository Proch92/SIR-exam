import gym
from ddqn import DDQN
import numpy as np
import sys
import os.path
import tensorflow as tf

tf.enable_eager_execution()

GYM = "LunarLander-v2"


def main():
    if len(sys.argv) != 2:
        print('usage: python ' + sys.argv[0] + ' [weights_path]')
        exit(0)

    weights_path = sys.argv[1]

    env = gym.make(GYM)
    env = gym.wrappers.Monitor(env, "./video", force=True)
    input_shape = env.observation_space.shape[0]
    output_shape = env.action_space.n
    print('environment: in: ({}) out: ({})'.format(input_shape, output_shape))

    ddqn = DDQN(input_shape, output_shape)
    if os.path.exists(weights_path):
        ddqn.load_weights(weights_path)

    state = env.reset()
    state = np.expand_dims(state, 0)
    tot_reward = 0
    for _ in range(1000):
        env.render()

        q_values = ddqn.predict(state)
        action = np.argmax(q_values)

        next_state, reward, done, info = env.step(action)
        next_state = np.expand_dims(next_state, 0)
        state = next_state
        tot_reward += reward

        if done:
            break

    env.close()
    print('total reward: {}'.format(tot_reward))


if __name__ == '__main__':
    main()
