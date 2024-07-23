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
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QDesktopWidget, QComboBox


# Regarding interface design, including content and component design
class above_window(QWidget):
    def __init__(self):
        super(above_window, self).__init__()
        self.resize(400, 250)

        self.doc_lang, self.flag = above_info_open()

        self.setWindowTitle(self.doc_lang['above_info_window']['above_window_title'])

        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(self.palette)

        self.center()
        self.init_above_assembly()

    # Interface component initialization
    def init_above_assembly(self):
        self.above_label = QLabel(self.doc_lang['above_info_window']['above_label'], self)
        self.above_label.move(100, 50)
        self.above_label.setStyleSheet("color:white")

        self.copyright = QLabel(self.doc_lang['above_info_window']['copyright'], self)
        self.copyright.move(110, 115)
        self.copyright.setFont(QFont("", 12))
        self.copyright.setStyleSheet("color:white")

        self.copyright_label = QLabel(self.doc_lang['above_info_window']['copyright_label'], self)
        self.copyright_label.move(200, 120)
        self.copyright_label.setFont(QFont("", 12))
        self.copyright_label.setStyleSheet("color:white")

        self.Hardware = QLabel(self.doc_lang['above_info_window']['hardware'], self)
        self.Hardware.move(110, 140)
        self.Hardware.setFont(QFont("", 12))
        self.Hardware.setStyleSheet("color:white")

        self.Hardware_label = QLabel(self.doc_lang['above_info_window']['hardware_label'], self)
        self.Hardware_label.move(200, 145)
        self.Hardware_label.setFont(QFont("", 12))
        self.Hardware_label.setStyleSheet("color:white")

        self.software = QLabel(self.doc_lang['above_info_window']['software'], self)
        self.software.move(110, 160)
        self.software.setFont(QFont("", 12))
        self.software.setStyleSheet("color:white")

        self.software_label = QLabel(self.doc_lang['above_info_window']['software_label'], self)
        self.software_label.move(200, 165)
        self.software_label.setFont(QFont("", 12))
        self.software_label.setStyleSheet("color:white")

        self.website = QLabel(self.doc_lang['above_info_window']['website'], self)
        self.website.move(110, 180)
        self.website.setFont(QFont("", 12))
        self.website.setStyleSheet("color:white")

        self.website_label = QLabel(self.doc_lang['above_info_window']['website_label'], self)
        self.website_label.move(200, 185)
        self.website_label.setFont(QFont("", 12))
        self.website_label.setStyleSheet("color:white")

        if int(self.flag) == 0:
            self.above_label.setFont(QFont("Roman times", 20, QFont.Bold))
            print(self.flag)
        else:
            self.above_label.setFont(QFont("Roman times", 15, QFont.Bold))
            self.copyright.move(110, 120)
            self.above_label.move(75, 50)

    # Define a function to center the window display
    def center(self):
        # Obtain screen coordinate system
        screen = QDesktopWidget().screenGeometry()
        # Obtain Window Coordinate System
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))


# Record subject information interface
class info_window(QDialog):
    def __init__(self):
        super(info_window, self).__init__()
        self.resize(500, 400)

        self.doc_lang, self.flag = above_info_open()

        self.setWindowTitle(self.doc_lang['above_info_window']['info_window_title'])

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(self.palette)

        self.init_info_assembly()
        self.init_info_layout()

        self.center()

    # Interface component initialization
    def init_info_assembly(self):
        self.first_label = QLabel(self.doc_lang['above_info_window']['first_label'], self)
        self.first_label.setFont(QFont('', 20))
        self.first_label.setStyleSheet("color:white")

        self.id_label = QLabel(self.doc_lang['above_info_window']['id_label'], self)
        self.id_label.setStyleSheet("color:white")
        self.id_label.setFont(QFont('', 15))
        self.id_edit = QLineEdit(self)
        self.id_edit.resize(200, 30)
        self.id_edit.setPlaceholderText(self.doc_lang['above_info_window']['id_edit'])

        self.name_label = QLabel(self.doc_lang['above_info_window']['name_label'], self)
        self.name_label.setStyleSheet("color:white")
        self.name_label.setFont(QFont('', 15))
        self.name_edit = QLineEdit(self)
        self.name_edit.resize(200, 30)
        self.name_edit.setPlaceholderText(self.doc_lang['above_info_window']['name_edit'])

        self.type_label = QLabel(self.doc_lang['above_info_window']['type_label'], self)
        self.type_label.setStyleSheet("color:white")
        self.type_label.setFont(QFont('', 15))
        self.type_edit = QComboBox(self)
        self.type_edit.resize(200, 30)
        self.type_edit.addItem(self.doc_lang['above_info_window']['type_he'], self)
        self.type_edit.addItem(self.doc_lang['above_info_window']['type_de'], self)

        self.gender_label = QLabel(self.doc_lang['above_info_window']['gender_label'], self)
        self.gender_label.setStyleSheet("color:white")
        self.gender_label.setFont(QFont('', 15))
        self.gender_edit = QComboBox(self)
        self.gender_edit.resize(200, 30)
        self.gender_edit.addItem(self.doc_lang['above_info_window']['gender_male'], self)
        self.gender_edit.addItem(self.doc_lang['above_info_window']['gender_female'], self)

        self.main_name_label = QLabel(self.doc_lang['above_info_window']['main_name_label'], self)
        self.main_name_label.setStyleSheet("color:white")
        self.main_name_label.setFont(QFont('', 15))
        self.main_name_edit = QLineEdit(self)
        self.main_name_edit.resize(200, 30)
        self.main_name_edit.setPlaceholderText(self.doc_lang['above_info_window']['main_name_edit'])

        self.save_button = QPushButton(self.doc_lang['above_info_window']['save_button'], self)
        self.save_button.clicked.connect(self.save_info)
        self.save_button.setStyleSheet("color:white")
        self.save_button.setFlat(True)

    # Component position setting
    def init_info_layout(self):
        self.first_label.move(100, 20)

        self.id_label.move(100, 100)
        self.id_edit.move(200, 100)

        self.name_label.move(100, 140)
        self.name_edit.move(200, 140)

        self.type_label.move(100, 180)
        self.type_edit.move(200, 180)

        self.gender_label.move(100, 220)
        self.gender_edit.move(200, 220)

        self.main_name_label.move(100, 260)
        self.main_name_edit.move(200, 260)

        self.save_button.move(350, 350)

    # Save subject information
    def save_info(self):
        file_name = "config/info.yaml"
        with open(file_name) as f:
            doc = yaml.safe_load(f)
        doc['id'] = self.id_edit.text()
        doc['name'] = self.name_edit.text()
        doc['type'] = self.type_edit.currentText()
        doc['gender'] = self.gender_edit.currentText()
        doc['main_name'] = self.main_name_edit.text()
        with open(file_name, 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False, allow_unicode=True)

        QMessageBox.about(self, "", self.doc_lang['above_info_window']['QMessageBox'])

        self.close()

    # Define a function to center the window display
    def center(self):
        # Obtain screen coordinate system
        screen = QDesktopWidget().screenGeometry()
        # Obtain Window Coordinate System
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))


# Open a Chinese English translation file
def above_info_open():
    f = open("config/language_setting.xml", 'r')
    flag = f.read()
    if int(flag) == 0:
        file_name = "lang/lang_above_info_cn.yaml"
    else:
        file_name = "lang/lang_above_info_en.yaml"
    with open(file_name) as f:
        doc_lang = yaml.safe_load(f)
    return doc_lang, flag
