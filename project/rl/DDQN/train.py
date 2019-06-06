import gym
from ddqn import DDQN
import numpy as np
import sys
from replay_buffer import Replay_buffer
import tensorflow as tf
import random
import os.path

tf.enable_eager_execution()

GYM = "CartPole-v0"
TARGET_RESET_FREQ = 100
REPLAY_BUFFER_SIZE = 10000
BATCH_SIZE = 50
DISCOUNT = 0.95
TRAINING_START = BATCH_SIZE * 50
TRAINING_FREQ = 10

# epsilon greedy exploration
E_START = 0.8
E_STOP = 0.01
E_STEP = (E_START - E_STOP) / 10**3


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
    epsilon_explore = E_START

    for epc in range(epochs):
        state = env.reset()
        state = np.expand_dims(state, 0)
        for _ in range(1000):
            # action selection
            if random.random() < epsilon_explore:
                action = random.randint(0, output_shape - 1)
            else:
                q_values = ddqn.predict(state)
                action = np.argmax(q_values)

            # simulation
            next_state, reward, done, info = env.step(action)
            next_state = np.expand_dims(next_state, 0)
            replay_buffer.add((state, action, reward, next_state, 0 if done else 1))
            state = next_state

            # training
            train_counter += 1
            if train_counter > TRAINING_START and train_counter % TRAINING_FREQ == 0:
                (batch_states, batch_actions, batch_s_t1, batch_rewards, batch_final) = replay_buffer.sample(BATCH_SIZE)

                with tf.GradientTape() as tape:
                    # actual prediction
                    action_rewards = tf.stack([tf.range(BATCH_SIZE, dtype=tf.int64), batch_actions], axis=1)
                    y_prediction = tf.gather_nd(ddqn(batch_states), action_rewards)

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

                if train_counter % 100 == 0:
                    print('[{} / {}] - loss: {:8.4f}'.format(epc, epochs, float(loss_value)))

            epsilon_explore = max(epsilon_explore - E_STEP, E_STOP)

            target_reset_count += 1
            if target_reset_count == TARGET_RESET_FREQ:
                target_network.set_weights(ddqn.get_weights())
                target_reset_count = 0

            if done:
                break

    ddqn.save_weights(weights_path)

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


if __name__ == '__main__':
    main()
