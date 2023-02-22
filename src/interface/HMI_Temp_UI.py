import sys
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit, QMessageBox
                             )

from src.interface.colorizer import Colorizer
from src.interface.arch_win import ArchWin
from src.interface.main_win import MainWin
from src.interface.setting_win import SettingWin
from src.interface.transfocator_win import TransfocatorWin


# TODO прописать чтение и отображение архивных записей
class UI(QMainWindow):
    def __init__(self, process_reference):
        super(UI, self).__init__()
        # Load the ui file
        uic.loadUi("resources/ui_res/HMI_rev2.ui", self)

        # ссылка на процесс для вызова его методов
        self.process_reference = process_reference

        # инициализация виджетов и методов экранов
        self.colorizer = Colorizer()
        self.arch_win = ArchWin(self, self.process_reference)
        self.main_win = MainWin(self, self.process_reference)
        self.setting_win = SettingWin(self, self.process_reference)
        self.transfocator_win = TransfocatorWin(self, self.process_reference)

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
        # Кнопки переключения экранов
        self.StackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        # Label
        # Связь профибас
        self.l_Profibus_OK = self.findChild(QLabel, "l_Profibus_OK")
        # Связь с трансфокатором
        self.l_Transf_OK = self.findChild(QLabel, "l_Transf_OK")
        # Связь с камерой
        self.l_Camera_OK = self.findChild(QLabel, "l_Camera_OK")

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

        # Определение событий элементов
        self.btn_Main_screen.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(0))
        self.btn_Parametr.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(2))
        self.btn_Transf.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(1))
        self.btn_Arch.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(3))

        # Show the App
        self.show()

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

        # Cтраница параметры

    def show_img_and_plc_data(self, data: dict):
        if data.get('current_img') is not None:
            self.main_win.update_current_img(data.get('current_img').copy())
            self.transfocator_win.update_transfocator_img(data.get('current_img').copy())
        if data.get('broken_img') is not None:
            self.main_win.update_defect_img(data.get('broken_img').copy())

    def get_pix_map(self, img):
        if len(img.shape) == 2:
            return self.get_pix_map_mono_ch(img)
        elif len(img.shape) == 3:
            return self.get_pix_map_rgb_ch(img)
        else:
            print('image wrong shape')

    def show_message(self, title, message, box_type="info"):
        msg_box = QMessageBox
        msg_box.about(self, title, message)

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


def create_ui(process_reference):
    new_app = QApplication(sys.argv)
    ui_window = UI(process_reference)
    return new_app, ui_window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI(process_reference=None)
    app.exec_()
