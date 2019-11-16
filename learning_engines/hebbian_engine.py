import logging

from tqdm import trange
import numpy as np
from matplotlib import pyplot as plt

from utils.visualization import draw_weights_update
from optimizers.optimizer import Optimizer


class HebbianEngine:

    def __init__(self, learning_rule, optimizer: Optimizer, visualize_weights: bool = False):
        self.learning_rule = learning_rule
        self.optimizer = optimizer
        self.visualize_weights = visualize_weights

    def fit(self, output_size: int, data, epochs: int, batch_size: int):
        temp = int(np.sqrt(output_size))
        out_grid = (temp, temp)
        samples = data.shape[0]
        input_size = data[0].shape[0] * data[0].shape[1]

        logging.info('Received {} samples.'.format(samples))
        logging.info('Input size = {}.'.format(input_size))
        logging.info('Output size = {}.'.format(output_size))

        synapses = np.random.normal(0.0, 1.0, (output_size, input_size))

        # Visualization
        fig = None
        if self.visualize_weights:
            plt.ion()
            fig = plt.figure()
            draw_weights_update(fig, synapses, data[0].shape, out_grid[0], out_grid[1])

        # Main loop
        for epoch in range(epochs):
            data = data[np.random.permutation(samples), :]

            batch_range = trange(samples // batch_size, desc='Epoch {}/{}'.format(epoch + 1, epochs))
            for batch in batch_range:
                inputs = data[batch * batch_size:(batch + 1) * batch_size, :]
                inputs = np.reshape(inputs, (inputs.shape[0], -1))

                synapses += self.optimizer.get_updates(self.learning_rule.update(inputs, synapses), epoch, epochs)

            if self.visualize_weights:
                draw_weights_update(fig, synapses, data[0].shape, out_grid[0], out_grid[1])

        # Wrap-up
        plt.ioff()
        plt.close()

        return synapses