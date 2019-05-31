import gym

from dqn import DQN


def main():
    env = gym.make("CartPole-v0")

    dqn = DQN([256, 256, 128], )


if __name__ == '__main__':
    main()
