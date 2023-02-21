import ctypes
from ctypes import *
import numpy as np
import cv2


class DeviceInformation(ctypes.Structure):
    fields = [("name", ctypes.c_char * 16),  # 定义一维数组 Определите одномерный массив
              ("transport", ctypes.c_char * 16),
              ("url", ctypes.c_char * 32),
              ("address", ctypes.c_char * 16),
              ("interfaceName", ctypes.c_char * 16),
              ("serial_num", ctypes.c_char * 16),
              ("pid", ctypes.c_int),
              ("width", ctypes.c_short),
              ("height", ctypes.c_short)]


fileName = "../BinX64/IRSDK.dll"  # 此处根据dll实际所在位置设置路径 Задайте здесь путь в соответствии с фактическим расположением библиотеки dll
GHOPTO_SDK = ctypes.WinDLL(fileName)


# Поиск подключенных устройств

m_deviceCount = c_int(0)

# 枚举查找设备 Перечислять и находить устройства
GHOPTO_SDK.IR_EnumerateDevices.argtypes = [c_void_p, c_void_p, c_int]
GHOPTO_SDK.IR_EnumerateDevices.restype = c_int
GHOPTO_SDK.IR_EnumerateDevices(None, byref(m_deviceCount), 0x00000020)
# USB设备0x00000020   #千兆网口设备0x00000008 # USB-устройство 0x00000020 # Устройство с гигабитным сетевым портом 0x00000008

# 获取设备信息打开设备 # Получите информацию об устройстве, чтобы открыть устройство
m_deviceList = DeviceInformation()
GHOPTO_SDK.IR_EnumerateDevices(pointer(m_deviceList), byref(m_deviceCount), 0x01000000)

m_DeviceHandle = None  # 设备号 # Номер устройства
GHOPTO_SDK.IR_OpenDevice.argtypes = [c_void_p, c_char_p]
GHOPTO_SDK.IR_OpenDevice.restype = c_void_p
m_DeviceHandle = GHOPTO_SDK.IR_OpenDevice(None, m_deviceList.url)

# 获取相机幅面大小 # Получить размер формата камеры
iWidth = c_int(0)
iHeight = c_int(0)
GHOPTO_SDK.IR_GetDigitArrayPara.argtypes = [c_void_p, c_void_p, c_void_p]
GHOPTO_SDK.IR_GetDigitArrayPara(m_DeviceHandle, byref(iWidth), byref(iHeight))

# Получение данных изображения
GHOPTO_SDK.IR_GetNewArray.argtypes = [c_void_p, ]
GHOPTO_SDK.IR_GetNewArray(m_DeviceHandle)  # 每次获取新图像都需调用一次该函数 # Эту функцию необходимо вызывать каждый раз, когда вы получаете новое изображение

arr_size = iWidth.value * iHeight.value
pRawShortData = (c_int16 * arr_size)([0])
cast(pRawShortData, POINTER(c_int16))
pBmpData = (c_uint8 * arr_size)([0])
cast(pBmpData, POINTER(c_int8))

# 获取14位原始数据，按两字节存放 # Получите 14 бит необработанных данных и сохраните их в двух байтах
GHOPTO_SDK.IR_GetDigitArray.argtypes = [c_void_p, POINTER(c_int16)]
GHOPTO_SDK.IR_GetDigitArray(m_DeviceHandle, pRawShortData)

# 原始数据转8位数据，方便显示   # Исходные данные преобразуются в 8-битные для удобства отображения
GHOPTO_SDK.IR_DigitArrayToBmp.argtypes = [c_void_p, POINTER(c_int16), POINTER(c_uint8), c_int, c_void_p]
GHOPTO_SDK.IR_DigitArrayToBmp(m_DeviceHandle, pRawShortData, pBmpData, 0, None)

# Использование дисплея модуля cv2
# 一维数据转二维矩阵 # Преобразование одномерных данных в двумерную матрицу
np_image = np.array(pBmpData).reshape(iHeight.value, iWidth.value)
np_image = np.flipud(np_image)  # 对数据进行上下反转，实现正常图像数据

# 调用cv2显示  # Вызовите cv2 для отображения
cv2.imshow('Camera Video', np_image)
key = cv2.waitKey(50)  # 50ms刷新一次 # 50 мс обновите один раз

# Управление параметрами камеры (возьмем коррекцию затвора в качестве примера, чтобы показать применение функции IR_SendSeriaPortCmd)
cmd = c_uint8 * 16
SHUTTER = cmd(0xFF, 0xFF, 0xAA, 0xFF, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
for i in range(3, len(SHUTTER) - 1):
    SHUTTER[15] = SHUTTER[15] ^ SHUTTER[i]

GHOPTO_SDK.IR_SendSeriaPortCmd.argtypes = [c_void_p, c_void_p, c_int]
GHOPTO_SDK.IR_SendSeriaPortCmd.restype = c_bool
GHOPTO_SDK.IR_SendSeriaPortCmd(m_DeviceHandle, byref(SHUTTER), len(SHUTTER))


# подводить итог
# Вышесказанное в основном реализует подключение камеры и реализацию отображения видео. Что касается других функций и приложений SDK, то на данный момент это не было реализовано и будет продолжено.благодарить！
