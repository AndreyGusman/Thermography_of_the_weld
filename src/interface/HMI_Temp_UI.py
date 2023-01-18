import sys

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView
                             )


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("resources/ui_res/HMI_rev2.ui", self)

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

        # TreeView
        self.T_Parquet = self.findChild(QTreeView, "T_Parquet")

        # ScrollBar
        self.ScrollBar_Parquet = self.findChild(QScrollBar, "ScrollBar_Parquet")

        # DateTimeEdit
        self.dateTimeArch = self.findChild(QDateTimeEdit, "dateTimeArch")

        # Show the App
        self.show()

        # Обход корневого каталога
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.T_Parquet.setModel(self.model)
        self.T_Parquet.setRootIndex(self.model.index('/'))
        self.T_Parquet.doubleClicked.connect(self._on_double_clicked)
        self.T_Parquet.setAnimated(False)
        self.T_Parquet.setIndentation(20)
        self.T_Parquet.setSortingEnabled(True)

    def check_profibus(self, net_status):
        if net_status:
            pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
            self.l_Profibus_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
            self.l_Profibus_OK.setPixmap(pix)

    def check_transf(self, net_status):
        if net_status:
            pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
            self.l_Transf_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
            self.l_Transf_OK.setPixmap(pix)

    def check_camera(self, net_status):
        if net_status:
            pix = QtGui.QPixmap('resources/ui_res/icons8_ok.ico')
            self.l_Camera_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('resources/ui_res/icons8_cancel.ico')
            self.l_Camera_OK.setPixmap(pix)

    def set_DT(self):
        dateSelected = self.calendar.selectedDate()
        H = self.B_Hour.value()
        M = self.B_Minute.value()
        S = self.B_Second.value()
        DT = (str(dateSelected.toPyDate()) + str(-H) + str(-M) + str(-S))
        list = (DT.split("-"))
        year = list[0]
        month = list[1]
        day = list[2]
        h = list[3]
        m = list[4]
        print(year, month, day, h, m)

        # Главная страница -> характеристики текущие (с профибаса)

    def set_lcd_Pos_UZK(self, x):
        perem = x
        self.lcd_Pos_UZK.value(perem)
        self.lcd_Pos_UZK_2.value(perem)

    def lcd_RollersSpeedSet(self, x):
        perem = x
        self.lcd_RollersSpeedSet.value(perem)

    def lcd_RollersSpeedAkt(self, x):
        perem = x
        self.lcd_RollersSpeedAkt.value(perem)

    def lcd_Diam(self, x):
        perem = x
        self.lcd_Diam.value(perem)

        # Главная страница -> характеристики дефектные

    def lcd_Defect(self, x):
        perem = x
        self.lcd_Defect.value(perem)

    def lcd_Defect_Place(self, x):
        perem = x
        self.lcd_Defect_Place.value(perem)

    def lcd_Temperature(self, x):
        perem = x
        self.lcd_Temperature.value(perem)

        # Cтраница параметры

    def lcd_frame_frequency(self):
        return self.lcd_frame_frequency.value()

        # Cтраница трансфокатора

    def lcd_Focus_Delta(self):
        return self.lcd_Focus_Delta.value()

    def lcd_Zoom_Delta(self):
        return self.lcd_Zoom_Delta.value()

    def _on_double_clicked(self):
        pass

    def update_broke_img(self, img, update):
        pix = self.get_pix_map(img)
        self.l_NG_img.setPixmap(pix)
        if update:
            self.update()

    def update_current_img(self, img, update):
        pix = self.get_pix_map(img)
        self.l_Current_img.setPixmap(pix)
        if update:
            self.update()

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
        image = QtGui.QImage(img, img.shape[1],
                             img.shape[0], img.shape[1] * 3, QtGui.QImage.Format.Format_RGB888)
        pix = QtGui.QPixmap(image)
        return pix


def create_ui():
    new_app = QApplication(sys.argv)
    ui_window = UI()
    return new_app, ui_window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
