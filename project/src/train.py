import gym
import sys
import network
import bool_utils
import random

# genetic
POPULATION_SIZE = 1000
ELITISM = 0.4
MUTATION_RATE = 0.05

# other const
NETWORK_SIZE = 50
GYM = 'CartPole-v1'


def main():
    if len(sys.argv) != 3:
        print('usage: python train.py network epochs')
    network_path = sys.argv[1]
    epochs = int(sys.argv[2])

    population, env = init()

    for epoch in range(epochs):
        fitness = [simulate(env, net) for net in population]
        population = genetic_step(population, fitness)
        print('epoch: {} - best fitness: {}'.format(epoch, max(fitness)))

    env.close()


def genetic_step(population, fitness):
    pop_sorted_zipped = sorted(zip(population, fitness), key=lambda p: -p[1])
    pop_sorted, fitness_sorted = zip(*pop_sorted_zipped)

    elite_n = int(len(pop_sorted) * ELITISM)
    new_pop_n = POPULATION_SIZE - elite_n
    if new_pop_n % 2 == 1:
        elite_n -= 1
        new_pop_n += 1

    elite = pop_sorted[-elite_n:]

    newborns = []
    for _ in range(int(new_pop_n / 2)):
        parents = random.choices(pop_sorted, weights=fitness_sorted, k=2)
        newborns.extend(crossover(parents))
    mutate(newborns)

    new_population = elite.extend(newborns)
    assert len(new_population) == POPULATION_SIZE, "new population has different size"

    return new_population


def mutate(pop):
    for net in pop:
        if random.random() < MUTATION_RATE:
            nodes_to_swap = random.sample(range(net.graph_size), 2)
            net.swap_nodes(nodes_to_swap)


def crossover(parents):
    genomes = [parent.get_chromosome() for parent in parents]
    cut = random.choice(range(len(genomes[0])))

    chromosome0 = []
    chromosome1 = []
    chromosome0.extend(genomes[0][:cut])
    chromosome0.extend(genomes[1][cut:])
    chromosome1.extend(genomes[1][:cut])
    chromosome1.extend(genomes[0][cut:])

    child0 = network.Network()
    child0.set_chromosome(chromosome0)
    child1 = network.Network()
    child1.set_chromosome(chromosome1)

    return [child0, child1]


def simulate(env, net):
    observation = env.reset()
    tot_reward = 0
    for i in range(1000):
        discrete = [True, True, False, False]  # bool_utils.discretize_1bool(observation, env.observation_space)
        action = net.step(discrete)
        observation, reward, done, info = env.step(1 if action else -1)
        tot_reward += reward
        if done:
            break
    return tot_reward


def init():
    env = gym.make(GYM)
    input_space = env.observation_space.shape[0]  # flatten space
    output_space = env.action_space.n

    population = [network.Network() for _ in range(POPULATION_SIZE)]
    for net in population:
        net.random_init(input_space, output_space, NETWORK_SIZE)

    population[0].print_info()

    return (population, env)


if __name__ == '__main__':
    main()
