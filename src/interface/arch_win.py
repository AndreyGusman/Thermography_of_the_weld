from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )
from ..config import Config
import datetime
from pathlib import Path
import glob
from natsort import natsorted


class ArchWin:
    def __init__(self, hmi_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference

        # атрибуты экземпляра для решения задачи
        self.metadata = None
        self.image_and_plc_data = {}
        self.last_selected_file = None

        self.sorted_file_path_list = None
        self.dict_parquet_file = None
        self.update_sorted_file_path_list()

        # подключение виджетов с класса HMI
        # Buttons
        # Применение даты и времени
        self.btn_Set_DT = self.hmi_reference.findChild(QPushButton, "btn_Set_DT")

        # ScrollBar
        self.ScrollBar_Parquet = self.hmi_reference.findChild(QScrollBar, "ScrollBar_Parquet")

        # TreeView
        self.T_Parquet = self.hmi_reference.findChild(QTreeView, "T_Parquet")
        self.ScrollBar_Parquet.setMinimum(1)
        self.ScrollBar_Parquet.setPageStep(1)

        # DateTimeEdit
        self.dateTimeArch = self.hmi_reference.findChild(QDateTimeEdit, "dateTimeArch")

        # CalendarWidget
        self.calendar = self.hmi_reference.findChild(QCalendarWidget, "calendar")

        # SpinBox
        self.B_Hour = self.hmi_reference.findChild(QSpinBox, "B_Hour")
        self.set_val_hour(int(datetime.datetime.now().hour))

        self.B_Minute = self.hmi_reference.findChild(QSpinBox, "B_Minute")
        self.B_Second = self.hmi_reference.findChild(QSpinBox, "B_Second")

        # Архивный кадр
        self.l_Arch_img = self.hmi_reference.findChild(QLabel, "l_Arch_img")

        # Обход корневого каталога
        self.model = QFileSystemModel()

        self.model.setRootPath(Config.WORKING_DIRECTORY)
        self.T_Parquet.setModel(self.model)
        self.T_Parquet.setRootIndex(self.model.index(Config.WORKING_DIRECTORY))
        self.T_Parquet.setAnimated(False)
        self.T_Parquet.setIndentation(20)
        self.T_Parquet.setSortingEnabled(True)
        for i in range(1, self.T_Parquet.header().length()):
            self.T_Parquet.hideColumn(i)

        self.ScrollBar_Parquet.valueChanged.connect(self.show_img)
        self.btn_Set_DT.clicked.connect(self.set_dt)
        self.T_Parquet.doubleClicked.connect(self._on_double_clicked)

    def associate_img_and_plc_data(self, img_data):
        self.image_and_plc_data[f'Image {img_data["Image id"]}']['Image'] = img_data['Image']
        if img_data["Image id"] == 1:
            read_img_and_data = self.image_and_plc_data.get(f'Image {1}').copy()
            self.update_arch_img(read_img_and_data)

    def set_metadata(self, metadata):
        self.metadata = metadata
        self.ScrollBar_Parquet.setMaximum(self.metadata['number_frames'])

    def set_plc_data(self, plc_data):
        self.image_and_plc_data = plc_data

    def show_img(self):
        select_img_id = self.ScrollBar_Parquet.value()
        key = f'Image {select_img_id}'
        if key != 'Image':
            if self.image_and_plc_data.get(key) is not None:
                read_img_and_data = self.image_and_plc_data.get(f'Image {select_img_id}').copy()
                if read_img_and_data['Image'] is not None:
                    self.update_arch_img(read_img_and_data)

    def _on_double_clicked(self):
        index = self.T_Parquet.currentIndex()
        self.hmi_reference.process_reference.get_parquet_file(self.model.filePath(index))

    def set_dt(self):
        date_selected = self.calendar.selectedDate()
        h_val = self.B_Hour.value()
        dt = (str(date_selected.toPyDate()) + str(-h_val))
        dt_list = (dt.split("-"))
        for i in range(len(dt_list)):
            if dt_list[i][0] == '0':
                dt_list[i] = dt_list[i][1:]
        str_file_path = Config.WORKING_DIRECTORY
        for el in dt_list:
            str_file_path += "/"
            str_file_path += el
        if self.last_selected_file != str_file_path:

            if Path(str_file_path).exists():
                self.last_selected_file = str_file_path
                self.T_Parquet.setRootIndex(self.model.index(self.last_selected_file))
            else:
                self.hmi_reference.show_message(title='Внимание!',
                                                message='В указанное время запись БД не производилась')
        else:
            self.T_Parquet.setRootIndex(self.model.index(Config.WORKING_DIRECTORY))
            self.last_selected_file = None

        # print(str_file_path)

    def update_arch_img_data(self, data):
        pass

    def update_arch_img(self, data: dict):
        img = data.pop('Image')
        if self.hmi_reference.setting_win.get_arch_screen_temperature() == 2:
            rgb_img = self.hmi_reference.colorizer.color_img_to_the_colormap(img)
            pix = self.hmi_reference.get_pix_map(rgb_img)
            self.l_Arch_img.setPixmap(pix)
        else:
            pix = self.hmi_reference.get_pix_map(img)
            self.l_Arch_img.setPixmap(pix)

        self.update_arch_img_data(data)

    def set_val_hour(self, val):
        self.B_Hour.setValue(val)

    def update_sorted_file_path_list(self):
        file_pattern = Config.WORKING_DIRECTORY + '/*' + '/*' + '/*' + '/*' + '/*.parquet'
        file_path_list = glob.glob(file_pattern)
        for i in range(len(file_path_list)):
            file_path_list[i] = file_path_list[i].replace('\\', '/')
        file_path_list = natsorted(file_path_list)
        self.sorted_file_path_list = file_path_list
        self.update_dict_parquet_file()

    def update_dict_parquet_file(self):
        self.dict_parquet_file = {self.sorted_file_path_list[i]: i for i in range(len(self.sorted_file_path_list))}
        print(self.dict_parquet_file)
