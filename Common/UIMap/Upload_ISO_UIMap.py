# -*- coding: utf-8 -*-
'''
Created on 2014年7月29日

@author: stm
'''
from selenium.webdriver.common.by import By

class Upload_ISO_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.frame("_medium_frame")        
        
    def get_header(self):
        '''
        get the header element text
        '''
        return self.driver.find_element(By.XPATH, '//*[@id="uploadform"]/div/h2')  
    
    def get_next_button(self):
        '''
        get the next button
        '''
        return self.driver.find_element(By.ID, "btn_next") 
    
    def get_image_name_input(self):
        '''
        get the image name input box element
        '''
        return self.driver.find_element(By.ID, 'imageAlias')
        
    def select_osname_by_name(self, name):
        osname_list = self.driver.find_element(By.ID, 'osname')
        items = osname_list.find_elements_by_xpath('//option')
        for item in items:
            if item.text == name:
                item.click()
                break
