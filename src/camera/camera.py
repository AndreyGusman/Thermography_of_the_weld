import time
import cv2
import numpy as np

from src.config import Config
from src.data_format import DataFormat


class Camera:
    def __init__(self):
        self.capture = None
        self.config = Config()

        self.current_plc_data = {}
        self.origin_img = None
        self.gray_img = None
        self.time_last_img = None
        self.calculated_frame_coordinate = None

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

            self.time_last_img = time.time()
            self.calculated_frame_coordinate = self.current_plc_data.get('Pos_UZK')

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

    def get_current_img_and_plc_data(self):
        var_name_current_img = DataFormat.var_name_current_img.copy()
        img = self.get_img()
        ret_dict = {var_name: self.current_plc_data.get(var_name) for var_name in var_name_current_img}
        ret_dict['image'] = img
        return ret_dict

    def test_get_broken_img_and_plc_data(self, img):
        var_name_broken_img = DataFormat.var_name_broken_img.copy()
        ret_dict = {var_name: self.current_plc_data.get(var_name) for var_name in var_name_broken_img}
        ret_dict['image'] = img
        return ret_dict

    def create_data_frame_to_parquet(self):
        if self.config.PARQUET_MODE == 1:
            var_name_to_parquet = DataFormat.parquet_format_mode_1.copy()
            ret_dict = {var_name: self.current_plc_data.get(var_name) for var_name in var_name_to_parquet}
            ret_dict['Image'] = self.gray_img
            ret_dict['Length'] = self.calculated_frame_coordinate
            ret_dict['Time'] = self.time_last_img
            ret_dict['reserve zone 1'] = 0
            ret_dict['reserve zone 2'] = 0
            return ret_dict

        # img_to_parquet = dict.copy(dict_img)
        # for i in range(len(img_to_parquet)):
        #     img_to_parquet[i] = self.camera.convert_img_to_one_row(img_to_parquet[i])
        # if len(img_to_parquet) == 1:
        #     img_to_parquet.append(np.zeros((1, 1)))
        # # пока нет железа имитируем данные с ПЛК
        # data_frame = [time.time(), random.randint(10, 10000), random.random(),
        #               self.camera.config.OUT_FRAME_WIDTH * self.camera.config.OUT_FRAME_HEIGHT]
        # for el in img_to_parquet:
        #     data_frame.append(list(el))
        # return data_frame

    def update_current_plc_data(self, data):
        self.current_plc_data = data

    @staticmethod
    def convert_img_to_one_row(conv_img: np.array):
        return np.reshape(conv_img, (1, -1))

    @staticmethod
    def convert_img_to_one_column(conv_img):
        return np.reshape(conv_img, (-1, 1))


def test_1():
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






if __name__ == '__main__':
    pass
