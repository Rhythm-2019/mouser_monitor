#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   exception.py
@Time    :   2022/10/18 16:16:33
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

def catch_exception(cancel_on_failure):
    def catch_exception_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exception_decorator
        