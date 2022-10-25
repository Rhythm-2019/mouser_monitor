#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   visitor.py
@Time    :   2022/10/25 14:15:32
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
from ctypes.wintypes import HACCEL
import logging
import time
import config
import os
import pickle
import undetected_chromedriver.v2 as uc
import requests
import json
import xml.etree.ElementTree as ET
import notice
from selenium.webdriver.common.by import By

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger('bisitor')


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
    


class MouserMonitor(object): 
    
    def __init__(self) -> None:
        self._product_qs_dict = {}
        self._driver = uc.Chrome()
    
    def refrash_product_qs_and_cookies(self):
        self._driver.get('https://www.mouser.cn')
        
        cookies = self._driver.get_cookies()
        with open('cookies.dat', 'wb') as f:
            pickle.dump(cookies, f)
        product_qs_dict = {}
        for identify in config.PRODUCT_LIST:
            self._driver.get('https://www.mouser.cn/c/?q=%s' % identify) 
            current_url = self._driver.current_url
            # https://www.mouser.cn/ProductDetail/Nisshinbo/NJM2904RB1-TE1?qs=Gh61b4mt6UJGJCqDJm4ivw%3D%3D
            if current_url.index('qs=') == -1:
                all_a_tag_elems = driver.find_elements_by_tag_name('a')
                for elem in all_a_tag_elems:
                    if elem.text == identify and elem.get_attribute('href') is not None: 
                        self._driver.get('https://www.mouser.cn' + elem.get_attribute('href'))
                        break
            product_qs = self._driver.find_element(By.ID, 'ProductQs').get_attribute('value')
                    
            product_qs_dict[identify] = product_qs
            print(product_qs)
            logger.info('get %s product qs is %s' % (identify, product_qs))
       
        self._product_qs_dict = product_qs_dict
        
    def request_GetProductInfoPartialViews(self, identify, product_qt): 
        url = "https://www.mouser.cn/Product/Product/GetProductInfoPartialViews?qs=%s&isVip=true&" % product_qt
        self._driver.get(url)
        pre_elem = self._driver.find_element(By.XPATH, '//pre')
        if pre_elem is None:
            return None
        
        pricingAndAvailabilityResult = json.loads(pre_elem.text)['pricingAndAvailabilityResult']
        tree = ET.fromstring(pricingAndAvailabilityResult)
                
        stock = tree.find('//*[@id="pdpPricingAvailability"]/div[2]/div[1]/dl/dd[1]/div[1]').text
        
        volumns_in_transit = {}
        for volumn_in_transit in tree.findall('//*[@id="content-onOrderShipments"]/div'):
            volumns_in_transit[volumn_in_transit[0].text] = volumn_in_transit[1].text
            
        logger.info('request %s successfully, get stock is %s volumns_in_transit is %s' % (identify, stock, volumn_in_transit))        
        return PricingAndAvailabilityResult(identify, stock, volumns_in_transit)

    def release(self):
        self._driver.quit()
        
    def run(self):
        if len(self._product_qs_dict) == 0:
            self.refrash_product_qs_and_cookies()
            
        for identify, product_qs in self._product_qs_dict.items():
        
            new_pricing_andAvailability_result = self.request_GetProductInfoPartialViews(identify, product_qs)
            old_pricing_andAvailability_result = PricingAndAvailabilityResult.deserialize(identify)
            
            if new_pricing_andAvailability_result.equals(old_pricing_andAvailability_result):
                logging.info('product %s no change' % identify)
                continue
            logging.info('product %s from %s change to %s' % (old_pricing_andAvailability_result, new_pricing_andAvailability_result))
            
            notice.email_notice(config.RECEIVER_EMAIL_LIST, 'mouser 监控脚本', 'product %s from %s change to %s' % (old_pricing_andAvailability_result, new_pricing_andAvailability_result))
