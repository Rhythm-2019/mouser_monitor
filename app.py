#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   app.py
@Time    :   2022/10/25 14:48:55
@Author  :   Rhythm-2019 
@Version :   1.0
@Contact :   rhythm_2019@163.com
@Desc    :   None
-------------------------------------------------
Change Activity:
-------------------------------------------------
'''
__author__ = 'Rhythm-2019'

# here put the import lib
import monitor

if __name__ == '__main__':
    monitor = monitor.MouserMonitor()
    monitor.run()
    monitor.release()