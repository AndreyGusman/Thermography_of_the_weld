class Config:
    # константы системы
    PIPE_TIMEOUT = 0.01
    TRY_SEND_RECEIVE_LIMIT = 10

    # константы камеры
    USE_NOTEBOOK_CAMERA: bool = True  # тестовый режим камеры

    CAMERA_NAME: int = 0  # путь захвата изображения камеры

    SOURCE_FRAME_WIDTH: int = 640  # размеры исходного изображения
    SOURCE_FRAME_HEIGHT: int = 480

    ROTATION_ANGLE: int = 0  # поворот изображения (кратно 90!)

    OUT_FRAME_WIDTH: int = 640  # размеры выходного изображения
    OUT_FRAME_HEIGHT: int = 512

    CAMERA_ADC: int = 8  # глубина цвета пикселя камеры

    CONVERT_TO_8BIT: bool = False  # перевод изображения в 8-ми битный режим

    NORMALIZATION: bool = False  # перевод значения пикселей к диапазону 0..1

    # настройки создания и обучения нейросетей
    # создание сети
    INPUT_SHAPE: tuple = (
        OUT_FRAME_HEIGHT,
        OUT_FRAME_WIDTH,
        1)  # входная размерность нейросети ширина, высота, колличество каналов

    # тренировка сети
    BATCH_SIZE: int = 4
    EPOCHS: int = 10

    # настройки работы с parquet
    BUFFER_SIZE = 10
    WORKING_DIRECTORY: str = ""
    TITTLE = ['Time', 'Length', 'defect', 'Size', 'Image', 'Defect image']
