from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )
from ..config import Config


class MainWin:
    def __init__(self, hmi_reference,process_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference

        self.lcd_Pos_UZK = self.hmi_reference.findChild(QLCDNumber, "lcd_Pos_UZK")
        self.lcd_RollersSpeedSet = self.hmi_reference.findChild(QLCDNumber, "lcd_RollersSpeedSet")
        self.lcd_RollersSpeedAkt = self.hmi_reference.findChild(QLCDNumber, "lcd_RollersSpeedAkt")
        self.lcd_Diam = self.hmi_reference.findChild(QLCDNumber, "lcd_Diam")

        self.lcd_Defect = self.hmi_reference.findChild(QLCDNumber, "lcd_Defect")
        self.lcd_Defect_Place = self.hmi_reference.findChild(QLCDNumber, "lcd_Defect_Place")
        self.lcd_Temperature = self.hmi_reference.findChild(QLCDNumber, "lcd_Temperature")
        self.lcdNum_Empty = self.hmi_reference.findChild(QLCDNumber, "lcdNum_Empty")

        # Текущий кадр (Главный экран)
        self.l_Current_img = self.hmi_reference.findChild(QLabel, "l_Current_img")

        # Дефектный кадр
        self.l_NG_img = self.hmi_reference.findChild(QLabel, "l_NG_img")

    def set_val_lcd_pos_uzk(self, val):
        self.lcd_Pos_UZK.display(val)

    def set_val_lcd_rollers_speed_set(self, val):
        self.lcd_RollersSpeedSet.display(val)

    def set_val_lcd_rollers_speed_akt(self, val):
        self.lcd_RollersSpeedAkt.display(val)

    def set_val_lcd_diam(self, val):
        self.lcd_Diam.display(val)

        # Главная страница -> характеристики дефектные

    def set_val_lcd_defect(self, val):
        self.lcd_Defect.display(val)

    def set_val_lcd_defect_place(self, val):
        self.lcd_Defect_Place.display(val)

    def set_val_lcd_temperature(self, val):
        self.lcd_Temperature.display(val)

    def update_defect_img(self, data: dict):
        img = data.pop('image')
        if self.hmi_reference.setting_win.get_main_screen_temperature() == 2:
            img = self.hmi_reference.colorizer.color_img_to_the_colormap(img)
        pix = self.hmi_reference.get_pix_map(img)
        self.l_NG_img.setPixmap(pix)

        self.update_defect_img_data(data)

    def update_current_img(self, data: dict):
        img = data.pop('image')
        if self.hmi_reference.setting_win.get_main_screen_temperature() == 2:
            rgb_img = self.hmi_reference.colorizer.color_img_to_the_colormap(img)
            pix = self.hmi_reference.get_pix_map(rgb_img)
            self.l_Current_img.setPixmap(pix)
        else:
            pix = self.hmi_reference.get_pix_map(img)
            self.l_Current_img.setPixmap(pix)

        self.update_current_img_data(data)

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
