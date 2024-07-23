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

import threading
import time

from process import Processing


# Save frame rate threads, multiple threads save simultaneously
class SaveFrame(threading.Thread):
    def __init__(self, capture, path):
        super().__init__()
        self.path = path
        self.time_output = None
        self.capture = capture
        self.num = 0
        self.date = []

    def run(self):
        while True:
            frame = self.capture.consumption()
            if isinstance(frame, bool):
                self.capture.record_release()
                # save Timestamp
                self.time_output = Processing.save_time('{}/{}.txt'.format(self.path,
                                                                           self.capture.device_info.name + 'UTC'),
                                                        self.date)
                break
            else:
                self.num += 1
                need = (self.num, time.time())
                self.date.append(need)
                # Write image frames to buffer
                self.capture.write_frame(frame)
