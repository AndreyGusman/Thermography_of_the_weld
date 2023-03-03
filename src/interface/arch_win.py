from PyQt5.QtWidgets import (QLabel, QDateTimeEdit,
                             QPushButton, QCalendarWidget, QSpinBox, QScrollBar,
                             QFileSystemModel, QTreeView
                             )
from src.interface.loaded_parquet_file import LoadedParquetFile
from src.interface.parquet_analyser import ParquetAnalyser
from ..config import Config
import datetime
from pathlib import Path


class ArchWin:
    def __init__(self, hmi_reference, process_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference
        self.process_reference = process_reference

        # атрибуты экземпляра для решения задачи
        self.parquet_analyser = ParquetAnalyser()
        self.current_view_pq_file = LoadedParquetFile(self, is_current_file=True)
        self.next_view_pq_file = LoadedParquetFile(self)
        self.previous_view_pq_file = LoadedParquetFile(self)

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

    def associate_img_and_plc_data(self, img_data):
        file_name = img_data.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.associate_img_and_plc_data(img_data)
            if self.current_view_pq_file.is_loaded and self.next_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.next_view_pq_file.file_name)

        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.associate_img_and_plc_data(img_data)
            if self.next_view_pq_file.is_loaded and self.previous_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.previous_view_pq_file.file_name)

        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.associate_img_and_plc_data(img_data)

    def set_metadata(self, metadata: dict):
        file_name = metadata.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.set_metadata(metadata)
            self.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.set_metadata(metadata)
            self.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.set_metadata(metadata)
            self.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        # self.ScrollBar_Parquet.setMaximum(self.metadata['number_frames'])

    def set_plc_data(self, plc_data):
        file_name = plc_data.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.set_plc_data(plc_data)
            self.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')
        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.set_plc_data(plc_data)
            self.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')
        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.set_plc_data(plc_data)
            self.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')

    def show_img(self):
        select_img_id = self.ScrollBar_Parquet.value()

        key = f'Image {select_img_id}'
        self.current_view_pq_file.get_img_and_plc_data(key, select_img_id)

        if select_img_id != self.ScrollBar_Parquet.minimum() or select_img_id != self.ScrollBar_Parquet.maximum():
            self.slider_over_value = 0

    def is_change_file(self):
        self.last_scroll_value = self.ScrollBar_Parquet.value()
        if self.last_scroll_value == self.ScrollBar_Parquet.minimum() or self.last_scroll_value == self.ScrollBar_Parquet.maximum():
            self.slider_over_value += 1
        else:
            self.slider_over_value = 0
        if self.slider_over_value >= 2 and self.last_scroll_value == self.ScrollBar_Parquet.minimum():
            self.replace_previous_file()
        if self.slider_over_value >= 2 and self.last_scroll_value == self.ScrollBar_Parquet.maximum():
            self.replace_next_file()

    def replace_previous_file(self):
        if isinstance(self.previous_view_pq_file.file_name, str) and \
                isinstance(self.previous_view_pq_file.metadata, dict) and \
                isinstance(self.previous_view_pq_file.image_and_plc_data, dict):
            self.set_text_parquet_info(text=f'Подгружен предыдущий parquet файл {self.previous_view_pq_file.file_name}')

            data1, data2, data3 = self.current_view_pq_file.get_all_data()
            self.next_view_pq_file.set_all_data(data1, data2, data3)

            data1, data2, data3 = self.previous_view_pq_file.get_all_data()
            self.current_view_pq_file.set_all_data(data1, data2, data3)

            last_key = list(self.current_view_pq_file.image_and_plc_data.keys())[-1]
            last_key = last_key.split(' ')[-1]
            self.ScrollBar_Parquet.setMaximum(int(last_key))
            if self.current_view_pq_file.is_loaded:
                self.ScrollBar_Parquet.setValue(self.current_view_pq_file.metadata.get('number_frames'))
                self.show_img()

            self.previous_view_pq_file.clear_data()
            _, self.previous_view_pq_file.file_name = self.parquet_analyser.check_neighboring_file(
                self.current_view_pq_file.file_name)
            if self.previous_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.previous_view_pq_file.file_name)
        else:
            self.hmi_reference.show_message(title='Внимание!',
                                            message='Предыдущего parquet файла не существует')

    def replace_next_file(self):
        if isinstance(self.next_view_pq_file.file_name, str) and \
                isinstance(self.next_view_pq_file.metadata, dict) and \
                isinstance(self.next_view_pq_file.image_and_plc_data, dict):
            self.set_text_parquet_info(text=f'Подгружен следующий parquet файл {self.next_view_pq_file.file_name}')

            data1, data2, data3 = self.current_view_pq_file.get_all_data()
            self.previous_view_pq_file.set_all_data(data1, data2, data3)

            data1, data2, data3 = self.next_view_pq_file.get_all_data()
            self.current_view_pq_file.set_all_data(data1, data2, data3)

            last_key = list(self.current_view_pq_file.image_and_plc_data.keys())[-1]
            last_key = last_key.split(' ')[-1]
            self.ScrollBar_Parquet.setMaximum(int(last_key))
            if self.current_view_pq_file.is_loaded:
                self.ScrollBar_Parquet.setValue(1)
                self.show_img()

            self.next_view_pq_file.clear_data()
            self.next_view_pq_file.file_name, _ = self.parquet_analyser.check_neighboring_file(
                self.current_view_pq_file.file_name)
            if self.next_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.next_view_pq_file.file_name)
        else:
            self.hmi_reference.show_message(title='Внимание!',
                                            message='Следующего parquet файла не существует')

    def _on_double_clicked(self):
        index = self.T_Parquet.currentIndex()
        file_path = self.model.filePath(index)
        spl_file_path = file_path.split('.')
        if spl_file_path[-1] == 'parquet':
            self.check_file_is_load(file_path)
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

    def check_file_is_load(self, file_path):
        if file_path == self.current_view_pq_file.file_name:
            print('file is load')
            return
        else:

            if file_path == self.previous_view_pq_file.file_name:
                if isinstance(self.previous_view_pq_file.file_name, str) and \
                        isinstance(self.previous_view_pq_file.metadata, dict) and \
                        isinstance(self.previous_view_pq_file.image_and_plc_data, dict):
                    self.replace_previous_file()
                    print('load prev file')
                    return

            if file_path == self.next_view_pq_file.file_name:
                if isinstance(self.next_view_pq_file.file_name, str) and \
                        isinstance(self.next_view_pq_file.metadata, dict) and \
                        isinstance(self.next_view_pq_file.image_and_plc_data, dict):
                    self.replace_next_file()
                    print('load next file')
                    return

            self.process_reference.get_parquet_file(file_path)
            self.set_text_parquet_info(text=f'Создан запрос на чтение файда {file_path}')
            self.current_view_pq_file.file_name = file_path
            self.next_view_pq_file.file_name, self.previous_view_pq_file.file_name = self.parquet_analyser.check_neighboring_file(
                file_path)
            print('load new file')
            return

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
