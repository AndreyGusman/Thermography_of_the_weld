from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )
from ..config import Config


class TransfocatorWin:
    def __init__(self, hmi_reference,process_reference):
        # ссылка на интерфейс для подключения виджетов
        self.hmi_reference = hmi_reference
        self.process_reference = process_reference
        # LCDNumber

        self.lcd_Pos_UZK_2 = self.hmi_reference.findChild(QLCDNumber, "lcd_Pos_UZK_2")
        self.lcd_RollersSpeedSet_2 = self.hmi_reference.findChild(QLCDNumber, "lcd_RollersSpeedSet_2")
        self.lcd_RollersSpeedAkt_2 = self.hmi_reference.findChild(QLCDNumber, "lcd_RollersSpeedAkt_2")
        self.lcd_Diam_2 = self.hmi_reference.findChild(QLCDNumber, "lcd_Diam_2")

        # Текущий кадр 2 (Трансфокатор)
        self.l_Current_img_2 = self.hmi_reference.findChild(QLabel, "l_Current_img_2")

    def set_val_lcd_pos_uzk(self, val):
        self.lcd_Pos_UZK_2.display(val)

    def set_val_lcd_rollers_speed_set(self, val):
        self.lcd_RollersSpeedSet_2.display(val)

    def set_val_lcd_rollers_speed_akt(self, val):
        self.lcd_RollersSpeedAkt_2.display(val)

    def set_val_lcd_diam(self, val):
        self.lcd_Diam_2.display(val)

    def update_transfocator_img(self, data: dict):
        img = data.pop('image')
        if self.hmi_reference.setting_win.get_transfocator_screen_temperature() == 2 and len(img.shape) == 2:
            rgb_img = self.hmi_reference.colorizer.color_img_to_the_colormap(img)
            pix = self.hmi_reference.get_pix_map(rgb_img)
            self.l_Current_img_2.setPixmap(pix)
        else:
            pix = self.hmi_reference.get_pix_map(img)
            self.l_Current_img_2.setPixmap(pix)
