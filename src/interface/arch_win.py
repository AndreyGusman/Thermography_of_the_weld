from PyQt5.QtWidgets import (QLabel, QDateTimeEdit,
                             QPushButton, QCalendarWidget, QSpinBox, QScrollBar,
                             QFileSystemModel, QTreeView
                             )
from src.interface.load_file_controller import LoadFileController

from ..config import Config
import datetime
from pathlib import Path


class ArchWin:
    def __init__(self, hmi_reference, process_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference
        self.process_reference = process_reference

        # атрибуты экземпляра для решения задачи
        self.file_controller = LoadFileController(self, self.process_reference)

        self.last_selected_file = None
        self.last_scroll_value = None
        self.slider_over_value = 0

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

        self.navigate_info = self.hmi_reference.findChild(QLabel, "label_7")  # 60 char

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
        self.ScrollBar_Parquet.sliderReleased.connect(self.is_change_file)

        self.btn_Set_DT.clicked.connect(self.set_dt)
        self.T_Parquet.doubleClicked.connect(self._on_double_clicked)

    def show_img(self):
        select_img_id = self.ScrollBar_Parquet.value()

        key = f'Image {select_img_id}'
        self.file_controller.current_view_pq_file.get_img_and_plc_data(key, select_img_id)

        if select_img_id != self.ScrollBar_Parquet.minimum() or select_img_id != self.ScrollBar_Parquet.maximum():
            self.slider_over_value = 0

    def is_change_file(self):
        self.last_scroll_value = self.ScrollBar_Parquet.value()
        if self.last_scroll_value == self.ScrollBar_Parquet.minimum() or self.last_scroll_value == self.ScrollBar_Parquet.maximum():
            self.slider_over_value += 1
        else:
            self.slider_over_value = 0
        if self.slider_over_value >= 2 and self.last_scroll_value == self.ScrollBar_Parquet.minimum():
            self.file_controller.replace_previous_file()
        if self.slider_over_value >= 2 and self.last_scroll_value == self.ScrollBar_Parquet.maximum():
            self.file_controller.replace_next_file()

    def _on_double_clicked(self):
        index = self.T_Parquet.currentIndex()
        file_path = self.model.filePath(index)
        spl_file_path = file_path.split('.')
        if spl_file_path[-1] == 'parquet':
            self.file_controller.check_file_is_load(file_path)
        else:
            self.set_text_parquet_info(text=f'Выбранный файл не имеет расширение .parquet')

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

    def set_text_parquet_info(self, text):
        resized_text = self.resize_str_len(text)
        self.navigate_info.setText(resized_text)

    @staticmethod
    def resize_str_len(text, mode: str = 'normal'):
        if len(text) > 59:
            if Config.WORKING_DIRECTORY in text:
                start_index = text.index(Config.WORKING_DIRECTORY)

                end_index = start_index + len(text) - 62
                resize_text = text[:start_index] + '..' + text[end_index:]

                return resize_text
        return text
