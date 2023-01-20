import cv2
import numpy as np
from src.config import Config
import matplotlib.pyplot as plt
import matplotlib as mlp


class Camera:
    def __init__(self):
        self.origin_img = None
        self.gray_img = None
        self.capture = None
        self.config = Config()
        colors = ["blue", "green", "green", "red"]
        nodes = [0.0, 0.5, 0.5, 1.0]
        self.colormap = mlp.colors.LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))  # 'inferno'
        self.current_plc_data = None

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

    def color_img_to_the_colormap(self, img):
        rgb_img = (self.colormap(img) * 2 ** 8).astype(np.uint8)[:, :, :3]

        return rgb_img

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


def test_2():
    test_camera = Camera()

    test_camera.get_capture()
    while True:
        image = test_camera.get_img()
        rgb_img = test_camera.color_img_to_the_colormap(image)
        print(len(image.shape))
        cv2.imshow('image', image)
        cv2.imshow('heatmap', rgb_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def plot_examples(colormaps):
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(19680801)
    data = np.random.randn(30, 30)
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        fig.colorbar(psm, ax=ax)
    plt.show()


def test_colormap():
    colors = ["blue", "green", "green", "red"]
    cmap1 = mlp.colors.LinearSegmentedColormap.from_list("mycmap", colors)
    nodes = [0.0, 0.2, 0.6, 1.0]
    cmap2 = mlp.colors.LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

    print(cmap2)
    plot_examples([cmap1, cmap2])


if __name__ == '__main__':
    test_colormap()
