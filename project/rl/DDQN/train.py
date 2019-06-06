import gym
from ddqn import DDQN
import numpy as np
import sys
from replay_buffer import Replay_buffer
import tensorflow as tf

tf.enable_eager_execution()

GYM = "CartPole-v0"
TARGET_RESET_FREQ = 50
REPLAY_BUFFER_SIZE = 1000
BATCH_SIZE = 10
DISCOUNT = 0.95
TRAINING_START = BATCH_SIZE * 5
TRAINING_FREQ = 5


def main():
    if len(sys.argv) != 2:
        print('usage: python ' + sys.argv[0] + ' epochs')
        exit(0)

    epochs = int(sys.argv[1])

    env = gym.make(GYM)
    input_shape = env.observation_space.shape[0]
    output_shape = env.action_space.n
    print('environment: in: ({}) out: ({})'.format(input_shape, output_shape))

    ddqn = DDQN(input_shape, output_shape)

    optimizer = tf.train.AdamOptimizer()

    # test
    state = env.reset()
    print('TEST - state: {}'.format(state))
    q = ddqn.predict(np.expand_dims(state, 0))
    print('TEST - prediction: {}'.format(q))

    # init training
    replay_buffer = Replay_buffer(REPLAY_BUFFER_SIZE)
    target_network = DDQN(input_shape, output_shape)
    target_network.set_weights(ddqn.get_weights())

    target_reset_count = 0
    train_counter = 0

    for epc in range(epochs):
        state = env.reset()
        state = np.expand_dims(state, 0)
        for _ in range(1000):
            # simulation
            q_values = ddqn.predict(state)
            action = np.argmax(q_values)
            next_state, reward, done, info = env.step(action)
            next_state = np.expand_dims(next_state, 0)
            replay_buffer.add((state, q_values, action, reward, next_state, 0 if done else 1))
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
                    loss_value = tf.reduce_mean(tf.pow(y_prediction - y_target, 2))
                    print(float(loss_value))

                grads = tape.gradient(loss_value, ddqn.trainable_variables)

                optimizer.apply_gradients(zip(grads, ddqn.trainable_variables))

            target_reset_count += 1
            if target_reset_count == TARGET_RESET_FREQ:
                target_network.set_weights(ddqn.get_weights())
                target_reset_count = 0

            if done:
                break


def construct_y(e, ddqn, target_network):
    (s, q, a, r, s_t1, final) = e
    if final:
        return r
    else:
        amax = np.argmax(ddqn.predict(s_t1))
        return r + DISCOUNT * target_network.predict(s_t1)[0][amax]


if __name__ == '__main__':
    main()
