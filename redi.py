#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   redi.py
@Time    :   2022/10/25 13:58:44
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
import redis
import config

class RedisStorage(object):
    def __init__(self, host, port=6379, db=0) -> None:
        self._pool = redis.ConnectionPool(host=host, port=port, db=db)
    
    def set(self, key, val, expire):
        r = redis.Redis(connection_pool=self._pool)
        r.set(key, val, expire)
        r.close()
        
    def get(self, key):
        r = redis.Redis(connection_pool=self._pool)
        r.get(key)
        r.close()
        
redisStorage = RedisStorage(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)