gates = [
    all,
    any,
    lambda ins: ins.count(True) % 2 == 1,
    lambda ins: ins.count(True) % 2 == 0
]
