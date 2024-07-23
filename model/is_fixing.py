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


def is_fixing(x0, y0, x1, y1, threshold):
    if x0 != 0:
        return (int(x0) - int(x1)) ^ 2 + (int(y0) - int(y1)) ^ 2 < threshold
    else:
        return False


if __name__ == '__main__':
    print(is_fixing(1, 1, 1, 1, 0))
