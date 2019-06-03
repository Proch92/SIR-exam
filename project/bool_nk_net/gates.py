import itertools

gates = [
    lambda ins: ins[0] and ins[1],
    lambda ins: ins[0] or ins[1],
    lambda ins: ins[0] != ins[1],
    lambda ins: not (ins[0] and ins[1]),
    lambda ins: not (ins[0] or ins[1]),
    lambda ins: not (ins[0] != ins[1]),
    lambda ins: ins[0],
    lambda ins: ins[1],
    lambda ins: not ins[0],
    lambda ins: not ins[1],
]

boolean_matrix = list(itertools.product([0, 1], repeat=1))
