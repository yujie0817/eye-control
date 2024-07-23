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

import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication
from device.devices import Devices
from mainwindow import MainWindow
from utils import get_config, get_camera_info

"""
This is the main file of the program and also the startup entry point of the program
"""
if __name__ == '__main__':
    try:
        # load profile
        config = get_config('config/eyeTrack.yaml')
        # Obtain camera information\
        cameras_info = get_camera_info(config)
        devices = Devices()
        [devices.append(camera_info) for camera_info in cameras_info]
    except:
        sys.exit()

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # or in new API
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    desktop = app.desktop()
    main_window = MainWindow(config, devices, desktop)
    main_window.show()
    sys.exit(app.exec_())
