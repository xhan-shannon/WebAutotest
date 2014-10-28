# -*- coding: utf-8 -*-
'''
Created on 2014年7月9日

@author: stm
'''
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Common.Utils.PD_DebugLog import PD_DEBUG_LOG, DEBUG_LOG_PRINT


class Register_VM_IP_Frame_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    
    IPADDR, NETMASK, GATEWAY, DNS, SECONDDNS = range(1, 6)
    
    def __init__(self, driver):
        self.driver = driver
        self.accept_next_alert = True
        self.driver.switch_to.frame("_medium_frame")        
        
    
    def get_input_elemt(self, elemt_idx):
        '''
        Get the element by xpath with the appropriate index 
        '''
        xpath = '/html/body/form/div/fieldset/table/tbody/tr[%d]/td/input' % elemt_idx
        elemt = self.driver.find_element(By.XPATH, xpath)
        return elemt
        
    def get_ip_addr_input(self):
        '''
        get the ip address input box element
        '''
        return self.get_input_elemt(Register_VM_IP_Frame_UIMap.IPADDR)
    
    def get_netmask_input(self):
        '''
        get the ip address input box element
        '''
        return self.get_input_elemt(Register_VM_IP_Frame_UIMap.NETMASK)
    
    
    def get_gateway_input(self):
        '''
        get the ip address input box element
        '''
        return self.get_input_elemt(Register_VM_IP_Frame_UIMap.GATEWAY)
    
    
    def get_dns_input(self):
        '''
        get the ip address input box element
        '''
        return self.get_input_elemt(Register_VM_IP_Frame_UIMap.DNS)
    
    
    def get_seconddns_input(self):
        '''
        get the ip address input box element
        '''
        return self.get_input_elemt(Register_VM_IP_Frame_UIMap.SECONDDNS)
    
    
    def get_submit_btn(self):
        '''
        get the file select button element
        '''
        return self.driver.find_element(By.ID, 'btn_submit')
    
    def return_main_page(self):
        self.driver.switch_to.default_content()
