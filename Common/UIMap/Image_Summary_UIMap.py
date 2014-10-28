# -*- coding: utf-8 -*-
'''
Created on 2014年7月11日

@author: stm
'''
from selenium.webdriver.common.by import By
from Common.Utils import PD_DebugLog

class ImageLib_Summary_UIMap(object):
    '''
    Get the page element from Platform Summary page
    '''

    def __init__(self, driver):
        ''' initialize the ImageLib Summary Page class '''
       
        self.driver = driver
        self.accept_next_alert = True
        
    def _common_enter_summary_frame_proc(self):
        # /html/body/div[2]/div[2]/iframe
        # //*[@id="_summary"]
        # self.driver.switch_to.frame('_summary')
        self.contentpanel = self.driver.find_element(By.ID, 'contentpanel')
        #PD_DebugLog.debug_print(self.contentpanel.page_source)
        self.framesummary = self.contentpanel.find_element(By.ID, '_stage')
        
        # continuously get the frame and the sub frame method experience 
        # failed: NoSuchFrameException: Message: u'Unable to locate frame: _stage._summary' ; Stacktrace: 
        # at FirefoxDriver.prototype.switchToFrame (file:///c:/users/stm/appdata/local/temp/tmpaqoscv/extensions/fxdriver@googlecode.com/components/driver_component.js:8974)
        # at DelayedCommand.prototype.executeInternal_/h (file:///c:/users/stm/appdata/local/temp/tmpaqoscv/extensions/fxdriver@googlecode.com/components/command_processor.js:10884)
        # at fxdriver.Timer.prototype.setTimeout/<.notify (file:///c:/users/stm/appdata/local/temp/tmpaqoscv/extensions/fxdriver@googlecode.com/components/command_processor.js:396)
        
        #self.driver_sub = self.driver.switch_to.frame('_stage._summary')
        
        # Failed: the method would not return the driver
        #self.driver_sub = self.driver.switch_to.frame('_stage')
        self.driver.switch_to.frame('_stage')
        self.driver.switch_to.frame('_summary')
        
        self.frame_summary_wrapper = self.driver.find_element(By.XPATH, '//html/body')
        
    def _test_if_in_summary_frame(self):
        # Test if frame summary is present
        # 1. 
        isPresent = self.frame_summary_wrapper != None
        msg = 'Frame summary is %s present'
        if isPresent:
            PD_DebugLog.debug_print(msg % '')
        else:
            PD_DebugLog.debug_print(msg % 'not')
        
        if isPresent:
            path_str = '/html/body/div/fieldset/table/tbody/tr/td[2]/ul/li/span'
            path_str_from_Chrome = '//*[@id="wrapper"]/fieldset/table/tbody/tr/td[2]/ul/li/span[1]'
            title_test_elm = self.driver.find_element(By.XPATH, path_str)
            text = title_test_elm.text
            PD_DebugLog.debug_print('The title is %s .' % text)
            
    def _common_exit_summary_frame_proc(self): 
        self.driver.switch_to.default_content()        
        
        
        
    def get_imagelib_text(self):
        '''
        get the image lib summary text
        '''
        
        self._common_enter_summary_frame_proc()
        # /html/body/div/fieldset/legend
        xpath = '/html/body/div/fieldset/legend'
        elem = self.driver.find_element(By.XPATH, xpath)
        text = elem.text
        PD_DebugLog.debug_print("Get the element title: " + elem.text)
        self._common_exit_summary_frame_proc()
        return text
        
    
    def click_register_image_link(self):
        '''
        get the register image link
        should use the right xpath expression end with 'a' element.
        '''
        
        self._common_enter_summary_frame_proc()
        
        xpath_from_Chrome = '//*[@id="wrapper"]/div[2]/table/tbody/tr/td/div/ul/li[2]/a'
        #xpath_from_firefox = '/html/body/div/fieldset/table/tbody/tr/td[2]/ul/li/span[2]'
        xpath_str = xpath_from_Chrome
        elem = self.frame_summary_wrapper.find_element(By.XPATH, xpath_str)
        #elem = self.frame_summary_wrapper.find_element_by_link_text(u'注册镜像')
        PD_DebugLog.debug_print("Get the element (register image) title: " + elem.text)

        elem.click()
        
        self._common_exit_summary_frame_proc()
        

    def return_to_parent(self):
        self.driver.switch_to.default_contenct()
