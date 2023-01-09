import numpy as np
from tensorflow import keras
from scr.neural_network.new_neural_model import NewNeuralModel
from scr.neural_network.fit_model import InterfaceFitModel
from scr.config import Config


class NeuralNetwork(NewNeuralModel, InterfaceFitModel):
    def __init__(self):
        super().__init__()
        self.working_model = None
        self.x_train = None
        self.y_train = None
        self.config = Config()

    def model_test(self):
        history = self.working_model.evaluate(self.x_train, self.y_train)
        print(history)
        return history

    def model_predict(self, input_arr):
        predict = self.working_model.predict(input_arr, batch_size=self.config.BATCH_SIZE)
        return predict

    def get_summary(self):
        self.working_model.summary()

    def save_model(self, path, name):
        self.working_model.save(f'{path}{name}')

    def load_model(self, model_path, model_name):
        self.working_model = keras.models.load_model(f'{model_path}{model_name}')


if __name__ == '__main__':
    network = NeuralNetwork()
