#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   app.py
@Time    :   2022/10/17 15:07:08
@Author  :   Rhythm-2019 
@Version :   1.0
@Contact :   rhythm_2019@163.com
@Desc    :   mouser 监控
-------------------------------------------------
Change Activity:
-------------------------------------------------
'''
__author__ = 'Rhythm-2019'

# here put the import lib
import json
from lib2to3.pgen2 import driver
import logging
import time
import requests
import pickle
import smtplib
import os
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from lxml import etree
import undetected_chromedriver.v2 as uc

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



PRODUCT_QS_DICT = {
    "NJM2904RB1-TE1": "dJbwp1x2B3yE9vcc8oOH2ju7J2PqSE1IbkZUq%2fQcMnrOY76iIDlwIB2PRghdOJfA",
    "NJM2904CRB1-TE1" : "dJbwp1x2B3yE9vcc8oOH2ju7J2PqSE1IpDafi68TnGHX16cEO8VwkiQi%252BgsElDHm",
    "NJM2903RB1-TE1": "dJbwp1x2B3yE9vcc8oOH2ju7J2PqSE1IZUB5QL2Sml4MMumCUxEJUt0U3%2fLvN84O",
    "NJM2903CRB1-TE1": "dJbwp1x2B3yE9vcc8oOH2ju7J2PqSE1IjHebPOBHlxbhaLQvpSGo6f7FlNCWmsAs",
    "NJM2903CRB1": "dJbwp1x2B3yE9vcc8oOH2o58nre0Yfb3UjrI6RuNmP1VGULu9qHdNsR5siLuNwjz"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.mouser.cn',
    'Cache-Control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'document',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Referer': 'https://www.mouser.cn/'
}

PROXIES = {'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}

RECEIVER_EMAIL_LIST = ["rhythm_2019@163.com"]
SENDER_EMAIL = '1345646105@qq.com'
SENDER_STMP_SECRET = 'dxunyehqljoehajc'
STMP_SERVER_ADDR = 'smtp.qq.com'
STMP_SERVER_PORT = 465

logger = logging.getLogger('mouser')

cookies = None

class PricingAndAvailabilityResult():
    
    def __init__(self, identity ,stock, voulumn_in_transit) -> None:
        self._identity = identity
        self._stock = stock
        self._voulumn_in_transit = voulumn_in_transit
        
    @property
    def stock(self):
        return self._stock
    
    @property
    def voulumn_in_transit(self):
        return self._voulumn_in_transit
        
    @property
    def identity(self):
        return self._identity

    def equals(self, pricing_andAvailability_result):
        return self._identity == pricing_andAvailability_result.identify and self._stock == pricing_andAvailability_result.stock and self._voulumn_in_transit == pricing_andAvailability_result.voulumn_in_transit
    
    def serialize(self): 
        with open("/tmp/mouser/%s" % self.identity, "wb") as f:
            pickle.dumps(self, f)
    
    @classmethod
    def deserialize(cls, identify):
        if not os.path.exists("/tmp/mouser/%s" % identify):
            return None
        with open("/tmp/mouser/%s" % identify, "rb") as f:
            return pickle.loads(f)
    

def email_notice(receiver_email_list, subject, content, attach_file=None):
    msg = MIMEMultipart()
    
    msg.attach(MIMEText(content))
    
    # 添加附件
    if attach_file is not None: #最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
        docFile = attach_file
        docApart = MIMEApplication(open(docFile, 'rb').read())
        docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
        msg.attach(docApart)    
    
    for receiver_email in receiver_email_list:
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
    
        try:
            s = smtplib.SMTP_SSL(STMP_SERVER_ADDR, STMP_SERVER_PORT)
            s.login(SENDER_EMAIL, SENDER_STMP_SECRET)
            s.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
            logger.info("send a email to %s" % receiver_email)
        except smtplib.SMTPException as e:
            logger.info("failed to send email to %s, eror is %s" % receiver_email, e)
        finally:
            s.quit()
      

def request_PoructQt(identify, cookies):
    url = 'https://www.mouser.cn/c/?q=%s' % identify
    print(url)
    resp = requests.get(url, headers=HEADERS, proxies=PROXIES, cookies=cookies, timeout=10, verify=False)
    print(resp.content)
    if resp.status_code == 301 or resp.status_code == 333: 
        localtion = resp.header['Location']
        product_qt = localtion.rindex('/')
        
        
        logger.info('get product %s qt is %s' % (identify, product_qt))
        return product_qt
    
    logger.error('failed to get product %s qt' % identify)
    return None
    
        
    
def request_GetProductInfoPartialViews(identify, product_qt): 
    url = "https://www.mouser.cn/Product/Product/GetProductInfoPartialViews?qs=%s&isVip=true&" % product_qt
        
    resp = requests.get(url, headers=HEADERS, timeout=10,  proxies=PROXIES, cookies=cookies, verify=False)
    if resp.status_code != 200: 
        logger.error("failed to request url %s, content is %s" % (url, resp.content))
        return 
    
    
    pricingAndAvailabilityResult = json.loads(resp.content).pricingAndAvailabilityResult
    tree = ET.fromstring(pricingAndAvailabilityResult)
            
    stock = tree.find('//*[@id="pdpPricingAvailability"]/div[2]/div[1]/dl/dd[1]/div[1]').text
    
    volumns_in_transit = {}
    for volumn_in_transit in tree.findall('//*[@id="content-onOrderShipments"]/div'):
        volumns_in_transit[volumn_in_transit[0].text] = volumn_in_transit[1].text
        
    logger.info('request %s successfully, get stock is %s volumns_in_transit is %s' % (identify, stock, volumn_in_transit))        
    return PricingAndAvailabilityResult(identify, stock, volumns_in_transit)

def request_cookies():
    
    s = requests.Session()
    resp = s.get('https://www.mouser.cn/', headers=HEADERS,  proxies=PROXIES, verify=False)
    
    if resp.status_code != 200:
        root = etree.HTML(resp.content)
        jsUrl = root.xpath('/html/body/script[2]/@src')[0]
        resp = s.get('https://www.mouser.cn%s' % jsUrl, headers=HEADERS, proxies=PROXIES, cookies=cookies, verify=False)
        resp = s.get('https://www.mouser.cn/%s/init.js' % jsUrl.split('/')[1], headers=HEADERS, proxies=PROXIES, cookies=cookies, verify=False)
        
        new_headers = HEADERS.copy()
        new_headers['Referer'] = 'https://www.mouser.cn/'
        resp = s.get('https://www.mouser.cn/', headers=new_headers, cookies=resp.cookies, proxies=PROXIES, verify=False)
        if resp.status_code != 200:
            raise
    return resp.cookies

def get_cookies():
    driver = uc.Chrome()
    driver.get('https://mouser.cn')  # my own test test site with max anti-bot protection
    
    driver.
    
# @catch_exception(False)
def handle(): 
    
    # cookies = request_cookies()
    # for identify, product_qs in PRODUCT_QS_DICT.items():
        
    #     product_qt = request_PoructQt(identify, cookies)
    #     if product_qt is None:
    #         continue
    #     new_pricing_andAvailability_result = request_GetProductInfoPartialViews(identify, product_qt, cookies)
    #     old_pricing_andAvailability_result = PricingAndAvailabilityResult.deserialize(identify)
        
    #     if new_pricing_andAvailability_result.equals(old_pricing_andAvailability_result):
    #         logging.info('product %s no change' % identify)
    #         continue
    #     logging.info('product %s from %s change to %s' % (old_pricing_andAvailability_result, new_pricing_andAvailability_result))
        
    #     email_notice(RECEIVER_EMAIL_LIST, 'mouser 监控脚本', 'product %s from %s change to %s' % (old_pricing_andAvailability_result, new_pricing_andAvailability_result))

if __name__ == '__main__': 
    handle()