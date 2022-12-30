# константы системы
MAX_QUEUE_SIZE = 10
PROGRAM_CAMERA_CLOSE = False

# константы камеры
USE_NOTEBOOK_CAMERA = True  # тестовый режим камеры

CAMERA_NAME = 0  # путь захвата изображения камеры

SOURCE_FRAME_WIDTH = 640  # размеры исходного изображения
SOURCE_FRAME_HEIGHT = 480

ROTATION_ANGLE = 0  # поворот изображения (кратно 90!)

OUT_FRAME_WIDTH = 500  # размеры выходного изображения
OUT_FRAME_HEIGHT = 500

CAMERA_ADC = 8  # глубина цвета пикселя камеры

CONVERT_TO_8BIT = False  # перевод изображения в 8-ми битный режим

NORMALIZATION = False  # перевод значения пикселей к диапазону 0..1

# настройки создания и обучения нейросетей
# создание сети
INPUT_SHAPE = (
    OUT_FRAME_HEIGHT,
    OUT_FRAME_WIDTH,
    1)  # входная размерность нейросети ширина, высота, колличество каналов

# тренировка сети
BATCH_SIZE = 4
EPOCHS = 10

# настройки работы с паркетом
WORKING_DIRECTORY = ""
TITTLE = ['Time', 'Length', 'defect', 'Size', 'Image', 'Defect image']
