import cv2
import numpy as np
from scr.config import Config


class Camera:
    def __init__(self):
        self.origin_img = None
        self.gray_img = None
        self.capture = None
        self.config = Config()

    def get_current_config(self):
        camera_config = {"CAMERA_NAME": self.config.CAMERA_NAME,
                         "OUT_FRAME_HEIGHT": self.config.OUT_FRAME_HEIGHT,
                         "OUT_FRAME_WIDTH": self.config.OUT_FRAME_WIDTH,
                         "USE_NOTEBOOK_CAMERA": self.config.USE_NOTEBOOK_CAMERA,
                         "SOURCE_FRAME_HEIGHT": self.config.SOURCE_FRAME_HEIGHT,
                         "SOURCE_FRAME_WIDTH": self.config.SOURCE_FRAME_WIDTH,
                         "ROTATION_ANGLE": self.config.ROTATION_ANGLE,
                         "CAMERA_ADC": self.config.CAMERA_ADC,
                         "CONVERT_TO_8BIT": self.config.CONVERT_TO_8BIT,
                         "NORMALIZATION": self.config.NORMALIZATION
                         }
        return camera_config

    def get_capture(self):
        self.capture = cv2.VideoCapture(self.config.CAMERA_NAME)

        return self.capture

    def rotation_img(self):
        for _ in range(int(self.config.ROTATION_ANGLE / 90)):
            self.gray_img = np.rot90(self.gray_img)

    def resize_img(self):
        re_size = (self.config.OUT_FRAME_WIDTH, self.config.OUT_FRAME_HEIGHT)
        self.gray_img = cv2.resize(self.gray_img, re_size)

    def get_origin_img(self):
        if self.capture is not None:
            _, self.origin_img = self.capture.read()
            return self.origin_img
        else:
            print('Подключение к камере не установлено.')

    def normalization_img(self):
        if self.config.CONVERT_TO_8BIT:
            self.gray_img = self.gray_img / (2 ** 8)
        else:
            self.gray_img = self.gray_img / (2 ** self.config.CAMERA_ADC)

    def convert_img_to_8bit(self):
        self.gray_img = self.gray_img * ((2 ** 8) / (2 ** self.config.CAMERA_ADC))

    def get_img(self):
        if self.capture is not None:
            if self.config.USE_NOTEBOOK_CAMERA:
                _, bgr_img = self.capture.read()
                self.gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
            else:
                self.gray_img = self.capture.read()

            if self.config.ROTATION_ANGLE:
                self.rotation_img()

            if self.config.SOURCE_FRAME_WIDTH != self.config.OUT_FRAME_WIDTH \
                    or self.config.SOURCE_FRAME_HEIGHT != self.config.OUT_FRAME_HEIGHT:
                self.resize_img()

            if self.config.CONVERT_TO_8BIT:
                self.convert_img_to_8bit()

            if self.config.NORMALIZATION:
                self.normalization_img()

            return self.gray_img
        else:
            print('Подключение к камере не установлено.')

    @staticmethod
    def convert_img_to_one_row(conv_img: np.array):
        return np.reshape(conv_img, (1, -1))

    @staticmethod
    def convert_img_to_one_column(conv_img):
        return np.reshape(conv_img, (-1, 1))


if __name__ == '__main__':
    test_camera = Camera()

    test_camera.get_capture()
    while True:
        img = test_camera.get_img()
        orig_img = test_camera.get_origin_img()
        cv2.imshow("test camera class origin img", orig_img)
        cv2.imshow("test camera class", img)
        print(test_camera.convert_img_to_one_column(img))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
