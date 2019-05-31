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
