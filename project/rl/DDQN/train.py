import gym
from ddqn import DDQN
import numpy as np
import sys
from replay_buffer import Replay_buffer
import tensorflow as tf
import random
import os.path
import math

tf.enable_eager_execution()

GYM = "CartPole-v1"
TARGET_RESET_FREQ = 20
REPLAY_BUFFER_SIZE = 2000
BATCH_SIZE = 50
DISCOUNT = 0.99
TRAINING_START = BATCH_SIZE + 100
TRAINING_FREQ = 5

# epsilon greedy exploration
E_START = 1
E_MIN = 0.01
E_DECAY = 1000
E_RESET_FREQ = 50000


def get_epsilon(epoc):
    return E_MIN + (E_START - E_MIN) * math.exp(-1. * epoc / E_DECAY)


def main():
    if len(sys.argv) != 3:
        print('usage: python ' + sys.argv[0] + ' epochs [weights_path]')
        exit(0)

    epochs = int(sys.argv[1])
    weights_path = sys.argv[2]

    env = gym.make(GYM)
    input_shape = env.observation_space.shape[0]
    output_shape = env.action_space.n
    print('environment: in: ({}) out: ({})'.format(input_shape, output_shape))

    ddqn = DDQN(input_shape, output_shape)
    if os.path.exists(weights_path):
        ddqn.load_weights(weights_path)

    optimizer = tf.train.AdamOptimizer()

    # init training
    replay_buffer = Replay_buffer(REPLAY_BUFFER_SIZE)
    target_network = DDQN(input_shape, output_shape)
    target_network.set_weights(ddqn.get_weights())

    target_reset_count = 0
    train_counter = 0
    e_counter = 0
    epsilon_explore = E_START
    loss_value = 0
    rewards_x_epoch = []
    e_x_time = []
    loss_x_time = []

    for epc in range(epochs):
        state = env.reset()
        state = np.expand_dims(state, 0)
        tot_reward = 0
        for _ in range(1000):
            # action selection
            if random.random() <= epsilon_explore:
                action = random.randint(0, output_shape - 1)
            else:
                q_values = ddqn.predict(state)
                action = np.argmax(q_values)

            # simulation
            next_state, reward, done, info = env.step(action)
            next_state = np.expand_dims(next_state, 0)
            replay_buffer.add((state, action, reward, next_state, 0 if done else 1))
            state = next_state
            tot_reward += reward

            # training
            train_counter += 1
            if train_counter > TRAINING_START and train_counter % TRAINING_FREQ == 0:
                (batch_states, batch_actions, batch_s_t1, batch_rewards, batch_final) = replay_buffer.sample(BATCH_SIZE)

                with tf.GradientTape() as tape:
                    # actual prediction
                    action_indexes = tf.stack([tf.range(BATCH_SIZE, dtype=tf.int64), batch_actions], axis=1)
                    y_prediction = tf.gather_nd(ddqn(batch_states), action_indexes)

                    # targets
                    amax = tf.argmax(ddqn(batch_s_t1), axis=1)
                    amax = tf.stack([tf.range(BATCH_SIZE, dtype=tf.int64), amax], axis=1)
                    batch_target_y = target_network(batch_s_t1)
                    target_expected_rewards = tf.gather_nd(batch_target_y, amax)
                    y_target = batch_rewards + (DISCOUNT * target_expected_rewards * batch_final)

                    # loss
                    loss_value = tf.reduce_mean(tf.pow(y_target - y_prediction, 2))

                grads = tape.gradient(loss_value, ddqn.trainable_variables)

                optimizer.apply_gradients(zip(grads, ddqn.trainable_variables))

            if train_counter > TRAINING_START:
                e_counter += 1
                epsilon_explore = get_epsilon(e_counter)
            if e_counter > E_RESET_FREQ:
                e_counter = 0

            e_x_time.append(epsilon_explore)
            loss_x_time.append(float(loss_value))

            target_reset_count += 1
            if target_reset_count == TARGET_RESET_FREQ:
                target_network.set_weights(ddqn.get_weights())
                target_reset_count = 0

            if done:
                break

        rewards_x_epoch.append(tot_reward)

        if epc % 10 == 0:
                print('[{:2.1f}%], e: {:5.4f} - loss: {:10.6f} - last episode reward: {}'.format((epc * 100) / epochs, epsilon_explore, float(loss_value), tot_reward))

    ddqn.save_weights(weights_path, save_format='h5')

    with open('rewards.csv', 'w') as f:
        for rew in rewards_x_epoch:
            f.write("%s," % rew)

    with open('epsilon.csv', 'w') as f:
        for e in e_x_time:
            f.write("%s," % e)

    with open('loss.csv', 'w') as f:
        for l in loss_x_time:
            f.write("%s," % l)

    # let's try it
    obs = env.reset()
    obs = np.expand_dims(obs, 0)
    for _ in range(1000):
        env.render()
        q_values = ddqn.predict(obs)
        action = np.argmax(q_values)
        obs, reward, done, info = env.step(action)
        obs = np.expand_dims(obs, 0)

        if done:
            break

    env.close()


if __name__ == '__main__':
    main()
