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

# Reading cameras and some commonly used tools
import os
import re

import cv2
import yaml


# Obtain Camera Path
class CameraConfig:
    def __init__(self, config):
        for att in config:
            setattr(self, att, config[att])
        self.device_path = None

    def set_path(self, new_path):
        self.device_path = new_path
        return True


# Obtain configuration files and information
def get_config(config):
    with open(config, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


# Using v4l2 to obtain camera information
def get_camera_info(config):
    # Use v4l2 to read the name of the camera and traverse to obtain the camera path
    cameras_info = os.popen('v4l2-ctl --list-devices').read()
    cameras_config = config['devices']['cameras']
    for camera_info in [camera_info for camera_info in cameras_info.split('\n\n') if camera_info]:
        v4l2_name = get_v4l2_name(camera_info)
        camera_path = get_camera_path(camera_info)
        for camera_name in cameras_config:
            if cameras_config[camera_name]['v4l2_name'] in v4l2_name:
                camera_config = CameraConfig(cameras_config[camera_name])
                camera_config.set_path(camera_path)
                yield camera_config


# Using Regular Expressions to Obtain Camera Path Names
def get_v4l2_name(camera_info):
    name = re.findall(r'^([^(:]+)', camera_info)[0].replace("—", "_")
    name = name.replace("—", "_")
    return name


# Since v4l2 reads cameras arranged according to/dev/video [0-9], we can traverse these paths to obtain camera information
def get_camera_path(camera_info):
    path = re.findall('/dev/video[0-9]+', camera_info)[0]
    return path


def flag_change(flag):
    with flag.get_lock():
        flag.value = 1 - flag.value


def update_record_output(device, new_path, new_timestamp):
    """
    Change the recording save path after recording ends
    :param new_record_output: new VideoWriter
    """
    device._record_output = cv2.VideoWriter('{}/{}/{}.mp4'.format(new_path, new_timestamp, device['name']),
                                            cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), device['fps'],
                                            (int(device.get('width')), int(device.get('height'))))
    return True


def above_info_open():
    file_name = "./config/info.yaml"
    with open(file_name) as f:
        doc = yaml.safe_load(f)
    return doc
