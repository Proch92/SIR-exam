import sys
import network
import genetic
import numpy as np

# genetic
POPULATION_SIZE = 80
ELITISM = 0.4
MUTATION_RATE = 0.1

# other const
NETWORK_SIZE = 10


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

    fitness = [simulate(net) for net in population]
    best = np.argmax(fitness)
    champion = population[best]
    for test in [(True, False), (False, False), (True, True), (False, True)]:
        for _ in range(10):
            out = champion.step(test)[0]
        if out == (test[0] != test[1]):
            print("ok!")
        else:
            print("wrong: {} {} -> {}".format(test[0], test[1], out))


def simulate(net):
    tests = [(True, True), (True, False), (False, True), (False, False)] * 10
    test_epochs = 10
    tot_reward = 0
    for test in tests:
        target = (test[0] != test[1])  # xor
        for _ in range(test_epochs):
            action = net.step(test)[0]
        if (action == target):
            tot_reward += 1
    return tot_reward


def init():
    topology = network.Network.random_topology(2, 1, NETWORK_SIZE)

    population = [network.Network(topology) for _ in range(POPULATION_SIZE)]
    population[0].print_info()

    return population


if __name__ == '__main__':
    main()
