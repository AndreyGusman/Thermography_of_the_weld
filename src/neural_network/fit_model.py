from tensorflow import keras

import matplotlib as plt
import numpy as np


class InterfaceFitModel:
    def __init__(self):
        pass

    @staticmethod
    def fit_model(model: keras.Sequential, x_train: np.array, y_train: np.array,
                  batch_size,
                  epochs):
        history = model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs)

        return history

    @staticmethod
    def show_history(history):
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    pass
