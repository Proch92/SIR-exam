def discretize_1bool(observation, space):
    discretized = []
    for i, val in enumerate(observation):
        discretized.append(val > ((space.low[i] + space.high[i]) / 2))
    return discretized
