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

from multiprocessing import Manager

import cv2
import yaml


# Camera configuration file, which can set camera parameters and read/write image modes
class Camera:
    def __init__(self, device_info):
        self.time_output = None
        self._device = None
        self._record_output = None
        self.manager = Manager()
        self._acquisition_buffer = self.manager.Queue()
        self._display_cache = self.manager.Queue()
        self.device_info = device_info
        """
            Camera parameter settings, including brightness, contrast, image enhancement, and camera's fps
            These configurations can be changed in the configuration file
            Add relevant fields to the configuration file to make changes
        """
        self._attribute_collection = {'time': cv2.CAP_PROP_POS_MSEC,
                                      'height': cv2.CAP_PROP_FRAME_HEIGHT,
                                      'width': cv2.CAP_PROP_FRAME_WIDTH,
                                      'brightness': cv2.CAP_PROP_BRIGHTNESS,
                                      'contrast': cv2.CAP_PROP_CONTRAST,
                                      'saturation': cv2.CAP_PROP_SATURATION,
                                      'sharpness': cv2.CAP_PROP_SHARPNESS,
                                      'gain': cv2.CAP_PROP_GAIN,
                                      'camera_fps': cv2.CAP_PROP_FPS,
                                      }
        self.init_device(device_info)

    # Camera parameter initialization, setting some basic parameters
    def init_device(self, device_info):
        self._device = cv2.VideoCapture(device_info.device_path)
        self.set('height', device_info.frame_height)
        self.set('width', device_info.frame_width)
        self.set('gain', device_info.gain)
        self.set('camera_fps', device_info.camera_fps)
        # self._device.set(cv2.CAP_PROP_AUTO_WB, 1)
        self._device.set(cv2.CAP_PROP_EXPOSURE, 166)
        # self._device.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        self._device.set(cv2.CAP_PROP_BRIGHTNESS, device_info.brightness)
        self._device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        return True

    @property
    def current_frame(self):
        flag, _last_frame = self._device.read()
        if self._display_cache.empty():
            self._display_cache.put(_last_frame)
        return _last_frame

    @property
    def display_frame(self):
        return self._display_cache.get()

    def update_record_output(self, path, new_timestamp):
        self._record_output = cv2.VideoWriter('{}/{}/{}.mp4'.format(path, new_timestamp, self.device_info.name),
                                              cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), self.device_info.fps,
                                              (self.device_info.frame_width, self.device_info.frame_height))
        # self.time_output = Processing.save_time('{}/{}/{}.txt'.format(path, new_timestamp, self._device_info.name), date)
        return True

    def get_name(self):
        return self.device_info.name

    def record_release(self):
        self._record_output.release()
        return True

    def write_frame(self, frame):
        self._record_output.write(frame)
        return True

    def produce(self, product):
        self._acquisition_buffer.put(product)
        return True

    def consumption(self):
        return self._acquisition_buffer.get()

    def set(self, target, new_value):
        self._device.set(self._attribute_collection[target], new_value)
        return True

    def get(self, target):
        return self._device.get(self._attribute_collection[target])

    def __getitem__(self, item):
        return eval('self.device_info.{}'.format(item))


def above_info_open(self):
    file_name = "config/info.yaml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)
    return doc
