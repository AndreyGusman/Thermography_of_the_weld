import scr.config as config
from camera import *
from neural_network import *

import cv2
import numpy as np


def test_camera():
    camera_cap = Camera()
    camera_cap.get_capture()
    count = 0
    while True:
        count += 1
        img = camera_cap.get_img()
        orig_img = camera_cap.get_origin_img()
        cv2.imshow("test camera_cap class origin img", orig_img)
        cv2.imshow("test camera_cap class", img)

        if count == 20:
            count = 0
            config.ROTATION_ANGLE += 90

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def test_neural_network():
    network = NeuralNetwork()
    network.working_model = network.create_new_cnn_model()
    network.working_model = network.get_compile_model(network.working_model)
    network.get_summary()
    network.save_model(path='', name="test Model")
    network.load_model(model_name='test Model', model_path='')
    network.get_summary()


def test_camera_and_nn():
    arr_img = []
    count = 0

    camera_cap = Camera()
    camera_cap.get_capture()

    network = NeuralNetwork()
    network.working_model = network.create_new_cnn_model()
    network.working_model = network.get_compile_model(network.working_model)
    network.get_summary()

    while True:
        img = camera_cap.get_img()
        arr_img.append(img)
        count += 1
        if count == 4:
            arr_img = np.array(arr_img)
            arr_img = np.expand_dims(arr_img, axis=3)
            arr_img = np.array(arr_img)
            predict = network.model_predict(arr_img)
            print(predict)
            count = 0
            arr_img = []
        cv2.imshow("test camera_cap class", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
