import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import MaxPooling2D, Conv2D
import scr.config as config


class NewNeuralModel:

    def __init__(self):
        pass

    @staticmethod
    def create_new_fcnn_model():
        pass

    @staticmethod
    def create_new_cnn_model():
        new_model = Sequential()
        new_model.add(
            Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=config.INPUT_SHAPE))
        new_model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
        new_model.add(MaxPooling2D((2, 2), strides=2))
        new_model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
        new_model.add(MaxPooling2D((2, 2), strides=2))
        new_model.add(Conv2D(64, (2, 2), padding='same', activation='relu'))
        new_model.add(MaxPooling2D((2, 2), strides=2))
        new_model.add(Flatten())
        new_model.add(Dense(64, activation='relu'))
        new_model.add(Dense(128, activation='relu'))
        new_model.add(Dense(11, activation='softmax'))
        return new_model

    @staticmethod
    def get_compile_model(uncompile_model, optimizer='rmsprop', loss='categorical_crossentropy', metrics='accuracy'):
        uncompile_model.compile(optimizer=optimizer, loss=loss,
                                metrics=[metrics])
        return uncompile_model


if __name__ == '__main__':
    pass
