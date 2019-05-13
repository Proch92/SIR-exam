import gym
import genetic
import sys
import network
import bool_utils


def main():
    if len(sys.argv) != 3:
        print('usage: python train.py network epochs')
    network_path = sys.argv[1]
    epochs = int(sys.argv[2])

    env = gym.make('CartPole-v1')
    net = network.Network()
    net.random_init(4, 1, 50)
    # net.load(network_path)

    gen_optimizer = genetic.Genetic(1000)

    for epoc in range(epochs):
        observation = env.reset()
        for i in range(1000):
            env.render()
            discretized = bool_utils.discretize_1bool(observation, env.observation_space)
            action = net.step(discretized)
            observation, reward, done, info = env.step(1 if action else -1)
            if done:
                print("finished after {} steps".format(i))
                break
        env.close()

    net.save(network_path)


if __name__ == '__main__':
    main()
