import gym
import sys
from markov_q_rl import Markov_QL


GYM = 'MountainCar-v0'


def main():
    if len(sys.argv) != 2:
        print('usage: python train.py bin')
    filename = sys.argv[1]

    env = gym.make(GYM)

    ql = Markov_QL.load(filename)

    # test
    observation = env.reset()
    for _ in range(200):
        env.render()
        action = ql.action(observation, train=False)
        observation, reward, done, info = env.step(action)

    env.close()


if __name__ == '__main__':
    main()
