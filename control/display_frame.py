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

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QFrame
from pupil_detectors import Detector2D
from pye3d.camera import CameraModel
from pye3d.detector_3d import Detector3D

import global_value
from control.iris_detection import get_gaze, get_pupil
from model.is_fixing import is_fixing
from model.linear_model import load_model, predict


# Display and record camera images
class DisplayFrame(QLabel):
    def __init__(self, parent, capture, config):
        super().__init__(parent)
        self.capture = capture
        self.setScaledContents(True)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet(
            "border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 149, 237);")
        self.lower()

        self.move(*config['location'][capture['name'] + '_display_frame'])
        self.resize(*config['resolution_ratio'][capture['name'] + '_display_frame'])

        self.x0 = 0
        self.y0 = 0
        self.isFixing = False

        self.regr_right_x, self.regr_right_y, self.regr_left_x, self.regr_left_y = load_model()
        self.gaze = (0, 0)
        global_value.set_value("calibated", False)
        self.model_2d = Detector2D()
        self.model_3d = Detector3D(CameraModel(focal_length=100, resolution=(320, 240)))

    # Process each frame
    def update_frame(self, flag):
        if not flag.value:
            frame = self.capture.current_frame
        else:
            frame = self.capture.display_frame
        try:
            # Distinguish which camera the image comes from based on the camera name and perform corresponding processing
            if self.capture['name'] == "left_eye_capture":
                # Obtain pupillary position information
                frame, eye_x, eye_y, area = get_pupil(frame, self.model_2d, self.model_3d)
                # Correcting data
                isFixing = is_fixing(self.x0, eye_x, self.y0, eye_y, threshold=50)
                self.x0 = eye_x
                self.y0 = eye_y
                # Pass data into the global dictionary
                global_value.set_value("isFixing_left", isFixing)
                global_value.set_value("left_eye_x", eye_x)
                global_value.set_value("left_eye_y", eye_y)

            if self.capture['name'] == "right_eye_capture":
                # Obtain pupillary position information
                frame, eye_x, eye_y, area = get_pupil(frame, self.model_2d, self.model_3d)
                # Correcting data
                isFixing = is_fixing(self.x0, eye_x, self.y0, eye_y, threshold=50)
                self.x0 = eye_x
                self.y0 = eye_y
                # Pass data into the global dictionary
                global_value.set_value("isFixing_right", isFixing)
                global_value.set_value("right_eye_x", eye_x)
                global_value.set_value("right_eye_y", eye_y)

            if self.capture['name'] == "face_capture":
                global_value.set_value("face", frame)
            if self.capture['name'] == "world_capture":
                global_value.set_value("world", frame)
            if self.capture['name'] == "left_eye_capture":
                global_value.set_value("left", frame)
            if self.capture['name'] == "right_eye_capture":
                global_value.set_value("right", frame)

            if self.capture['name'] == "world_capture":
                frame, gaze_x, gaze_y, gaze_r = get_gaze(frame)
                if gaze_x == 0:
                    gaze_x = self.x0
                    gaze_y = self.y0
                isFixing = is_fixing(self.x0, gaze_x, self.y0, gaze_y, threshold=250)
                self.x0 = gaze_x
                self.y0 = gaze_y
                # Obtain calibrated data
                global_value.set_value("isFixing_gaze", isFixing)
                global_value.set_value("gaze_x", gaze_x)
                global_value.set_value("gaze_y", gaze_y)
                right_eye_x = global_value.get_value("right_eye_x")
                right_eye_y = global_value.get_value("right_eye_y")
                left_eye_x = global_value.get_value("left_eye_x")
                left_eye_y = global_value.get_value("left_eye_y")
                # Using linear regression for gaze prediction and generating predicted data
                if global_value.get_value("calibated"):
                    self.regr_right_x, self.regr_right_y, self.regr_left_x, self.regr_left_y = load_model()
                    if left_eye_x != 0 and left_eye_y != 0 and right_eye_x != 0 and right_eye_y != 0:
                        gaze = predict([right_eye_x, right_eye_y, right_eye_x ** 2, right_eye_y ** 2],
                                       [left_eye_x, left_eye_y, left_eye_x ** 2, left_eye_y ** 2],
                                       self.regr_right_x, self.regr_right_y, self.regr_left_x, self.regr_left_y)
                        self.gaze = gaze
                    frame = cv2.circle(frame, self.gaze, 20, (0, 255, 0), 3)
            # Draw gaze points in the panoramic camera
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            self.setPixmap(QPixmap.fromImage(image))
        # If there is a problem with the camera, throw an exception
        except:
            print('err')
