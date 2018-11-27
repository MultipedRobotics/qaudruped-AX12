#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pi@multiped ~ $ sudo i2cdetect -y 1
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1f
# 20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 70: 70 -- -- -- -- -- -- --
#
from __future__ import print_function
import time
from pygecko.multiprocessing import geckopy
from messages import IMU, Vector
from nxp_imu import IMU as IMU_hw

def bye():
    print('='*40)
    print(' lidar bye ...')
    print('='*40)


def imu_publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    p = geckopy.Publisher()

    test = kwargs.get('test', False)

    imu = IMU_hw()

    while not geckopy.is_shutdown():
        if test:  # fake readings
            msg = IMU(
                Vector(1,2,3),
                Vector(1,2,3),
                Vector(1,2,3),
            )

        else:
            a,m,g = imu.get()
            geckopy.log('{:.1f} {:.1f} {:.1f}'.format(*a))
            msg = IMU(
                Vector(*a),
                Vector(*m),
                Vector(*g)
            )

        p.pub('imu', msg)

        msg = Vector(0,0,1)
        p.pub('unit_accel', msg)

        # sleep
        rate.sleep()


if __name__ == "__main__":
    kw = {'test': True}
    imu_publisher(kwargs=kw)
