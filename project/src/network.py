import random
import dill
from gates import gates


class Node():
    gate = None
    parents = []

    def __init__(self, gate, parents=[]):
        self.gate = gate
        self.parents = parents

    def add_parent(self, parent):
        self.parents.append(parent)

    def activate(self, past):
        return self.gate([past[p] for p in self.parents])


class Network:
    nodes = []
    input_nodes = []
    out_nodes = []
    network_state = []
    graph_size = 0

    def __init__(self):
        pass

    def step(self, inputs):
        assert (len(inputs) == len(self.input_nodes)), "number of inputs is different from expected number"
        self.network_state.extend(inputs)

        activations = [node.activate(self.network_state) for node in self.nodes]
        self.network_state = activations
        return [activations[out] for out in self.out_nodes]

    def random_init(self, n_inputs, n_outputs, graph_size=10):
        self.graph_size = graph_size
        self.network_state = random.choices([False, True], k=self.graph_size)
        connected = []

        self.nodes.append(Node(random.choice(gates)))
        connected.append(0)

        for i in range(1, self.graph_size):
            self.nodes.append(Node(random.choice(gates)))
            goto = random.choice(connected)
            parent = random.choice(connected)
            self.nodes[i].add_parent(parent)
            self.nodes[goto].add_parent(i)
            connected.append(i)

        self.nodes[0].add_parent(random.choice(connected))
        self.nodes[random.choice(connected)].add_parent(0)

        self.out_nodes = random.sample(connected, n_outputs)
        self.input_nodes = random.sample(connected, n_inputs)
        for i in range(n_inputs):
            self.nodes[self.input_nodes[i]].add_parent(self.graph_size + i)

    def save(self, filename):
        with open(filename, mode="wb") as f:
            dill.dump({
                'nodes': [(node.gate, node.parents) for node in self.nodes],
                'input_nodes': self.input_nodes,
                'out_nodes': self.out_nodes,
                'graph_size': self.graph_size
            }, f)

    def load(self, filename):
        with open(filename, mode="rb") as f:
            data = dill.load(f)
            self.graph_size = data['graph_size']
            self.input_nodes = data['input_nodes']
            self.out_nodes = data['out_nodes']
            for (gate, parents) in data['nodes']:
                self.nodes.append(Node(gate, parents))
            self.network_state = random.choices([False, True], k=(self.graph_size + len(self.input_nodes)))

    def print_info(self):
        print('# of nodes: {}'.format(len(self.nodes)))
        print('# of net states: {}'.format(len(self.network_state)))
        print('input shape: ({})'.format(len(self.input_nodes)))
        print('output shape: ({})'.format(len(self.out_nodes)))

    def check_network(self):
        assert (len(self.nodes) == len(self.network_state) - len(self.input_nodes)), "number of nodes is different from number of states minus input shape"
