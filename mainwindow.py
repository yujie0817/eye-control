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
倒计时改了正计时
光流关闭
改一个屏幕校准
接受信号取三张图片计算注视点
添加了socket模块
添加了目标匹配（轨迹模块减少计算尚未添加）


"""
# import datetime
import os
import threading
import time
from multiprocessing import Process, Barrier, Value
from shutil import copyfile

import cv2
import numpy as np
import yaml
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox, QFrame
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from mmdet.apis import init_detector
from mmdet.utils import register_all_modules
from pupil_detectors import Detector2D
from pye3d.camera import CameraModel
from pye3d.detector_3d import Detector3D

import global_value
from communication import service_send
from control.above_info import above_window, info_window
from control.display_frame import DisplayFrame
from control.iris_detection import get_pupil
from control.pvd import ParadigmVideoDisplay
from control.setting import setting_window
from model.linear_model import predict, load_model_path
from process import Fixation_point
from process.calibration import Calibration
from process.record import CaptureFrame
from threadsync.save import SaveFrame
from utils import update_record_output, flag_change
# from ultralytics import YOLO


# The main interface of the program implements most basic functions
class MainWindow(QWidget):
    def __init__(self, config, devices, desktop):
        super().__init__()

        # Global Dictionary Initialization
        self.copy_path = None
        global_value._init()

        # Main page settings
        self.resize(*config['resolution_ratio']['mainwindow'])

        # Chinese and English file initialization
        self.doc_lang = main_open()
        self.flag = 0
        self.time = 0
        global_value.set_value("flag", False)

        # Initialization of camera files, configuration files, and some fields
        self._config = config
        self._devices = devices
        self._desktop = desktop
        self._uniform_timestamp = None
        self._barrier = Barrier(len(devices) + 1)
        self._recoding = Value('i', 0)
        self.calibrating = Value('i', 0)

        # Interface components and button initialization
        self.init_assembly()
        self.set_button()

        # Setting the interface and about interface initialization
        self.setting_page = setting_window()
        self.above_page = above_window()

        self.init_capture_display()
        self.init_paradigm_video_display()
        self.init_timestamp()

        # Button method initialization
        self.start_button.clicked.connect(self.start_recoding)
        # self.start_button.clicked.connect(self.get_locations)
        self.calibration_button.clicked.connect(self.start_calibration)
        self.above_button.clicked.connect(self.show_above_page)
        # self.handle_button.clicked.connect(self.start_handle)
        self.handle_button.clicked.connect(self.start_socket)
        self.stop_button.clicked.connect(self.end_recoding)
        self.setting_button.clicked.connect(self.show_setting_page)

        # Initialize the subject information input interface
        self.info_page = info_window()
        self.info_page.exec_()

        global_value._init()

    # Display settings interface
    def show_setting_page(self):
        self.setting_page.show()

    # About Interface Display
    def show_above_page(self):
        self.above_page.show()

    def start_handle(self):
        # Processing.sync(self.copy_path)
        Fixation_point.trans_left_video_to_picture(self.copy_path)
        Fixation_point.trans_right_video_to_picture(self.copy_path)
        Fixation_point.fixation_point(self.copy_path)

    # Calling calibration methods, click to perform calibration
    def start_calibration(self):
        # Calibration requires a new process to be called
        calibration = Calibration(9)
        calibration_process = Process(target=calibration.show, )
        calibration.show()

    # Initialization of interface components, setting the positions, images, and dimensions of each component
    def init_assembly(self):
        self.deep_label = QLabel('', self)
        self.pixmap_deep_carema_label = QPixmap("./img/1.jpg")
        self.deep_label.setPixmap(self.pixmap_deep_carema_label)
        self.deep_label.setScaledContents(True)
        self.deep_label.move(1330, 680)
        self.deep_label.resize(521, 300)

        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(self.palette)

        self.top_img = QLabel('', self)
        self.main_button = QPushButton('主页', self)
        self.setting_button = QPushButton('设置', self)
        self.above_button = QPushButton('关于', self)
        self.calibration_button = QPushButton('', self)
        self.start_button = QPushButton('', self)
        self.stop_button = QPushButton('', self)
        self.handle_button = QPushButton('', self)

        self.video_time = QTimer(self)
        self.video_time_label = QLabel("   录制计时器  ", self)
        self.video_time_label.setStyleSheet("color:white")
        self.video_time_label.setFont(QFont('', 12))
        self.video_time.timeout.connect(self.showTime)
        self.video_time_label.setFrameShape(QFrame.Box)
        self.video_time_label.setStyleSheet("color:white")
        self.video_time_label.resize(130, 25)
        # self.video_time_label.raise_()

        self.face_label = QLabel('', self)
        self.world_label = QLabel('', self)
        self.left_label = QLabel('', self)
        self.right_label = QLabel('', self)
        self.deep_label = QLabel('', self)

        self.top_img.setPixmap(QPixmap("./img/UAIS pupil.png"))
        self.top_img.setScaledContents(True)
        self.top_img.resize(150, 30)
        self.top_img.move(10, 20)

        self.main_button.move(20, 90)
        self.main_button.resize(200, 60)
        self.main_button.setStyleSheet(
            "border-width: 1px;border-style: solid;border-color: rgb(255, 255, 255);")
        self.setting_button.move(220, 90)
        self.setting_button.resize(200, 60)
        self.setting_button.setStyleSheet(
            "border-width: 1px;border-style: solid;border-color: rgb(255, 255, 255);")
        self.above_button.move(420, 90)
        self.above_button.resize(200, 60)
        self.above_button.setStyleSheet(
            "border-width: 1px;border-style: solid;border-color: rgb(255, 255, 255);")

        self.calibration_button.move(1300, 95)
        self.calibration_button.resize(50, 50)
        self.start_button.move(1400, 95)
        self.start_button.resize(50, 50)
        self.stop_button.move(1500, 95)
        self.stop_button.resize(50, 50)
        self.video_time_label.move(1570, 110)
        self.handle_button.move(1750, 95)
        self.handle_button.resize(50, 50)

        self.world_name_label = QLabel('全景摄像头', self)
        self.world_name_label.move(20, 180)
        self.world_name_label.raise_()
        self.world_name_label.setStyleSheet("background:transparent")

        self.face_name_label = QLabel('表情摄像头', self)
        self.face_name_label.move(1330, 373)
        self.face_name_label.raise_()
        self.face_name_label.setStyleSheet("background:transparent")

        self.left_name_label = QLabel('左眼摄像头', self)
        self.left_name_label.move(1330, 180)
        self.left_name_label.raise_()
        self.left_name_label.setStyleSheet("background:transparent")

        self.right_name_label = QLabel('右眼摄像头', self)
        self.right_name_label.move(1595, 180)
        self.right_name_label.raise_()
        self.right_name_label.setStyleSheet("background:transparent")

    # Stimulation paradigm playback countdown display
    def showTime(self):
        cap = cv2.VideoCapture('./normal_form/test.mp4')
        # if cap.isOpened():
        #     rate = cap.get(5)
        #     frame_num = cap.get(7)
        #     duration = int(frame_num / rate) * 100 / 100
        self.time = self.time + 1
        self.video_time_label.setText("已录制：" + str(self.time) + "秒")

    # Set the size, position, and background image of the button
    def set_button(self):
        self.main_button.setFont(QFont('', 20))
        self.setting_button.setFont(QFont('', 20))
        self.above_button.setFont(QFont('', 20))

        self.calibration_button.setFlat(True)
        self.calibration_button.setIcon(QIcon("./img/校准.png"))
        self.calibration_button.setIconSize(QtCore.QSize(50, 50))

        self.start_button.setFlat(True)
        self.start_button.setIcon(QIcon("./img/录制.png"))
        self.start_button.setIconSize(QtCore.QSize(50, 50))

        self.handle_button.setFlat(True)
        self.handle_button.setIcon(QIcon("./img/后期处理.png"))
        self.handle_button.setIconSize(QtCore.QSize(50, 50))

        self.stop_button.setFlat(True)
        self.stop_button.setIcon(QIcon("./img/record1.png"))
        self.stop_button.setIconSize(QtCore.QSize(50, 50))

        self.calibration_button.setStyleSheet("border:none;border-radius:25px;")
        self.start_button.setStyleSheet("border:none;border-radius:25px;")
        self.stop_button.setStyleSheet("border:none;border-radius:25px;")
        self.handle_button.setStyleSheet("border:none;border-radius:25px;")

    # Initialization timestamp
    def init_timestamp(self):
        now = int(round(time.time() * 1000))
        self.uniform_timestamp = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(now / 1000))

    # Start the camera acquisition and display thread
    def init_capture_display(self):
        [setattr(self, device['name'], DisplayFrame(self, device, self._config)) for device in self._devices]
        timer_capture = QTimer(self)
        timer_capture.start(1000 // self._config['display_fps'])
        timer_capture.timeout.connect(self.update_capture_display)

    # start socket with Android
    def start_socket(self):
        # gaze = get_locations()
        pth = '/home/uais/桌面/objectNET/mmdetection/configs/'
        config_file = pth + 'rtmdet/rtmdet_tiny_8xb32-300e_coco.py'
        checkpoint_file = './detmodels/rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth'
        register_all_modules()
        model = init_detector(config_file, checkpoint_file, device='cpu')  # or device='cuda:0'
        # model = YOLO('yolov8n.pt')
        socket_thread = threading.Thread(target=service_send.receive_and_send, args=(1, model))
        socket_thread.start()

    # Update camera display
    def update_capture_display(self):
        [getattr(self, device['name']).update_frame(self._recoding) for device in self._devices]
        img_face = global_value.get_value("face")
        cv2.imwrite("./img/3.jpg", img_face)
        first = cv2.imread("./img/2.jpg")
        second = cv2.imread("./img/3.jpg")
        pre = cv2.resize(first, (384, 216))
        nex = cv2.resize(second, (384, 216))
        face_dense_img = face_dense(pre, nex)
        cv2.imwrite("./img/4.jpg", face_dense_img)
        self.pixmap_deep_carema_label = QPixmap("./img/4.jpg")
        self.deep_label.setPixmap(self.pixmap_deep_carema_label)
        self.deep_label.setScaledContents(True)
        self.deep_label.move(1330, 680)
        self.deep_label.resize(521, 300)
        cv2.imwrite("./img/2.jpg", img_face)

    def init_paradigm_video_display(self):
        self.video_show_window = ParadigmVideoDisplay(self, self._desktop, self._config)

    # Start data collection
    def start_recoding(self):
        if global_value.get_value("flag") == True:
            save_doc = save_open()
            self.video_time.start(1000)
            self.start_button.setIcon(QIcon("./img/Suspend.png"))
            self.start_button.setIconSize(QtCore.QSize(85, 85))
            self.start_button.setEnabled(False)

            record_save_path = self._config['path']['record_save_path']
            save_path = save_doc['id'] + '_' + self.uniform_timestamp
            if not os.path.exists('{}/{}'.format(record_save_path, save_path)):
                os.makedirs('{}/{}'.format(record_save_path, save_path))
            self._devices.collective_operation(update_record_output, record_save_path, save_path)

            copy_path = record_save_path + '/' + save_path
            copyfile("config/info.yaml", copy_path + '/' + 'info.yaml')
            # copy models
            additional_files = ["model/eye0.model", "model/eye1.model", "model/lefteye_x.model",
                                "model/lefteye_y.model", "model/righteye_x.model",
                                "model/righteye_y.model"]
            for file_path in additional_files:
                copyfile(file_path, copy_path + '/' + os.path.basename(file_path))

            flag_change(self._recoding)
            [CaptureFrame(device, barrier=self._barrier, get_flag=self._recoding).start() for device in self._devices]
            self._barrier.wait()
            self.video_show_window.media_start()
            [SaveFrame(device, copy_path).start() for device in self._devices]
            self.start_button.setEnabled(True)
            self.copy_path = copy_path
        else:
            self.msgBox = QMessageBox.information(self, "提示", "请先进行校准", QMessageBox.Yes)

    # stop recording
    def end_recoding(self):
        self.start_button.setIcon(QIcon("./img/录制.png"))
        self.start_button.setIconSize(QtCore.QSize(50, 50))
        self.video_show_window.media_stop()
        self.video_time.stop()
        self.time = 0
        flag_change(self._recoding)
        self.init_timestamp()

    def end_recoding_time(self):
        self.start_button.setIcon(QIcon("./img/录制.png"))
        self.start_button.setIconSize(QtCore.QSize(50, 50))
        self.video_show_window.media_stop()
        self.video_time.stop()
        self.time = 0
        flag_change(self._recoding)
        self.init_timestamp()

    # Selection event after closing the program
    def closeEvent(self, event):
        f = open("./config/log.xml", 'w').close()
        reply = QMessageBox.question(self, self.doc_lang['main_window']['wrning'],
                                     self.doc_lang['main_window']['leave'], QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()  # close window
        else:
            event.ignore()  # Ignore click on X event


def main_open():
    f = open("config/language_setting.xml", 'r')
    flag = f.read()
    if int(flag) == 0:
        file_name = "lang/lang_cn.yaml"
    else:
        file_name = "lang/lang_en.yaml"
    with open(file_name) as f:
        doc_lang = yaml.safe_load(f)
    return doc_lang


def save_open():
    file_name = "./config/info.yaml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)
    return doc


def face_dense(pre, nex):
    # 流光法初始化
    # cap = cv2.VideoCapture(path+"/face_capture.mkv")
    frame_dense = pre
    prvs = cv2.cvtColor(frame_dense, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame_dense)
    hsv[..., 1] = 255
    frame = nex
    next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    prvs = next
    # cv2.imshow("1.jpg", bgr)
    return bgr

# get gaze point
def get_locations():
    img_world = global_value.get_value("world")
    img_right = global_value.get_value("right")
    img_left = global_value.get_value("left")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = f"coordinate/{timestamp}"
    os.makedirs(path)
    # print(path)
    cv2.imwrite(f"{path}/world.jpg", img_world)
    cv2.imwrite(f"{path}/right.jpg", img_right)
    cv2.imwrite(f"{path}/left.jpg", img_left)
    regr_right_x, regr_right_y, regr_left_x, regr_left_y = load_model_path("./model")
    model_2d = Detector2D()
    model_3d = Detector3D(CameraModel(focal_length=100, resolution=(320, 240)))
    img_left, left_eye_x, left_eye_y, area = get_pupil(img_left, model_2d, model_3d)
    img_right, right_eye_x, right_eye_y, area = get_pupil(img_right, model_2d, model_3d)
    gaze = predict([right_eye_x, right_eye_y, right_eye_x ** 2, right_eye_y ** 2],
                   [left_eye_x, left_eye_y, left_eye_x ** 2, left_eye_y ** 2],
                   regr_right_x, regr_right_y, regr_left_x, regr_left_y)
    # print(gaze)
    return gaze