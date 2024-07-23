"""
(*)~---------------------------------------------------------------------------
uEye - eye tracking platform
Copyright (C) xxxxxxxxxx
Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)

@Author
@Date 2023.1.1
@Version 1.0
@email
@Description

"""

import yaml
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, \
    QGridLayout, QMessageBox, QDesktopWidget, QSlider, QRadioButton, QComboBox


# Setting interface
class setting_window(QWidget):
    def __init__(self):
        super(setting_window, self).__init__()
        self.resize(750, 650)
        self.set_language = 0

        self.doc_lang = open_setting()

        self.setWindowTitle(self.doc_lang['setting_window']['window_title'])
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(self.palette)

        self.center()
        self.init_setting_assembly()
        self.language_button_init()
        self.init_layout()

    # Set interface component initialization
    def init_setting_assembly(self):
        file_name = "config/eyeTrack.yaml"
        with open(file_name) as f:
            doc = yaml.safe_load(f)

        self.left_eye_setting_label = QLabel(self.doc_lang['setting_window']['left_eye_setting_label'], self)
        self.left_eye_setting_label.setStyleSheet("color:white")

        self.left_eye_fps_label = QLabel(self.doc_lang['setting_window']['fps_label'], self)
        self.left_eye_fps_label.setStyleSheet("color:white")
        self.left_eye_fps_set = QComboBox(self)
        self.left_eye_fps_set.resize(100, 100)
        self.left_eye_fps_set.addItem(str(self.doc_lang['setting_window']['left_eye_fps_215']), self)
        self.left_eye_fps_set.addItem(str(self.doc_lang['setting_window']['left_eye_fps_108']), self)

        self.left_eye_bright_label = QLabel(self.doc_lang['setting_window']['bright_label'], self)
        self.left_eye_bright_label.setStyleSheet("color:white")
        self.left_eye_bright_set = QSlider(Qt.Horizontal, self)
        self.left_eye_bright_set.setRange(0, 200)
        self.left_eye_bright_num = QLabel('0', self)
        self.left_eye_bright_num.setStyleSheet("color:white")
        self.left_eye_bright_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_bright_set))

        self.left_eye_contrast_label = QLabel(self.doc_lang['setting_window']['contrast_label'], self)
        self.left_eye_contrast_label.setStyleSheet("color:white")
        self.left_eye_contrast_set = QSlider(Qt.Horizontal, self)
        self.left_eye_contrast_set.setRange(0, 200)
        self.left_eye_contrast_num = QLabel('0', self)
        self.left_eye_contrast_num.setStyleSheet("color:white")
        self.left_eye_contrast_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_contrast_set))

        self.left_eye_saturation_label = QLabel(self.doc_lang['setting_window']['saturation_label'])
        self.left_eye_saturation_label.setStyleSheet("color:white")
        self.left_eye_saturation_set = QSlider(Qt.Horizontal, self)
        self.left_eye_saturation_set.setRange(0, 200)
        self.left_eye_saturation_num = QLabel('0', self)
        self.left_eye_saturation_num.setStyleSheet("color:white")
        self.left_eye_saturation_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_saturation_set))

        self.left_eye_sharpness_label = QLabel(self.doc_lang['setting_window']['sharpness_label'])
        self.left_eye_sharpness_label.setStyleSheet("color:white")
        self.left_eye_sharpness_set = QSlider(Qt.Horizontal, self)
        self.left_eye_sharpness_set.setRange(0, 200)
        self.left_eye_sharpness_num = QLabel('0', self)
        self.left_eye_sharpness_num.setStyleSheet("color:white")
        self.left_eye_sharpness_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_sharpness_set))

        self.left_eye_gain_label = QLabel(self.doc_lang['setting_window']['gain_label'], self)
        self.left_eye_gain_label.setStyleSheet("color:white")
        self.left_eye_gain_set = QSlider(Qt.Horizontal, self)
        self.left_eye_gain_set.setRange(0, 200)
        self.left_eye_gain_set.setValue(doc['devices']['cameras']['left_eye_capture']['gain'])
        self.left_eye_gain_num = QLabel('0', self)
        self.left_eye_gain_num.setStyleSheet("color:white")
        self.left_eye_gain_num.setText(str(self.left_eye_gain_set.value()))
        self.left_eye_gain_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_gain_set))

        self.right_eye_setting_label = QLabel(self.doc_lang['setting_window']['right_eye_setting_label'], self)
        self.right_eye_setting_label.setStyleSheet("color:white")

        self.right_eye_fps_label = QLabel(self.doc_lang['setting_window']['fps_label'], self)
        self.right_eye_fps_label.setStyleSheet("color:white")
        self.right_eye_fps_set = QComboBox(self)
        self.right_eye_fps_set.addItem(str(self.doc_lang['setting_window']['right_eye_fps_215']), self)
        self.right_eye_fps_set.addItem(str(self.doc_lang['setting_window']['right_eye_fps_108']), self)

        self.right_eye_bright_label = QLabel(self.doc_lang['setting_window']['bright_label'], self)
        self.right_eye_bright_label.setStyleSheet("color:white")
        self.right_eye_bright_set = QSlider(Qt.Horizontal, self)
        self.right_eye_bright_set.setRange(0, 200)
        self.right_eye_bright_num = QLabel('0', self)
        self.right_eye_bright_num.setStyleSheet("color:white")
        self.right_eye_bright_set.valueChanged.connect(lambda: self.on_change_func(self.right_eye_bright_set))

        self.right_eye_contrast_label = QLabel(self.doc_lang['setting_window']['contrast_label'], self)
        self.right_eye_contrast_label.setStyleSheet("color:white")
        self.right_eye_contrast_set = QSlider(Qt.Horizontal, self)
        self.right_eye_contrast_set.setRange(0, 200)
        self.right_eye_contrast_num = QLabel('0', self)
        self.right_eye_contrast_num.setStyleSheet("color:white")
        self.right_eye_contrast_set.valueChanged.connect(lambda: self.on_change_func(self.right_eye_contrast_set))

        self.right_eye_saturation_label = QLabel(self.doc_lang['setting_window']['saturation_label'])
        self.right_eye_saturation_label.setStyleSheet("color:white")
        self.right_eye_saturation_set = QSlider(Qt.Horizontal, self)
        self.right_eye_saturation_set.setRange(0, 200)
        self.right_eye_saturation_num = QLabel('0', self)
        self.right_eye_saturation_num.setStyleSheet("color:white")
        self.right_eye_saturation_set.valueChanged.connect(lambda: self.on_change_func(self.right_eye_saturation_set))

        self.right_eye_sharpness_label = QLabel(self.doc_lang['setting_window']['sharpness_label'])
        self.right_eye_sharpness_label.setStyleSheet("color:white")
        self.right_eye_sharpness_set = QSlider(Qt.Horizontal, self)
        self.right_eye_sharpness_set.setRange(0, 200)
        self.right_eye_sharpness_num = QLabel('0', self)
        self.right_eye_sharpness_num.setStyleSheet("color:white")
        self.right_eye_sharpness_set.valueChanged.connect(lambda: self.on_change_func(self.right_eye_sharpness_set))

        self.right_eye_gain_label = QLabel(self.doc_lang['setting_window']['gain_label'], self)
        self.right_eye_gain_label.setStyleSheet("color:white")
        self.right_eye_gain_set = QSlider(Qt.Horizontal, self)
        self.right_eye_gain_set.setRange(0, 200)
        self.right_eye_gain_set.setValue(doc['devices']['cameras']['right_eye_capture']['gain'])
        self.right_eye_gain_num = QLabel('0', self)
        self.right_eye_gain_num.setStyleSheet("color:white")
        self.right_eye_gain_num.setText(str(self.right_eye_gain_set.value()))
        self.right_eye_gain_set.valueChanged.connect(lambda: self.on_change_func(self.right_eye_gain_set))

        self.face_setting_label = QLabel(self.doc_lang['setting_window']['face_setting_label'], self)
        self.face_setting_label.setStyleSheet("color:white")

        self.face_bright_label = QLabel(self.doc_lang['setting_window']['bright_label'], self)
        self.face_bright_label.setStyleSheet("color:white")
        self.face_bright_set = QSlider(Qt.Horizontal, self)
        self.face_bright_set.setRange(0, 200)
        self.face_bright_num = QLabel('0', self)
        self.face_bright_num.setStyleSheet("color:white")
        self.face_bright_set.valueChanged.connect(lambda: self.on_change_func(self.face_bright_set))

        self.face_contrast_label = QLabel(self.doc_lang['setting_window']['contrast_label'], self)
        self.face_contrast_label.setStyleSheet("color:white")
        self.face_contrast_set = QSlider(Qt.Horizontal, self)
        self.face_contrast_set.setRange(0, 200)
        self.face_contrast_num = QLabel('0', self)
        self.face_contrast_num.setStyleSheet("color:white")
        self.face_contrast_set.valueChanged.connect(lambda: self.on_change_func(self.face_contrast_set))

        self.face_saturation_label = QLabel(self.doc_lang['setting_window']['saturation_label'])
        self.face_saturation_label.setStyleSheet("color:white")
        self.face_saturation_set = QSlider(Qt.Horizontal, self)
        self.face_saturation_set.setRange(0, 200)
        self.face_saturation_num = QLabel('0', self)
        self.face_saturation_num.setStyleSheet("color:white")
        self.face_saturation_set.valueChanged.connect(lambda: self.on_change_func(self.face_saturation_set))

        self.face_sharpness_label = QLabel(self.doc_lang['setting_window']['sharpness_label'])
        self.face_sharpness_label.setStyleSheet("color:white")
        self.face_sharpness_set = QSlider(Qt.Horizontal, self)
        self.face_sharpness_set.setRange(0, 200)
        self.face_sharpness_num = QLabel('0', self)
        self.face_sharpness_num.setStyleSheet("color:white")
        self.face_sharpness_set.valueChanged.connect(lambda: self.on_change_func(self.face_sharpness_set))

        self.face_gain_label = QLabel(self.doc_lang['setting_window']['gain_label'], self)
        self.face_gain_label.setStyleSheet("color:white")
        self.face_gain_set = QSlider(Qt.Horizontal, self)
        self.face_gain_set.setRange(0, 200)
        self.face_gain_set.setValue(doc['devices']['cameras']['face_capture']['gain'])
        self.face_gain_num = QLabel('0', self)
        self.face_gain_num.setStyleSheet("color:white")
        self.face_gain_num.setText(str(self.face_gain_set.value()))
        self.face_gain_set.valueChanged.connect(lambda: self.on_change_func(self.face_gain_set))

        self.world_setting_label = QLabel(self.doc_lang['setting_window']['world_setting_label'], self)
        self.world_setting_label.setStyleSheet("color:white")

        self.world_bright_label = QLabel(self.doc_lang['setting_window']['bright_label'], self)
        self.world_bright_label.setStyleSheet("color:white")
        self.world_bright_set = QSlider(Qt.Horizontal, self)
        self.world_bright_set.setRange(0, 200)
        self.world_bright_num = QLabel('0', self)
        self.world_bright_num.setStyleSheet("color:white")
        self.world_bright_set.valueChanged.connect(lambda: self.on_change_func(self.world_bright_set))

        self.world_contrast_label = QLabel(self.doc_lang['setting_window']['contrast_label'], self)
        self.world_contrast_label.setStyleSheet("color:white")
        self.world_contrast_set = QSlider(Qt.Horizontal, self)
        self.world_contrast_set.setRange(0, 200)
        self.world_contrast_num = QLabel('0', self)
        self.world_contrast_num.setStyleSheet("color:white")
        self.world_contrast_set.valueChanged.connect(lambda: self.on_change_func(self.world_contrast_set))

        self.world_saturation_label = QLabel(self.doc_lang['setting_window']['saturation_label'])
        self.world_saturation_label.setStyleSheet("color:white")
        self.world_saturation_set = QSlider(Qt.Horizontal, self)
        self.world_saturation_set.setRange(0, 200)
        self.world_saturation_num = QLabel('0', self)
        self.world_saturation_num.setStyleSheet("color:white")
        self.world_saturation_set.valueChanged.connect(lambda: self.on_change_func(self.world_saturation_set))

        self.world_sharpness_label = QLabel(self.doc_lang['setting_window']['sharpness_label'])
        self.world_sharpness_label.setStyleSheet("color:white")
        self.world_sharpness_set = QSlider(Qt.Horizontal, self)
        self.world_sharpness_set.setRange(0, 200)
        self.world_sharpness_num = QLabel('0', self)
        self.world_sharpness_num.setStyleSheet("color:white")
        self.world_sharpness_set.valueChanged.connect(lambda: self.on_change_func(self.world_sharpness_set))

        self.world_gain_label = QLabel(self.doc_lang['setting_window']['gain_label'], self)
        self.world_gain_label.setStyleSheet("color:white")
        self.world_gain_set = QSlider(Qt.Horizontal, self)
        self.world_gain_set.setRange(0, 200)
        self.world_gain_set.setValue(doc['devices']['cameras']['world_capture']['gain'])
        self.world_gain_num = QLabel('0', self)
        self.world_gain_num.setStyleSheet("color:white")
        self.world_gain_num.setText(str(self.world_gain_set.value()))
        self.world_gain_set.valueChanged.connect(lambda: self.on_change_func(self.world_gain_set))

        self.annother_setting_label = QLabel(self.doc_lang['setting_window']['annother_setting_label'], self)
        self.annother_setting_label.setStyleSheet("color:white")

        self.language_label = QLabel(self.doc_lang['setting_window']['language_label'], self)
        self.language_label.setStyleSheet("color:white")
        self.chinese_button = QRadioButton('中文', self)
        self.chinese_button.setStyleSheet("color:white")
        self.english_button = QRadioButton('English', self)
        self.english_button.setStyleSheet("color:white")

        self.recovery_button = QPushButton(self.doc_lang['setting_window']['recovery_button'], self)
        self.save_button = QPushButton(self.doc_lang['setting_window']['save_button'], self)
        self.save_button.clicked.connect(self.save_setting)

    # Setting the position of interface components
    def init_layout(self):
        self.grid = QGridLayout()

        self.grid.addWidget(self.left_eye_setting_label, 0, 0)
        self.grid.addWidget(self.right_eye_setting_label, 0, 6)
        self.grid.addWidget(self.face_setting_label, 7, 0)
        self.grid.addWidget(self.world_setting_label, 7, 6)
        self.grid.addWidget(self.annother_setting_label, 14, 0)

        self.grid.addWidget(self.left_eye_fps_label, 1, 0)
        self.grid.addWidget(self.left_eye_fps_set, 1, 1, 1, 2)
        # self.grid.addWidget(self.left_eye_fps_num,1,3)

        self.grid.addWidget(self.left_eye_bright_label, 2, 0)
        self.grid.addWidget(self.left_eye_bright_set, 2, 1, 1, 2)
        self.grid.addWidget(self.left_eye_bright_num, 2, 3)

        self.grid.addWidget(self.left_eye_contrast_label, 3, 0)
        self.grid.addWidget(self.left_eye_contrast_set, 3, 1, 1, 2)
        self.grid.addWidget(self.left_eye_contrast_num, 3, 3)

        self.grid.addWidget(self.left_eye_saturation_label, 4, 0)
        self.grid.addWidget(self.left_eye_saturation_set, 4, 1, 1, 2)
        self.grid.addWidget(self.left_eye_saturation_num, 4, 3)

        self.grid.addWidget(self.left_eye_sharpness_label, 5, 0)
        self.grid.addWidget(self.left_eye_sharpness_set, 5, 1, 1, 2)
        self.grid.addWidget(self.left_eye_sharpness_num, 5, 3)

        self.grid.addWidget(self.left_eye_gain_label, 6, 0)
        self.grid.addWidget(self.left_eye_gain_set, 6, 1, 1, 2)
        self.grid.addWidget(self.left_eye_gain_num, 6, 3)

        self.grid.addWidget(self.right_eye_fps_label, 1, 6)
        self.grid.addWidget(self.right_eye_fps_set, 1, 7, 1, 2)
        # self.grid.addWidget(self.right_eye_fps_num,1,9)

        self.grid.addWidget(self.right_eye_bright_label, 2, 6)
        self.grid.addWidget(self.right_eye_bright_set, 2, 7, 1, 2)
        self.grid.addWidget(self.right_eye_bright_num, 2, 9)

        self.grid.addWidget(self.right_eye_contrast_label, 3, 6)
        self.grid.addWidget(self.right_eye_contrast_set, 3, 7, 1, 2)
        self.grid.addWidget(self.right_eye_contrast_num, 3, 9)

        self.grid.addWidget(self.right_eye_saturation_label, 4, 6)
        self.grid.addWidget(self.right_eye_saturation_set, 4, 7, 1, 2)
        self.grid.addWidget(self.right_eye_saturation_num, 4, 9)

        self.grid.addWidget(self.right_eye_sharpness_label, 5, 6)
        self.grid.addWidget(self.right_eye_sharpness_set, 5, 7, 1, 2)
        self.grid.addWidget(self.right_eye_sharpness_num, 5, 9)

        self.grid.addWidget(self.right_eye_gain_label, 6, 6)
        self.grid.addWidget(self.right_eye_gain_set, 6, 7, 1, 2)
        self.grid.addWidget(self.right_eye_gain_num, 6, 9)

        self.grid.addWidget(self.face_bright_label, 8, 0)
        self.grid.addWidget(self.face_bright_set, 8, 1, 1, 2)
        self.grid.addWidget(self.face_bright_num, 8, 3)

        self.grid.addWidget(self.face_contrast_label, 9, 0)
        self.grid.addWidget(self.face_contrast_set, 9, 1, 1, 2)
        self.grid.addWidget(self.face_contrast_num, 9, 3)

        self.grid.addWidget(self.face_saturation_label, 10, 0)
        self.grid.addWidget(self.face_saturation_set, 10, 1, 1, 2)
        self.grid.addWidget(self.face_saturation_num, 10, 3)

        self.grid.addWidget(self.face_sharpness_label, 11, 0)
        self.grid.addWidget(self.face_sharpness_set, 11, 1, 1, 2)
        self.grid.addWidget(self.face_sharpness_num, 11, 3)

        self.grid.addWidget(self.face_gain_label, 12, 0)
        self.grid.addWidget(self.face_gain_set, 12, 1, 1, 2)
        self.grid.addWidget(self.face_gain_num, 12, 3)

        self.grid.addWidget(self.world_bright_label, 8, 6)
        self.grid.addWidget(self.world_bright_set, 8, 7, 1, 2)
        self.grid.addWidget(self.world_bright_num, 8, 9)

        self.grid.addWidget(self.world_contrast_label, 9, 6)
        self.grid.addWidget(self.world_contrast_set, 9, 7, 1, 2)
        self.grid.addWidget(self.world_contrast_num, 9, 9)

        self.grid.addWidget(self.world_saturation_label, 10, 6)
        self.grid.addWidget(self.world_saturation_set, 10, 7, 1, 2)
        self.grid.addWidget(self.world_saturation_num, 10, 9)

        self.grid.addWidget(self.world_sharpness_label, 11, 6)
        self.grid.addWidget(self.world_sharpness_set, 11, 7, 1, 2)
        self.grid.addWidget(self.world_sharpness_num, 11, 9)

        self.grid.addWidget(self.world_gain_label, 12, 6)
        self.grid.addWidget(self.world_gain_set, 12, 7, 1, 2)
        self.grid.addWidget(self.world_gain_num, 12, 9)

        self.grid.addWidget(self.language_label, 14, 0)
        self.grid.addWidget(self.chinese_button, 14, 1, 1, 2)
        self.grid.addWidget(self.english_button, 14, 3, 1, 2)

        self.grid.addWidget(self.recovery_button, 17, 7, 1, 1)
        self.grid.addWidget(self.save_button, 17, 8, 1, 1)

        self.setLayout(self.grid)

    # Monitoring and numerical changes of various setting functions on the setting interface
    def on_change_func(self, slider):
        if slider == self.left_eye_bright_set:
            self.left_eye_bright_num.setText(str(self.left_eye_bright_set.value()))
        if slider == self.left_eye_contrast_set:
            self.left_eye_contrast_num.setText(str(self.left_eye_contrast_set.value()))
        if slider == self.left_eye_saturation_set:
            self.left_eye_saturation_num.setText(str(self.left_eye_saturation_set.value()))
        if slider == self.left_eye_sharpness_set:
            self.left_eye_sharpness_num.setText(str(self.left_eye_sharpness_set.value()))
        if slider == self.left_eye_gain_set:
            self.left_eye_gain_num.setText(str(self.left_eye_gain_set.value()))

        if slider == self.right_eye_bright_set:
            self.right_eye_bright_num.setText(str(self.right_eye_bright_set.value()))
        if slider == self.right_eye_contrast_set:
            self.right_eye_contrast_num.setText(str(self.right_eye_contrast_set.value()))
        if slider == self.right_eye_saturation_set:
            self.right_eye_saturation_num.setText(str(self.right_eye_saturation_set.value()))
        if slider == self.right_eye_sharpness_set:
            self.right_eye_sharpness_num.setText(str(self.right_eye_sharpness_set.value()))
        if slider == self.right_eye_gain_set:
            self.right_eye_gain_num.setText(str(self.right_eye_gain_set.value()))

        if slider == self.face_bright_set:
            self.face_bright_num.setText(str(self.face_bright_set.value()))
        if slider == self.face_contrast_set:
            self.face_contrast_num.setText(str(self.face_contrast_set.value()))
        if slider == self.face_saturation_set:
            self.face_saturation_num.setText(str(self.face_saturation_set.value()))
        if slider == self.face_sharpness_set:
            self.face_sharpness_num.setText(str(self.face_sharpness_set.value()))
        if slider == self.face_gain_set:
            self.face_gain_num.setText(str(self.face_gain_set.value()))

        if slider == self.world_bright_set:
            self.world_bright_num.setText(str(self.world_bright_set.value()))
        if slider == self.world_contrast_set:
            self.world_contrast_num.setText(str(self.world_contrast_set.value()))
        if slider == self.world_saturation_set:
            self.world_saturation_num.setText(str(self.world_saturation_set.value()))
        if slider == self.world_sharpness_set:
            self.world_sharpness_num.setText(str(self.world_sharpness_set.value()))
        if slider == self.world_gain_set:
            self.world_gain_num.setText(str(self.world_gain_set.value()))

    # Change language component initialization
    def language_button_init(self):
        self.chinese_button.setChecked(True)
        self.chinese_button.toggled.connect(self.change_language)

    def change_language(self):
        if self.chinese_button.isChecked():
            self.set_language = 0
        else:
            self.set_language = 1

    #  Save Settings
    def save_setting(self):
        file_name = "config/eyeTrack.yaml"
        with open(file_name) as f:
            doc = yaml.safe_load(f)
        doc['devices']['cameras']['left_eye_capture']['gain'] = self.left_eye_gain_set.value()
        doc['devices']['cameras']['right_eye_capture']['gain'] = self.right_eye_gain_set.value()
        doc['devices']['cameras']['world_capture']['gain'] = self.world_gain_set.value()
        doc['devices']['cameras']['face_capture']['gain'] = self.face_gain_set.value()
        # self.left_eye_fps_num.setText(str(self.left_eye_fps_set.value()))
        # self.left_eye_fps_set.valueChanged.connect(lambda: self.on_change_func(self.left_eye_fps_set))ain'] =self.face_gain_set.value()
        doc['devices']['cameras']['left_eye_capture']['fps'] = int(self.left_eye_fps_set.currentText())
        doc['devices']['cameras']['right_eye_capture']['fps'] = int(self.right_eye_fps_set.currentText())
        if int(self.left_eye_fps_set.currentText()) == 215:
            doc['devices']['cameras']['left_eye_capture']['camera_fps'] = 20
        else:
            doc['devices']['cameras']['left_eye_capture']['camera_fps'] = 10

        if int(self.right_eye_fps_set.currentText()) == 215:
            doc['devices']['cameras']['right_eye_capture']['camera_fps'] = 20
        else:
            doc['devices']['cameras']['right_eye_capture']['camera_fps'] = 10

            # doc['devices']['cameras']['world_capture']['camera_fps'] = self.world_fps_set.value()
        # doc['devices']['cameras']['face_capture']['camera_fps'] = self.face_fps_set.value()
        with open(file_name, 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)

        QMessageBox.about(self, "", self.doc_lang['setting_window']['QMessageBox'])
        f = open("config/language_setting.xml", 'w')
        f.write(str(self.set_language))

    # Define a function to center the window display
    def center(self):
        # Obtain screen coordinate system
        screen = QDesktopWidget().screenGeometry()
        # Obtain Window Coordinate System
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))


def open_setting():
    f = open("config/language_setting.xml", 'r')
    flag = f.read()
    if int(flag) == 0:
        file_name = "lang/lang_setting_cn.yaml"
    else:
        file_name = "lang/lang_setting_en.yaml"
    with open(file_name) as f:
        doc_lang = yaml.safe_load(f)
    return doc_lang
