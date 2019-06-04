import tensorflow as tf


class DDQN(tf.keras.Model):
    """docstring for DQN"""

    def __init__(self, layers=[128, 64]):
        super(DDQN, self).__init__(name='dqn_model')

        if layers:
            self.model = self.model_definition(layers)

    def model_definition(self, layers):
        tf.keras.Sequential([

        ])
