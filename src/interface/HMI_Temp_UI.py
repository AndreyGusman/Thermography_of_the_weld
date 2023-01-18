from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileSystemModel,
                             QDirModel, QStackedWidget, QStyleOptionSpinBox, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView
                             )
from PyQt5 import uic, QtCore, QtGui
import sys, os


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("../../resources/ui_res/HMI_rev2.ui", self)

        # Определение виджетов
        self.btn_Main_screen = self.findChild(QPushButton, "btn_Main_screen")
        self.btn_Parametr = self.findChild(QPushButton, "btn_Parametr")
        self.btn_Transf = self.findChild(QPushButton, "btn_Transf")
        self.btn_Arch = self.findChild(QPushButton, "btn_Arch")
        self.btn_Set_DT = self.findChild(QPushButton, "btn_Set_DT")

        self.StackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        self.l_Profibus_OK = self.findChild(QLabel, "l_Profibus_OK")
        self.l_Transf_OK = self.findChild(QLabel, "l_Transf_OK")
        self.l_Camera_OK = self.findChild(QLabel, "l_Camera_OK")
        self.l_Current_img = self.findChild(QLabel, "l_Current_img")
        self.l_NG_img = self.findChild(QLabel, "l_NG_img")

        self.groupBox_4 = self.findChild(QGroupBox, "groupBox_4")
        self.groupBox_2 = self.findChild(QGroupBox, "groupBox_2")
        self.groupBox_3 = self.findChild(QGroupBox, "groupBox_3")
        self.groupBox_17 = self.findChild(QGroupBox, "groupBox_17")
        self.groupBox_11 = self.findChild(QGroupBox, "groupBox_11")
        self.groupBox_12 = self.findChild(QGroupBox, "groupBox_12")
        self.groupBox_14 = self.findChild(QGroupBox, "groupBox_14")
        self.groupBox_9 = self.findChild(QGroupBox, "groupBox_9")
        self.groupBox_10 = self.findChild(QGroupBox, "groupBox_10")

        self.lcd_Pos_UZK = self.findChild(QLCDNumber, "lcd_Pos_UZK")
        self.lcd_RollersSpeedSet = self.findChild(QLCDNumber, "lcd_RollersSpeedSet")
        self.lcd_RollersSpeedAkt = self.findChild(QLCDNumber, "lcd_RollersSpeedAkt")
        self.lcd_Diam = self.findChild(QLCDNumber, "lcd_Diam")

        self.lcd_Focus_Delta = self.findChild(QLCDNumber, "lcd_Focus_Delta")
        self.lcd_Zoom_Delta = self.findChild(QLCDNumber, "lcd_Zoom_Delta")

        self.calendar = self.findChild(QCalendarWidget, "calendar")

        self.B_Hour = self.findChild(QSpinBox, "B_Hour")
        self.B_Minute = self.findChild(QSpinBox, "B_Minute")
        self.B_Second = self.findChild(QSpinBox, "B_Second")

        self.T_Parquet = self.findChild(QTreeView, "T_Parquet")

        self.ScrollBar_Parquet = self.findChild(QScrollBar, "ScrollBar_Parquet")

        self.dateTimeArch = self.findChild(QDateTimeEdit, "dateTimeArch")

        # Определение событий элементов
        self.btn_Main_screen.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(0))
        self.btn_Parametr.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(2))
        self.btn_Transf.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(1))
        self.btn_Arch.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(3))
        self.btn_Set_DT.clicked.connect(self.set_DT)

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

    def check_profibus(self, Net):
        if Net == True:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_ok.ico')
            self.l_Profibus_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_cancel.ico')
            self.l_Profibus_OK.setPixmap(pix)

    def check_transf(self, Net):
        if Net == True:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_ok.ico')
            self.l_Transf_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_cancel.ico')
            self.l_Transf_OK.setPixmap(pix)

    def check_camera(self, Net):
        if Net == True:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_ok.ico')
            self.l_Camera_OK.setPixmap(pix)
        else:
            pix = QtGui.QPixmap('../../resources/ui_res/icons8_cancel.ico')
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

    def _on_double_clicked(self):
        pass


def create_ui():
    app = QApplication(sys.argv)
    UIWindow = UI()
    return app, UIWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
