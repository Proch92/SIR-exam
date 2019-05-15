import gym
import sys
import network
import bool_utils
import genetic

# genetic
POPULATION_SIZE = 5
ELITISM = 0.4
MUTATION_RATE = 0.05

# other const
NETWORK_SIZE = 50
GYM = 'CartPole-v1'


def main():
    if len(sys.argv) != 2:
        print('usage: python train.py epochs')
    epochs = int(sys.argv[1])

    env, population = init()

    ga = genetic.GA(POPULATION_SIZE, MUTATION_RATE, ELITISM)

    for epoch in range(epochs):
        fitness = [simulate(env, net) for net in population]
        population = ga.step(population, fitness)
        print('epoch: {} - best fitness: {}'.format(epoch, max(fitness)))

    env.close()


def simulate(env, net):
    observation = env.reset()
    tot_reward = 0
    print('.')
    for i in range(10):
        discrete = bool_utils.discretize_1bool(observation, env.observation_space)
        action = net.step(discrete)
        observation, reward, done, info = env.step(1 if action else -1)
        print(observation)
        tot_reward += reward
        if done:
            break
    return tot_reward


def init():
    env = gym.make(GYM)
    input_space = env.observation_space.shape[0]  # flatten space
    output_space = env.action_space.n

    topology = network.Network.random_topology(input_space, output_space, NETWORK_SIZE)

    population = [network.Network(topology) for _ in range(POPULATION_SIZE)]
    population[0].print_info()

    return (env, population)


if __name__ == '__main__':
    main()
