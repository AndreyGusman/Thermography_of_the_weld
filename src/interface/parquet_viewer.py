from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QLabel, QDateTimeEdit,
                             QLCDNumber, QPushButton, QCalendarWidget, QSpinBox, QDoubleSpinBox, QGroupBox, QScrollBar,
                             QFileSystemModel, QTreeView, QCheckBox, QLineEdit
                             )


class ParquetViewer:
    def __init__(self, hmi_reference):
        self.metadata = None
        self.image_and_plc_data = {}
        self.hmi_reference = hmi_reference

        # ScrollBar
        self.ScrollBar_Parquet = self.hmi_reference.findChild(QScrollBar, "ScrollBar_Parquet")
        self.ScrollBar_Parquet.valueChanged.connect(self.show_img)
        self.ScrollBar_Parquet.setMinimum(1)
        self.ScrollBar_Parquet.setPageStep(1)

    def associate_img_and_plc_data(self, img_data):
        self.image_and_plc_data[f'Image {img_data["Image id"]}']['Image'] = img_data['Image']
        if img_data["Image id"] == 1:
            read_img_and_data = self.image_and_plc_data.get(f'Image {1}').copy()
            self.hmi_reference.update_arch_img(read_img_and_data)

    def set_metadata(self, metadata):
        self.metadata = metadata
        self.ScrollBar_Parquet.setMaximum(self.metadata['number_frames'])

    def set_plc_data(self, plc_data):
        self.image_and_plc_data = plc_data

    def show_img(self):
        try:
            select_img_id = self.ScrollBar_Parquet.value()
            print(select_img_id)
            key = f'Image {select_img_id}'

            if key != 'Image':
                if self.image_and_plc_data.get(key) is not None:
                    read_img_and_data = self.image_and_plc_data.get(f'Image {select_img_id}').copy()
                    if read_img_and_data['Image'] is not None:
                        self.hmi_reference.update_arch_img(read_img_and_data)
                        print(f'load {key}')

        except Exception as e:
            pass
