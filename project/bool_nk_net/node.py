import gates


class Node:
    def __init__(self):
        self.parents = []

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_parents(self, _parents):
        self.parents.extend(_parents)

    def activate(self, past, gate):
        return gates.boolean_matrix[gate][(past[self.parents[0]] * 2) + (past[self.parents[1]])]
