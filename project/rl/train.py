import gym
import sys
from markov_q_rl import Markov_QL
import matplotlib.pyplot as plt


GYM = 'MountainCar-v0'


def main():
    if len(sys.argv) != 2:
        print('usage: python train.py epochs')
    epochs = int(sys.argv[1])

    env = gym.make(GYM)

    ql = Markov_QL(env.action_space, env.observation_space)

    print('observation space: {}'.format(env.observation_space.shape))
    print('actions space: {}'.format(env.action_space))

    rewards = []
    best_results = []

    max_pos = -0.39
    min_episodes = 500
    for epoch in range(epochs):
        observation = env.reset()

        tot_reward = 0
        for episode in range(10**12):
            action = ql.action(observation)
            newobservation, reward, done, info = env.step(action)
            if newobservation[0] > max_pos:
                reward = 5
                max_pos = newobservation[0]
            tot_reward += reward
            ql.reward(observation, action, reward, newobservation)
            observation = newobservation
            if done:
                if episode + 1 < min_episodes:
                    min_episodes = episode + 1
                rewards.append(tot_reward)
                best_results.append(min_episodes)
                print('{} - record: {} - reward: {}'.format(epoch + 1, min_episodes, tot_reward))
                break

    plt.plot(rewards)
    plt.xlabel('epoch')
    plt.ylabel('reward')
    plt.show()

    # test
    observation = env.reset()
    for _ in range(200):
        env.render()
        action = ql.action(observation, train=False)
        observation, reward, done, info = env.step(action)

    env.close()

    ql.save('markov.bin')


if __name__ == '__main__':
    main()
