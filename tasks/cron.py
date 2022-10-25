#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   cron.py
@Time    :   2022/10/18 12:22:42
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
import threading
import mouser
import threading
import schedule
import time


class JobSchduleThread(threading.Thread):
    def __init__(self, thread_name, interval):
        threading.Thread.__init__(self)
        self._thread_name = thread_name
        self._interval = interval
 
    def run(self):
        cease_continuous_run = threading.Event()
        
        while not cease_continuous_run.is_set():
            schedule.run_pending()
            time.sleep(self._interval)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    
    
def start():
    schedule.every(10).minute.do(run_threaded, mouser.handle)
    JobSchduleThread().start()
    
    