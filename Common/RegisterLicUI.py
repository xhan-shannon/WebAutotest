# -*- coding: utf-8 -*-
'''
Created on 20140630

@author: stm
'''
from selenium.webdriver.common.by import By

class RegisterLicUI(object):
    '''
    Deal with UI elements related to the register lic file window 
    '''
    def __init__(self, driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.driver.implicitly_wait(30)

    def get_response_msg_elm(self):
        '''
        get the task table element
        '''
        response_msg = self.driver.find_element_by_id('msg').text
        return response_msg

    def get_select_file_btn_elm(self):
        '''
        get select file button element
        '''
        select_file_btn_elm = self.driver.find_element(By.XPATH,
                                 '//*[@id="uploadform"]/div/p[3]/input')
         
        return select_file_btn_elm

    def get_submit_btn(self):
        '''
        Return the submit button
        '''
        return self.driver.find_element_by_id("btn_submit")

    
    def get_alert_text(self):
        '''
        Switch to alert and get the alert text
        '''
        alert = self.driver.switch_to_alert()
        return alert.text

    
    def get_current_title(self):
        return self.driver.title
    
    
        
    
    
     
