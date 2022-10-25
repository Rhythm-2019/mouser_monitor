#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   __init__.py
@Time    :   2022/10/18 11:13:20
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
import pickledb


class LocalStorage(object):
    
    def __init__(self) -> None:
        self._db = pickledb.load('store.db', True)
        
    def set(self, key, value):
        self._db.set(key, value)
    
    def get(self, key):
        return self._db.get(key)
    
localStorage = LocalStorage()