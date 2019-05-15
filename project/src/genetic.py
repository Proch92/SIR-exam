import random


class GA(object):
    """docstring for GA"""

    def __init__(self, population_size, mutation_rate, elitism):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism = elitism

    def step(self, population, fitness):
        pop_sorted_zipped = sorted(zip(population, fitness), key=lambda p: -p[1])
        pop_sorted, fitness_sorted = zip(*pop_sorted_zipped)

        elite_n = int(len(pop_sorted) * self.elitism)
        new_pop_n = self.population_size - elite_n

        new_population = []
        new_population.extend(pop_sorted[-elite_n:])

        newborns = []
        for _ in range(new_pop_n):
            parents = random.choices(pop_sorted, weights=fitness_sorted, k=2)
            newborns.append(self.crossover(parents))
        self.mutate(newborns)

        new_population.extend(newborns)

        assert len(new_population) == self.population_size, "new population has different size"
        return new_population

    def mutate(self, pop):
        for net in pop:
            if random.random() < self.mutation_rate:
                gates_swap = random.sample(range(net.graph_size), 2)
                g = net.gates[gates_swap[0]]
                net.gates[gates_swap[0]] = net.gates[gates_swap[1]]
                net.gates[gates_swap[1]] = g

    def crossover(self, parents):
        genomes = [parent.gates for parent in parents]
        cut = random.choice(range(len(genomes[0])))

        child = parents[0].copy()
        newgates = []
        newgates.extend(genomes[0][:cut])
        newgates.extend(genomes[1][cut:])
        child.gates = newgates

        return child
