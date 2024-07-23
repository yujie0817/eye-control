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

import os

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow


# Components used to play stimulus paradigms
class ParadigmVideoDisplay(QMainWindow):
    def __init__(self, parent, desktop, config):
        super().__init__(parent)
        self.paradigm_video = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        # The widget for video playback output is defined above
        self.media_player.setVideoOutput(self.paradigm_video)
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(os.getcwd() + config['path']['paradigm_video_path'])))
        self.paradigm_video.setFullScreen(True)
        # Set the screen for playing videos
        self.paradigm_video.setGeometry(desktop.screenGeometry(1))
        self.media_player.mediaStatusChanged.connect(self.media_end_check)

    # Start playing paradigm
    def media_start(self):
        self.media_player.play()

    def media_stop(self):
        self.media_player.stop()

    # Paradigm End Check
    def media_end_check(self):
        if self.media_player.mediaStatus() == 7:
            self.parent().end_recoding_time()
