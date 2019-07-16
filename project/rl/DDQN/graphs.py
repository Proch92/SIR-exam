import csv
import matplotlib.pyplot as plt

with open('rewards.csv', 'r') as f:
    rewards = list(csv.reader(f, delimiter=','))[0][:-1]

with open('epsilon.csv', 'r') as f:
    epsilon = list(csv.reader(f, delimiter=','))[0][:-1]

with open('loss.csv', 'r') as f:
    loss = list(csv.reader(f, delimiter=','))[0][:-1]

print('rewards length {}'.format(len(rewards)))
print('epsilon length {}'.format(len(epsilon)))
print('loss length {}'.format(len(loss)))

print(rewards[0])
print(type(rewards[0]))
rewards = [int(float(r)) for r in rewards]
epsilon = [float(e) for e in epsilon]
loss = [float(l) for l in loss]
loss = [min(l, 1000.0) / 1000 for l in loss]

epochs = range(len(rewards))
steps = range(len(epsilon))

plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Total Reward')
plt.plot(epochs, rewards)
plt.savefig('rewards.png')

# plt.figure()
# plt.plot(steps, loss)
# plt.plot(steps, epsilon)
# plt.savefig('epsilon.png')
