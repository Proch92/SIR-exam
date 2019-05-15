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
        self.gates = random.choices(gates.gates, k=self.graph_size)
        self.init_swaps()

    def step(self, inputs):
        assert len(inputs) == len(self.input_nodes), "number of inputs is different than expected number"

        self.swap()

        for i, inp in enumerate(inputs):
            self.state[self.graph_size + i] = inp

        for i in range(self.graph_size):
            self.activations[i] = self.nodes[i].activate(self.state, self.gates[i])

        return [self.activations[out] for out in self.output_nodes]

    def swap(self):
        s = self.activations
        self.activations = self.state
        self.state = s

    def init_swaps(self):
        self.state = random.choices([False, True], k=(self.graph_size + len(self.input_nodes)))
        self.activations = random.choices([False, True], k=(self.graph_size + len(self.input_nodes)))

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
        connected = []
        nodes = []

        nodes.append(Node())
        connected.append(0)

        for i in range(1, graph_size):
            nodes.append(Node())
            goto = random.choice(connected)
            parent = random.choice(connected)
            nodes[i].add_parent(parent)
            nodes[goto].add_parent(i)
            connected.append(i)

        nodes[0].add_parent(random.choice(connected))
        nodes[random.choice(connected)].add_parent(0)

        output_nodes = random.sample(connected, n_outputs)
        input_nodes = random.sample(connected, n_inputs)
        for i in range(n_inputs):
            nodes[input_nodes[i]].add_parent(graph_size + i)

        assert len(nodes) == graph_size, "random initialization produced more nodes than expected"

        return (nodes, input_nodes, output_nodes)
