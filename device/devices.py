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

from device.camera import Camera


# Device information reading
class Devices:
    def __init__(self):
        self._device_library = {}

    def append(self, device_info):
        device = Camera(device_info)
        self._device_library[device_info.name] = device

    def __iter__(self):
        return iter(self._device_library.values())

    def collective_operation(self, function, *extra_parameters):
        if extra_parameters:
            [function(device, *extra_parameters) for device in self]
        else:
            [function(device) for device in self]

    def __len__(self):
        return len(self._device_library)

    def __getitem__(self, item):
        return self._device_library[item]
