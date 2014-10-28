# -*- coding: utf-8 -*-
'''
Created on 2014年7月9日

@author: stm
'''
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Common.Utils.PD_DebugLog import PD_DEBUG_LOG, DEBUG_LOG_PRINT
from Common.Utils import utils_misc


class Register_Image_Frame_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    
    # OS Category ToolKit
    OS_CATG_TOOLKIT = "ToolKit"
    OS_CATEGORY = ("ToolKit", "SUSE", "Red Hat", "Other ISO", "AIX")
    
    # OS Descriptions
    OS_DESC_TOOLKIT_V52 = "IBM ToolKit v52"
    OS_DESC_TOOLKIT_V53 = "IBM ToolKit v53"
    OS_DESC_TOOLKIT_V54 = "IBM ToolKit v54"
    OS_DESC_TOOLKIT_OTH = "IBM ToolKit other version"
    
    OS_DESC = (("IBM ToolKit v52", "IBM ToolKit v53", "IBM ToolKit v54", 
                "IBM ToolKit other version"
                ),
               ("SUSE Linux Enterprise Server 10 for IBM Power", 
                "SUSE Linux Enterprise Server 11 for IBM Power",
                "SUSE Linux Enterprise Server 12 for IBM Power", 
                "SUSE Linux Enterprise Server other version"
                ),
               ("Red Hat Enterprise Linux Server release 5.7 for IBM Power",
                "Red Hat Enterprise Linux Server release 5.8 for IBM Power",
                "Red Hat Enterprise Linux Server release 6.0 for IBM Power",
                "Red Hat Enterprise Linux Server release 6.1 for IBM Power",
                "Red Hat Enterprise Linux Server release 6.2 for IBM Power",
                "Red Hat Enterprise Linux Server release 6.3 for IBM Power",
                "Red Hat Enterprise Linux Server release 6.4 for IBM Power",
                "Red Hat Enterprise Linux Server release 7.0 for IBM Power",
                "Red Hat Enterprise Linux Server other version"
                ),
               ("Other ISO, unkonwn version"
                ),
               ("AIX 5L 5.3",
                "AIX 6.1",
                "AIX other version")
               )

    #//*[@id="osname"]/option[8]
    
    def __init__(self, driver):
        self.driver = driver
        self.accept_next_alert = True
        self.driver.switch_to.frame("_medium_frame")        
        
    def get_image_alias_input(self):
        '''
        get the ip address input box element
        '''
        return self.driver.find_element(By.ID, "imageAlias")
    
    def get_image_file_location_input(self):
        '''
        get the platform name input box element
        '''
        return self.driver.find_element(By.ID, "ospath")
    

    def get_submit_btn(self):
        '''
        get the submit button element
        '''
        #import pdb; pdb.set_trace()
        # The element is on the bottom of the dialog form
        # Need keep the dialog part visible, for example, keep a 
        # proper screen resolution.
        btn_elem = self.driver.find_element(By.ID, 'btn_submit')
        return btn_elem
    

    def is_notify_msg_present(self):
        utils_misc.set_script_timeout(self.driver)
        elem = None
        try:
            #xpath = '//div/div[@class="noty_message"]/span'
            css = 'noty_message'
            #elem = self.driver.find_element(By.XPATH, xpath)
            elem = self.driver.find_element(By.CLASS_NAME, css)
            utils_misc.restore_script_timeout(self.driver)
        except:
            return False
            
        if elem:
            return True
        else:
            return False
        
    
    def get_notify_msg(self):
        utils_misc.set_script_timeout(self.driver)
        elem = None
        
        xpath = '//div/div[@class="noty_message"]/span'
        elem = self.driver.find_element(By.XPATH, xpath)
        self.driver.set_script_timeout(30)
        return elem.text
            
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

    def get_file_type_img_radiobtn(self):
        '''
        Get the file type radio button: ISO, IMG
        '''
        return self.get_file_type_radiobtn('rdo_img')
    
    
    def get_file_type_iso_radiobtn(self):
        '''
        Get the file type radio button: ISO, IMG
        '''
        return self.get_file_type_radiobtn('rdo_iso')
    
    def get_file_type_radiobtn(self, id_name):
        '''
        Get the file type radio button: ISO, IMG
        '''
        return self.driver.find_element(By.ID, id_name)
    
    def select_osname_by_name(self, name):
        osname_list = self.driver.find_element(By.ID, 'osname')
        items = osname_list.find_elements_by_xpath('//option')
        for item in items:
            if item.text == name:
                item.click()
                break
        
    def select_ostype_by_value(self, value):
        '''
        To get the os category by value for the os category
        '''
        xpath = '//option[@value="%s"]' % value
        osname_list = self.driver.find_element(By.ID, 'ostype')
        item = osname_list.find_element_by_xpath(xpath)
        item.click()
        
    def select_osname_by_value(self, value):
        '''
        To get the os name by value for the os description
        '''
        xpath = '//*[@id="osname"]/option[@value="%s"]' % value
        osname_list = self.driver.find_element(By.ID, 'osname')
        item = osname_list.find_element_by_xpath(xpath)
        item.click()
        
    def get_alert_text(self):
        '''
        Switch to alert and get the alert text
        '''
        alert = self.driver.switch_to_alert()
        return alert.text
    
    def is_loading_getvminfo(self):
        utils_misc.set_script_timeout(self.driver)
        elem = None
        try:
            xpath = '//div[@class="loading_overlay"]/p'
            elem = self.driver.find_element(By.XPATH, xpath)
            utils_misc.restore_script_timeout(self.driver)
        except:
            return False
            
        if elem:
            return True
        else:
            return False
    