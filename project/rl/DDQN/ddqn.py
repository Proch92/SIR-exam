import tensorflow as tf


class DDQN(tf.keras.Model):
    """docstring for DQN"""

    def __init__(self, input_shape, output_shape):
        super(DDQN, self).__init__(name='dqn_model')

        self.dense = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu', input_shape=(input_shape,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu')
        ])

        self.value = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(64,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1)
        ])

        self.advantage = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(64,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(output_shape)
        ])

    def call(self, input):
        x = self.dense(input)
        value = self.value(x)
        advantages = self.advantage(x)

        average_a = tf.reduce_mean(advantages)

        return tf.map_fn(lambda a: value + (a - average_a), advantages)
