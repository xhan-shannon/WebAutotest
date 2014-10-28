# -*- coding: utf-8 -*-
'''
Created on 2014年7月9日

@author: stm
'''
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Common.Utils.PD_DebugLog import PD_DEBUG_LOG, DEBUG_LOG_PRINT


class Register_Platfrom_Frame_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    def __init__(self, driver):
        self.driver = driver
        self.accept_next_alert = True
        self.driver.switch_to.frame("_medium_frame")        
        
    def get_ip_register_input(self):
        '''
        get the ip address input box element
        '''
        return self.driver.find_element(By.ID, "ip_addr")
    
    def get_platform_name_input(self):
        '''
        get the platform name input box element
        '''
        return self.driver.find_element(By.ID, "platform_name")
    
    def get_username_input(self):
        '''
        get the user name input box element
        '''
        return self.driver.find_element(By.ID, "user_name")
    
    def get_userpasswd_input(self):
        '''
        get the user name input box element
        '''
        return self.driver.find_element(By.ID, "user_password")
    
    def get_file_select_btn(self):
        '''
        get the file select button element
        '''
        return self.driver.find_element(By.XPATH, 
                    '//*[@id="platformForm"]/div/div[1]/fieldset[3]/table/tbody/tr[1]/td[1]/input[1]')

    def get_file_select_text(self):
        '''
        get the file select button element
        '''
        return self.driver.find_element(By.ID, "ospath") 

    def update_file_select_text(self, text):
        '''
        Update the text for file select text
        '''
        elmt = self.get_file_select_text()
        elmt.readonly = False
        js = 'document.getElementById("ospath").readOnly = ""'
        self.driver.execute_script(js)
        elmt.send_keys(text)
        elmt.send_keys(Keys.TAB)
        
        if DEBUG_LOG_PRINT:
            print(elmt.get_attribute('readonly'))
            #print(elmt.get_attribute('class')).send_keys()
            print(elmt.get_attribute('type'))
            print(elmt.get_attribute('style'))
            
        file_elm = self.driver.find_element(By.ID, "file")
        file_elm_js_onchange = 'document.getElementById("file").onchange()'
        self.driver.execute_script(file_elm_js_onchange, file_elm)
 

        #elmt.onchange()

    def get_submit_btn(self):
        '''
        get the submit button element
        '''
        return self.driver.find_element(By.ID, 'btn_submit')
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
        