import cv2
import numpy as np
import scr.config as config


class Camera:
    def __init__(self):
        self.origin_img = None
        self.gray_img = None
        self.capture = None

    @staticmethod
    def get_current_config():
        camera_config = {"CAMERA_NAME": config.CAMERA_NAME,
                         "OUT_FRAME_HEIGHT": config.OUT_FRAME_HEIGHT,
                         "OUT_FRAME_WIDTH": config.OUT_FRAME_WIDTH,
                         "USE_NOTEBOOK_CAMERA": config.USE_NOTEBOOK_CAMERA,
                         "SOURCE_FRAME_HEIGHT": config.SOURCE_FRAME_HEIGHT,
                         "SOURCE_FRAME_WIDTH": config.SOURCE_FRAME_WIDTH,
                         "ROTATION_ANGLE": config.ROTATION_ANGLE,
                         "CAMERA_ADC": config.CAMERA_ADC,
                         "CONVERT_TO_8BIT": config.CONVERT_TO_8BIT,
                         "NORMALIZATION": config.NORMALIZATION
                         }
        return camera_config

    def get_capture(self):
        self.capture = cv2.VideoCapture(config.CAMERA_NAME)

        return self.capture

    def rotation_img(self):
        for _ in range(int(config.ROTATION_ANGLE / 90)):
            self.gray_img = np.rot90(self.gray_img)

    def resize_img(self):
        re_size = (config.OUT_FRAME_WIDTH, config.OUT_FRAME_HEIGHT)
        self.gray_img = cv2.resize(self.gray_img, re_size)

    def get_origin_img(self):
        if self.capture is not None:
            _, self.origin_img = self.capture.read()
            return self.origin_img
        else:
            print('Подключение к камере не установлено.')

    def normalization_img(self):
        if config.CONVERT_TO_8BIT:
            self.gray_img = self.gray_img / (2 ** 8)
        else:
            self.gray_img = self.gray_img / (2 ** config.CAMERA_ADC)

    def convert_img_to_8bit(self):
        self.gray_img = self.gray_img * ((2 ** 8) / (2 ** config.CAMERA_ADC))

    def get_img(self):
        if self.capture is not None:
            if config.USE_NOTEBOOK_CAMERA:
                _, bgr_img = self.capture.read()
                self.gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
            else:
                self.gray_img = self.capture.read()

            if config.ROTATION_ANGLE:
                self.rotation_img()

            if config.SOURCE_FRAME_WIDTH != config.OUT_FRAME_WIDTH \
                    or config.SOURCE_FRAME_HEIGHT != config.OUT_FRAME_HEIGHT:
                self.resize_img()

            if config.CONVERT_TO_8BIT:
                self.convert_img_to_8bit()

            if config.NORMALIZATION:
                self.normalization_img()

            return self.gray_img
        else:
            print('Подключение к камере не установлено.')

    @staticmethod
    def convert_img_to_one_row(con_img: np.array):
        return np.reshape(con_img, (1, -1))

    @staticmethod
    def convert_img_to_one_column(con_img):
        return np.reshape(con_img, (-1, 1))


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
