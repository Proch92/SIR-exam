import random
import dill
from node import Node
import gates


class Network:
    def __init__(self, topology):
        (nodes, input_nodes, output_nodes) = topology
        self.nodes = nodes
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.graph_size = len(self.nodes)
        self.gates = random.choices(range(len(gates.boolean_matrix)), k=self.graph_size)
        self.init_swaps()

    def step(self, inputs):
        assert len(inputs) == len(self.input_nodes), "number of inputs is different than expected number"

        self.swap()

        for i, inp in enumerate(inputs):
            self.state[self.input_nodes[i]] = inp

        for i in range(self.graph_size):
            self.activations[i] = self.nodes[i].activate(self.state, self.gates[i])

        return [self.activations[out] for out in self.output_nodes]

    def swap(self):
        s = self.activations
        self.activations = self.state
        self.state = s

    def init_swaps(self):
        self.state = random.choices([False, True], k=(self.graph_size))
        self.activations = random.choices([False, True], k=(self.graph_size))

    def print_info(self):
        print('# of nodes: {}'.format(len(self.nodes)))
        print('# of net states: {}'.format(len(self.state)))
        print('input shape: ({})'.format(len(self.input_nodes)))
        print('output shape: ({})'.format(len(self.output_nodes)))
        print('nodes max parents number: {}'.format(max([len(n.parents) for n in self.nodes])))

    def copy(self):
        return Network((self.nodes, self.input_nodes, self.output_nodes))

    # def save(self, filename):
    #     with open(filename, mode="wb") as f:
    #         dill.dump({
    #             'nodes': [node.parents for node in self.nodes],
    #             'input_nodes': self.input_nodes,
    #             'output_nodes': self.output_nodes,
    #             'gates': None
    #         }, f)

    # @staticmethod
    # def load(filename):
    #     with open(filename, mode="rb") as f:
    #         data = dill.load(f)
    #         input_nodes = data['input_nodes']
    #         output_nodes = data['output_nodes']
    #         gates = data['gates']
    #         nodes = []
    #         for parents in data['nodes']:
    #             n = Node()
    #             n.add_parents(parents)
    #             nodes.append(n)

    #         return Network((nodes, input_nodes, output_nodes), gates)

    @staticmethod
    def random_topology(n_inputs, n_outputs, graph_size):
        nodes = []

        for i in range(graph_size):
            nodes.append(Node())
            parents = random.sample(range(graph_size), 2)
            nodes[i].add_parents(parents)

        output_nodes = random.sample(range(graph_size), n_outputs)
        input_nodes = random.sample(range(graph_size), n_inputs)

        assert len(nodes) == graph_size, "random initialization produced more nodes than expected"

        return (nodes, input_nodes, output_nodes)
