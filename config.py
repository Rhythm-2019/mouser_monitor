#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   config.py
@Time    :   2022/10/25 13:56:00
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
PROXIES = {'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}

RECEIVER_EMAIL_LIST = ["rhythm_2019@163.com"]
SENDER_EMAIL = '1345646105@qq.com'
SENDER_STMP_SECRET = 'dxunyehqljoehajc'
STMP_SERVER_ADDR = 'smtp.qq.com'
STMP_SERVER_PORT = 465

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


PRODUCT_LIST = [
    'NJM2904RB1-TE1',
    # 'NJM2904CRB1-TE1',
    # 'NJM2903RB1-TE1',
    # 'NJM2903CRB1-TE1',
    # 'NJM2903CRB1',
]

