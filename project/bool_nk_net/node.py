class Node:
    def __init__(self):
        self.parents = []
        self.parent_n = 0

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_parents(self, _parents):
        self.parents.extend(_parents)

    def activate(self, past, gate):
        # print("{} {} -> {}".format(past[self.parents[0]], past[self.parents[1]], gate([past[self.parents[0]], past[self.parents[1]]])))
        return gate([past[p] for p in self.parents])
