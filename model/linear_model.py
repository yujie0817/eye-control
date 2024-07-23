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

import joblib
from sklearn import linear_model


# Obtain fixation point prediction model
def get_model(data_right, data_left, gaze_x, gaze_y):
    regr_right_x = linear_model.LinearRegression()
    regr_right_x.fit(data_right, gaze_x)
    joblib.dump(regr_right_x, 'model/righteye_x.model')

    regr_right_y = linear_model.LinearRegression()
    regr_right_y.fit(data_right, gaze_y)
    joblib.dump(regr_right_y, 'model/righteye_y.model')

    regr_left_x = linear_model.LinearRegression()
    regr_left_x.fit(data_left, gaze_x)
    joblib.dump(regr_left_x, 'model/lefteye_x.model')

    regr_left_y = linear_model.LinearRegression()
    regr_left_y.fit(data_left, gaze_y)
    joblib.dump(regr_left_y, 'model/lefteye_y.model')


# Loading fixation point prediction model
def load_model():
    regr_right_x = joblib.load("model/righteye_x.model")
    regr_right_y = joblib.load("model/righteye_y.model")

    regr_left_x = joblib.load("model/lefteye_x.model")
    regr_left_y = joblib.load("model/lefteye_y.model")
    return regr_right_x, regr_right_y, regr_left_x, regr_left_y


def load_model_path(dir):
    regr_right_x = joblib.load(dir + "/righteye_x.model")
    regr_right_y = joblib.load(dir + "/righteye_y.model")

    regr_left_x = joblib.load(dir + "/lefteye_x.model")
    regr_left_y = joblib.load(dir + "/lefteye_y.model")
    return regr_right_x, regr_right_y, regr_left_x, regr_left_y


# Perform fixation point prediction
def predict(data_right, data_left, regr_right_x, regr_right_y, regr_left_x, regr_left_y):
    rightgaze_x = int(regr_right_x.predict([data_right]))
    rightgaze_y = int(regr_right_y.predict([data_right]))
    leftgaze_x = int(regr_left_x.predict([data_left]))
    leftgaze_y = int(regr_left_y.predict([data_left]))
    gaze_x = int((leftgaze_x + rightgaze_x) / 2)
    gaze_y = int((leftgaze_y + rightgaze_y) / 2)

    return (gaze_x, gaze_y)
