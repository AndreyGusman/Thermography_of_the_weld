from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )
from ..config import Config


class SettingWin:
    def __init__(self, hmi_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference

        self.lcd_Focus_Delta = self.hmi_reference.findChild(QLCDNumber, "lcd_Focus_Delta")
        self.lcd_Zoom_Delta = self.hmi_reference.findChild(QLCDNumber, "lcd_Zoom_Delta")

        self.lcd_frame_frequency = self.hmi_reference.findChild(QLCDNumber, "lcd_frame_frequency")

        self.lcd_frame_frequency = self.hmi_reference.findChild(QSpinBox, "lcd_frame_frequency")

        self.B_min_temp = self.hmi_reference.findChild(QDoubleSpinBox, "B_min_temp")
        self.B_max_temp = self.hmi_reference.findChild(QDoubleSpinBox, "B_max_temp")

        # CheckBox
        self.check_arch = self.hmi_reference.findChild(QCheckBox, "check_arch")
        self.check_main_screen = self.hmi_reference.findChild(QCheckBox, "check_main_screen")
        self.check_transfocator = self.hmi_reference.findChild(QCheckBox, "check_transfocator")

        # LineEdit
        self.ftp_ip = self.hmi_reference.findChild(QLineEdit, "ftp_ip")
        self.ftp_port = self.hmi_reference.findChild(QLineEdit, "ftp_port")
        self.ftp_login = self.hmi_reference.findChild(QLineEdit, "ftp_login")
        self.ftp_pass = self.hmi_reference.findChild(QLineEdit, "ftp_pass")

        self.B_min_temp.valueChanged.connect(self.update_val_min_temp)
        self.B_max_temp.valueChanged.connect(self.update_val_max_temp)

    def update_val_min_temp(self):
        self.hmi_reference.colorizer.min_temperature = self.B_min_temp.value()
        self.hmi_reference.colorizer.create_colormap()

    def update_val_max_temp(self):
        self.hmi_reference.colorizer.max_temperature = self.B_max_temp.value()
        self.hmi_reference.colorizer.create_colormap()

    def get_val_lcd_focus_delta(self):
        return self.lcd_Focus_Delta.value()

    def get_val_lcd_zoom_delta(self):
        return self.lcd_Zoom_Delta.value()

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