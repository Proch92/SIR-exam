import gym

from ddqn import DDQN


def main():
    env = gym.make("CartPole-v0")

    ddqn = DDQN(layers=[256, 256, 128])


if __name__ == '__main__':
    main()
