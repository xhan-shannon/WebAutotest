# -*- coding: utf-8 -*-
'''
Created on 2014年7月9日

@author: stm
'''
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Common.Utils.PD_DebugLog import PD_DEBUG_LOG, DEBUG_LOG_PRINT


class Remove_VM_Frame_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    
    IPADDR, NETMASK, GATEWAY, DNS, SECONDDNS = range(1, 6)
    
    def __init__(self, driver):
        self.driver = driver
        self.accept_next_alert = True
        self.driver.switch_to.frame("_small_frame")        
        
    
    def get_checkbox_elemt(self, elemt_idx):
        '''
        Get the element by xpath with the appropriate xpath 
        '''
        xpath = '//html/body/form/div/p/input'
        elemt = self.driver.find_element(By.XPATH, xpath)
        return elemt
        
    
    def get_confirmed_btn(self):
        '''
        get the file select button element
        '''
        return self.driver.find_element(By.ID, 'btn_submit')
