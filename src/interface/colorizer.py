import matplotlib.pyplot as plt
import matplotlib as mlp
import numpy as np


class Colorizer:
    def __init__(self):
        self.min_temperature = 0.5
        self.max_temperature = 0.5
        self.colors = ["blue", "green", "green", "red"]
        self.default_nodes = [0.0, 0.5, 0.5, 1.0]
        self.nodes = [0.0, self.min_temperature, self.max_temperature, 1.0]
        self.default_colormap = mlp.colors.LinearSegmentedColormap.from_list("default_colormap",
                                                                             list(zip(self.default_nodes,
                                                                                      self.colors)))  # 'inferno'
        self.current_colormap = None

    def color_img_to_the_colormap(self, img):
        if self.current_colormap is None:
            rgb_img = (self.default_colormap(img) * 2 ** 8).astype(np.uint8)[:, :, :3]
        else:
            rgb_img = (self.current_colormap(img) * 2 ** 8).astype(np.uint8)[:, :, :3]
        return rgb_img
    # TODO привязать создание цветовой карты к интерфейсу
    def create_colormap(self):
        if self.max_temperature >= self.min_temperature:
            self.current_colormap = mlp.colors.LinearSegmentedColormap.from_list("default_colormap",
                                                                                 list(zip(self.nodes,
                                                                                          self.colors)))


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
