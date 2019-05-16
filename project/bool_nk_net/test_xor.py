import sys
import network
import genetic
import random

# genetic
POPULATION_SIZE = 80
ELITISM = 0.4
MUTATION_RATE = 0.1

# other const
NETWORK_SIZE = 100


def main():
    if len(sys.argv) != 2:
        print('usage: python test_xor.py epochs')
    epochs = int(sys.argv[1])

    population = init()

    ga = genetic.GA(POPULATION_SIZE, MUTATION_RATE, ELITISM)

    for epoch in range(epochs):
        fitness = [simulate(net) for net in population]
        population = ga.step(population, fitness)
        print('epoch: {} - best fitness: {}'.format(epoch, max(fitness)))


def simulate(net):
    tests = 100
    tot_reward = 0
    observation = random.choices([True, False], k=2)
    for _ in range(tests):
        action = net.step(observation)
        tot_reward += 1 if (action == (observation[0] != observation[1])) else 0
    return tot_reward


def init():
    topology = network.Network.random_topology(2, 1, NETWORK_SIZE)

    population = [network.Network(topology) for _ in range(POPULATION_SIZE)]
    population[0].print_info()

    return population


if __name__ == '__main__':
    main()
