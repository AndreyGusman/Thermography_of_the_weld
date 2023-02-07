import sys
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )

from src.interface.colorizer import Colorizer
from src.interface.parquet_viewer import ParquetViewer
from ..config import Config


# from src.processes_and_threading.ui_process import UIProcess


# TODO прописать чтение и отображение архивных записей
class UI(QMainWindow):
    def __init__(self, process_reference):
        super(UI, self).__init__()
        # Load the ui file
        uic.loadUi("resources/ui_res/HMI_rev2.ui", self)

        self.colorizer = Colorizer()
        self.parquet_viewer = ParquetViewer(self)
        self.process_reference = process_reference

        self.selected_file_path = None
        # Определение виджетов

        # Buttons
        # Главный экран
        self.btn_Main_screen = self.findChild(QPushButton, "btn_Main_screen")
        # Параметры
        self.btn_Parametr = self.findChild(QPushButton, "btn_Parametr")
        # Трансфокатор
        self.btn_Transf = self.findChild(QPushButton, "btn_Transf")
        # Архив
        self.btn_Arch = self.findChild(QPushButton, "btn_Arch")
        # Применение даты и времени
        self.btn_Set_DT = self.findChild(QPushButton, "btn_Set_DT")

        self.StackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        # Label
        # Связь профибас
        self.l_Profibus_OK = self.findChild(QLabel, "l_Profibus_OK")
        # Связь с трансфокатором
        self.l_Transf_OK = self.findChild(QLabel, "l_Transf_OK")
        # Связь с камерой
        self.l_Camera_OK = self.findChild(QLabel, "l_Camera_OK")
        # Текущий кадр (Главный экран)
        self.l_Current_img = self.findChild(QLabel, "l_Current_img")
        # Текущий кадр 2 (Трансфокатор)
        self.l_Current_img_2 = self.findChild(QLabel, "l_Current_img_2")
        # Дефектный кадр
        self.l_NG_img = self.findChild(QLabel, "l_NG_img")
        # Архивный кадр
        self.l_Arch_img = self.findChild(QLabel, "l_Arch_img")

        # GroupBox
        self.groupBox_4 = self.findChild(QGroupBox, "groupBox_4")
        self.groupBox_2 = self.findChild(QGroupBox, "groupBox_2")
        self.groupBox_3 = self.findChild(QGroupBox, "groupBox_3")
        self.groupBox_17 = self.findChild(QGroupBox, "groupBox_17")
        self.groupBox_11 = self.findChild(QGroupBox, "groupBox_11")
        self.groupBox_12 = self.findChild(QGroupBox, "groupBox_12")
        self.groupBox_14 = self.findChild(QGroupBox, "groupBox_14")
        self.groupBox_9 = self.findChild(QGroupBox, "groupBox_9")
        self.groupBox_10 = self.findChild(QGroupBox, "groupBox_10")

        # LCDNumber
        self.lcd_Pos_UZK = self.findChild(QLCDNumber, "lcd_Pos_UZK")
        self.lcd_Pos_UZK_2 = self.findChild(QLCDNumber, "lcd_Pos_UZK_2")
        self.lcd_RollersSpeedSet = self.findChild(QLCDNumber, "lcd_RollersSpeedSet")
        self.lcd_RollersSpeedSet_2 = self.findChild(QLCDNumber, "lcd_RollersSpeedSet_2")
        self.lcd_RollersSpeedAkt = self.findChild(QLCDNumber, "lcd_RollersSpeedAkt")
        self.lcd_RollersSpeedAkt_2 = self.findChild(QLCDNumber, "lcd_RollersSpeedAkt_2")
        self.lcd_Diam = self.findChild(QLCDNumber, "lcd_Diam")
        self.lcd_Diam_2 = self.findChild(QLCDNumber, "lcd_Diam_2")

        self.lcd_Defect = self.findChild(QLCDNumber, "lcd_Defect")
        self.lcd_Defect_Place = self.findChild(QLCDNumber, "lcd_Defect_Place")
        self.lcd_Temperature = self.findChild(QLCDNumber, "lcd_Temperature")
        self.lcdNum_Empty = self.findChild(QLCDNumber, "lcdNum_Empty")

        self.lcd_Focus_Delta = self.findChild(QLCDNumber, "lcd_Focus_Delta")
        self.lcd_Zoom_Delta = self.findChild(QLCDNumber, "lcd_Zoom_Delta")

        self.lcd_frame_frequency = self.findChild(QLCDNumber, "lcd_frame_frequency")

        # CalendarWidget
        self.calendar = self.findChild(QCalendarWidget, "calendar")

        # SpinBox
        self.B_Hour = self.findChild(QSpinBox, "B_Hour")
        self.B_Minute = self.findChild(QSpinBox, "B_Minute")
        self.B_Second = self.findChild(QSpinBox, "B_Second")

        self.lcd_frame_frequency = self.findChild(QSpinBox, "lcd_frame_frequency")

        self.B_min_temp = self.findChild(QDoubleSpinBox, "B_min_temp")
        self.B_max_temp = self.findChild(QDoubleSpinBox, "B_max_temp")

        # CheckBox
        self.check_arch = self.findChild(QCheckBox, "check_arch")
        self.check_main_screen = self.findChild(QCheckBox, "check_main_screen")
        self.check_transfocator = self.findChild(QCheckBox, "check_transfocator")

        # LineEdit
        self.ftp_ip = self.findChild(QLineEdit, "ftp_ip")
        self.ftp_port = self.findChild(QLineEdit, "ftp_port")
        self.ftp_login = self.findChild(QLineEdit, "ftp_login")
        self.ftp_pass = self.findChild(QLineEdit, "ftp_pass")

        # TreeView
        self.T_Parquet = self.findChild(QTreeView, "T_Parquet")



        # DateTimeEdit
        self.dateTimeArch = self.findChild(QDateTimeEdit, "dateTimeArch")

        #
        # Определение событий элементов
        self.btn_Main_screen.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(0))
        self.btn_Parametr.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(2))
        self.btn_Transf.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(1))
        self.btn_Arch.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(3))
        self.btn_Set_DT.clicked.connect(self.set_dt)
        self.B_min_temp.valueChanged.connect(self.update_val_min_temp)
        self.B_max_temp.valueChanged.connect(self.update_val_max_temp)

        # Show the App
        self.show()

        # Обход корневого каталога
        self.model = QFileSystemModel()
        # self.model.setRootPath(QDir.currentPath())
        self.model.setRootPath(Config.WORKING_DIRECTORY)
        self.T_Parquet.setModel(self.model)
        self.T_Parquet.setRootIndex(self.model.index('/'))
        self.T_Parquet.doubleClicked.connect(self._on_double_clicked)
        self.T_Parquet.setAnimated(False)
        self.T_Parquet.setIndentation(20)
        self.T_Parquet.setSortingEnabled(True)

    def update_val_min_temp(self):
        self.colorizer.min_temperature = self.B_min_temp.value()
        self.colorizer.create_colormap()

    def update_val_max_temp(self):
        self.colorizer.max_temperature = self.B_max_temp.value()
        self.colorizer.create_colormap()

    def set_status_profibus(self, net_status):
        if net_status:
            pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
            self.l_Profibus_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
            self.l_Profibus_OK.setPixmap(pix)

    def set_status_transfocator(self, net_status):
        if self.l_Transf_OK is not None:
            if net_status:
                pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
                self.l_Transf_OK.setPixmap(pix)
            else:
                pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
                self.l_Transf_OK.setPixmap(pix)
        else:
            print("self.l_Transf_OK not find")

    def set_status_camera(self, net_status):
        if net_status:
            pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
            self.l_Camera_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
            self.l_Camera_OK.setPixmap(pix)

    def set_dt(self):
        date_selected = self.calendar.selectedDate()
        h_val = self.B_Hour.value()
        m_val = self.B_Minute.value()
        s_val = self.B_Second.value()
        dt = (str(date_selected.toPyDate()) + str(-h_val) + str(-m_val) + str(-s_val))
        dt_list = (dt.split("-"))
        year = dt_list[0]
        month = dt_list[1]
        day = dt_list[2]
        h = dt_list[3]
        m = dt_list[4]
        print(year, month, day, h, m)

        # Главная страница -> характеристики текущие (с профибаса)

    def set_val_lcd_pos_uzk(self, val):
        self.lcd_Pos_UZK.display(val)
        self.lcd_Pos_UZK_2.display(val)

    def set_val_lcd_rollers_speed_set(self, val):
        self.lcd_RollersSpeedSet.display(val)
        self.lcd_RollersSpeedSet_2.display(val)

    def set_val_lcd_rollers_speed_akt(self, val):
        self.lcd_RollersSpeedAkt.display(val)
        self.lcd_RollersSpeedAkt_2.display(val)

    def set_val_lcd_diam(self, val):
        self.lcd_Diam.display(val)
        self.lcd_Diam_2.display(val)

        # Главная страница -> характеристики дефектные

    def set_val_lcd_defect(self, val):
        self.lcd_Defect.display(val)

    def set_val_lcd_defect_place(self, val):
        self.lcd_Defect_Place.display(val)

    def set_val_lcd_temperature(self, val):
        self.lcd_Temperature.display(val)

        # Cтраница параметры

    def get_val_lcd_frame_frequency(self):
        return self.lcd_frame_frequency.value()

    def get_val_min_screen_temperature(self):
        return self.B_min_temp.value()

    def get_val_max_screen_temperature(self):
        return self.B_max_temp.value()

    def get_main_screen_temperature(self):
        # return 0 - not checked; 2 - checked
        return self.check_main_screen.checkState()

    def get_transfocator_screen_temperature(self):
        # return 0 - not checked; 2 - checked
        return self.check_transfocator.checkState()

    def get_arch_screen_temperature(self):
        # return 0 - not checked; 2 - checked
        return self.check_arch.checkState()

    def get_ftp_ip(self):
        # return string
        return self.ftp_ip.text()

    def get_ftp_port(self):
        # return string
        return self.ftp_port.text()

    def get_ftp_login(self):
        # return string
        return self.ftp_login.text()

    def get_ftp_pass(self):
        # return string
        return self.ftp_pass.text()

        # Cтраница трансфокатора

    def get_val_lcd_focus_delta(self):
        return self.lcd_Focus_Delta.value()

    def get_val_lcd_zoom_delta(self):
        return self.lcd_Zoom_Delta.value()

    def _on_double_clicked(self):
        index = self.T_Parquet.currentIndex()
        self.process_reference.get_parquet_file(self.model.filePath(index))

    def show_img_and_plc_data(self, data: dict):
        if data.get('current_img') is not None:
            self.update_current_img(data.get('current_img'))
        if data.get('broken_img') is not None:
            self.update_defect_img(data.get('broken_img'))

    def update_arch_img(self, data: dict):
        img = data.pop('Image')
        if self.get_transfocator_screen_temperature() == 2:
            img = self.colorizer.color_img_to_the_colormap(img)
        pix = self.get_pix_map(img)
        self.l_Arch_img.setPixmap(pix)

        self.update_arch_img_data(data)

    def update_defect_img(self, data: dict):
        img = data.pop('image')
        if self.get_main_screen_temperature() == 2:
            img = self.colorizer.color_img_to_the_colormap(img)
        pix = self.get_pix_map(img)
        self.l_NG_img.setPixmap(pix)

        self.update_defect_img_data(data)

    def update_current_img(self, data: dict):
        img = data.pop('image')
        if self.get_main_screen_temperature() == 2:
            rgb_img = self.colorizer.color_img_to_the_colormap(img)
            pix = self.get_pix_map(rgb_img)
            self.l_Current_img.setPixmap(pix)
        else:
            pix = self.get_pix_map(img)
            self.l_Current_img.setPixmap(pix)

        if self.get_transfocator_screen_temperature() == 2 and len(img.shape) == 2:
            rgb_img = self.colorizer.color_img_to_the_colormap(img)
            pix = self.get_pix_map(rgb_img)
            self.l_Current_img_2.setPixmap(pix)
        else:
            pix = self.get_pix_map(img)
            self.l_Current_img_2.setPixmap(pix)

        self.update_current_img_data(data)

    def get_pix_map(self, img):
        if len(img.shape) == 2:
            return self.get_pix_map_mono_ch(img)
        elif len(img.shape) == 3:
            return self.get_pix_map_rgb_ch(img)
        else:
            print('image wrong shape')

    @staticmethod
    def get_pix_map_mono_ch(img):
        image = QtGui.QImage(img, img.shape[1],
                             img.shape[0], img.shape[1], QtGui.QImage.Format.Format_Grayscale8)
        pix = QtGui.QPixmap(image)
        return pix

    @staticmethod
    def get_pix_map_rgb_ch(img):
        im_np = np.array(img)
        q_image = QtGui.QImage(im_np.data, im_np.shape[1], im_np.shape[0],
                               QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(q_image)
        return pix

    def update_current_img_data(self, data: dict):
        var_to_update_func = {'Pos_UZK': self.set_val_lcd_pos_uzk,
                              'RollersSpeedSet': self.set_val_lcd_rollers_speed_set,
                              'RollersSpeedAkt': self.set_val_lcd_rollers_speed_akt, 'Diam': self.set_val_lcd_diam
                              }
        for key in var_to_update_func:
            # var_to_update_func словарь сопоставления имён переменных получаемых из data и функций куда
            # их нужно передать для обновления. var_to_update_func.get(key) получает ссылку на функцию
            # (val=data.get(key)) вызывает функцию со следующими аргументами data.get(key)
            var_to_update_func.get(key)(val=data.get(key))

    def update_defect_img_data(self, data: dict):
        var_to_update_func = {'Defect': self.set_val_lcd_defect,
                              'Pos_UZK': self.set_val_lcd_defect_place,
                              'Defect_temperature': self.set_val_lcd_temperature}
        for key in var_to_update_func:
            # var_to_update_func словарь сопоставления имён переменных получаемых из data и функций куда
            # их нужно передать для обновления. var_to_update_func.get(key) получает ссылку на функцию
            # (val=data.get(key)) вызывает функцию со следующими аргументами data.get(key)
            var_to_update_func.get(key)(val=data.get(key))

    def update_arch_img_data(self,data):
        pass


def create_ui(process_reference):
    new_app = QApplication(sys.argv)
    ui_window = UI(process_reference)
    return new_app, ui_window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
