# -*- coding: utf-8 -*-
'''
Created on 2014��10��23��

@author: stm
'''
from selenium.webdriver.common.by import By
from Common.Utils import PD_DebugLog, utils_misc
import time

class VM_Summary_UIMap():
    '''
    Get the page element from Platform Summary page
    '''
    
    # Routine actions bar("常规" 栏）
    ACTION_BOOTUP, ACTION_SMSBOOT, ACTION_SHUTDOWN, ACTION_POWERDOWN, ACTION_REBOOT = range(1,6)
    
    # More actions bar("更多" 栏）
    ACTION_EDIT, ACTION_RENAME, ACTION_REMOVE, ACTION_VOL_MGMT, ACTION_CONFIG_NIC, \
    ACTION_CDROM_MGMT, ACTION_UNMOUNT, ACTION_MIGRATE, ACTION_VM_TEMPLATE_CONVT, \
    ACTION_REGISTER_IP, ACTION_CANCEL_BOOT_WITH_HOST, ACTION_SOFTWARE_MGMT = range(1,13)
    
    VM_NAME_XPATH = '/html/body/div/fieldset/legend'
    VM_CURRENT_STATUS_XPATH = '//*[@id="vm_status_show"]'
    VM_IPADDR_XPATH = '/html/body/div/form/fieldset/table/tbody/tr/td[2]/ul/li[2]/span[2]'
    
    
    def __init__(self, driver):
        ''' initialize the Platform Summary Page class '''
       
        self.driver = driver
        self.accept_next_alert = True
        
    def _common_enter_summary_frame_proc(self):
        # /html/body/div[2]/div[2]/iframe
        # //*[@id="_summary"]
        # self.driver.switch_to.frame('_summary')
        self.contentpanel = self.driver.find_element(By.ID, 'contentpanel')
        #PD_DebugLog.debug_print(self.contentpanel.page_source)
        self.framesummary = self.contentpanel.find_element(By.ID, '_stage')
        #PD_DebugLog.debug_print(self.frame_summary.)
        
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
            path_str = '//html/body/div/fieldset/table/tbody/tr/td[2]/ul/li/span'
            path_str_from_Chrome = '//*[@id="wrapper"]/fieldset/table/tbody/tr/td[2]/ul/li/span[1]'
            title_test_elm = self.driver.find_element(By.XPATH, path_str)
            text = title_test_elm.text
            PD_DebugLog.debug_print('The title is %s .' % text)
            
    def _common_exit_summary_frame_proc(self): 
        self.driver.switch_to.default_content()        
        
        
    def get_vm_static_label_text(self, label_xpath):
        '''
        get the static label text
        '''
        self._common_enter_summary_frame_proc()
        
        elem = self.driver.find_element(By.XPATH, label_xpath)
        text = elem.text
        PD_DebugLog.debug_print("Get the element title: " + elem.text)
        self._common_exit_summary_frame_proc()
        return text
    
    
    def get_vm_name(self):
        '''
        get the vm name
        '''
        return self.get_vm_static_label_text(VM_Summary_UIMap.VM_NAME_XPATH)    
        
        
    def get_vm_ip(self):
        '''
        get the vm name
        '''
        return self.get_vm_static_label_text(VM_Summary_UIMap.VM_IPADDR_XPATH)    
        
    
    def get_vm_current_status(self):
        '''
        To get the vm current status txt
        '''
        return self.get_vm_static_label_text(VM_Summary_UIMap.VM_CURRENT_STATUS_XPATH)


    def execute_action_without_confirm_dialog(self, action_type, with_dialog_prompt=False):
        '''
        To execute the action in the route bar without dialog prompt
        '''
        self.execute_action_with_confirm_dialog(action_type, False, False)
        
    
    def execute_action_with_confirm_dialog(self, action_type, confirm=True, with_dialog_prompt=True):
        '''
        To execute the action in the route bar
        '''
        self._common_enter_summary_frame_proc()
        # //*[@id="vm_shutdown"]
        xpath = '//html/body/div/form/div/table/tbody/tr/td/div/ul/li[%d]/a' % action_type
        shutdown_system_elemt = self.driver.find_element(By.XPATH, xpath)
        shutdown_system_elemt.click()
        time.sleep(1)
        
        if with_dialog_prompt:
            alert_dialog = self.driver.switch_to_alert()
            assert alert_dialog
            
            time.sleep(1)
            if confirm:
                alert_dialog.accept()
            else:
                alert_dialog.cancel()
            time.sleep(1)
            
        self._common_exit_summary_frame_proc()
        
    def execute_boot_system(self):
        '''
        To shutdown system
        '''
        self.execute_action_without_confirm_dialog(VM_Summary_UIMap.ACTION_BOOTUP)
    
        
    def execute_shutdown_system(self, shutdown_confirmed=True):
        '''
        To shutdown system
        '''
        self.execute_action_with_confirm_dialog(VM_Summary_UIMap.ACTION_SHUTDOWN, shutdown_confirmed)
        
    
    def execute_powerdown_system(self, powerdown_confirmed=True):
        '''
        To shutdown system
        '''
        self.execute_action_with_confirm_dialog(VM_Summary_UIMap.ACTION_POWERDOWN, powerdown_confirmed)
        
        
    def execute_reboot_system(self, reboot_confirmed=True):
        '''
        To shutdown system
        '''
        self.execute_action_with_confirm_dialog(VM_Summary_UIMap.ACTION_REBOOT, reboot_confirmed)
        
        
    def is_vm_starting(self):
        '''
        To compare the current status txt, if it running  return True
        '''
        return self.test_expected_status_text(u'启动中')
        
        
    def is_vm_running(self):
        '''
        To compare the current status txt, if it running  return True
        '''
        return self.test_expected_status_text(u'运行')
        
        
    def is_vm_in_shutdown_progress(self):
        return self.is_vm_in_powerdown_progress()
        
        
    def is_vm_in_powerdown_progress(self):
        '''
        To compare the current status txt, if it running  return True
        '''
        return self.test_expected_status_text(u'关闭中')
        
        
    def is_vm_in_deleting_progress(self):
        '''
        To compare the current status txt, if it deleting return True
        '''
        return self.test_expected_status_text(u'删除中')
        
        
    def test_expected_status_text(self, status_text):
        '''
        To compare the status text expected
        '''
        expect_text = status_text
        got_text = self.get_vm_current_status()
        
        if expect_text == got_text:
            return True
        else: 
            return False
        

    def get_more_actions_bar(self):
        '''
        Return the more actions bar
        '''
        self._common_enter_summary_frame_proc()
        
        xpath = '/html/body/div/form/div/table/tbody/tr/td[2]/div/h3/a'
        more_actions_bar_elemt = self.driver.find_element(By.XPATH, xpath)
        class_attribute_value = more_actions_bar_elemt.get_attribute("class")
        
        PD_DebugLog.debug_print("more actions bar class attribute is : " + class_attribute_value)
        if class_attribute_value != 'expand':
            more_actions_bar_elemt.click() 
        
        class_attribute_value = more_actions_bar_elemt.get_attribute("class")
        PD_DebugLog.debug_print("more actions bar class attribute is : " + class_attribute_value)
        
            
        self._common_exit_summary_frame_proc()
        
        return more_actions_bar_elemt, class_attribute_value 
    
    
    def expand_more_actions_bar(self):
        '''
        Make the more actions bar is expanded, if not expand it
        '''
        self._common_enter_summary_frame_proc()
        
        xpath = '/html/body/div/form/div/table/tbody/tr/td[2]/div/h3/a'
        more_actions_bar_elemt = self.driver.find_element(By.XPATH, xpath)
        class_attribute_value = more_actions_bar_elemt.get_attribute("class")
        
        PD_DebugLog.debug_print("more actions bar class attribute is : " + class_attribute_value)
        if class_attribute_value != 'expand':
            more_actions_bar_elemt.click() 
        
        class_attribute_value = more_actions_bar_elemt.get_attribute("class")
        PD_DebugLog.debug_print("more actions bar class attribute is : " + class_attribute_value)
        
        self._common_exit_summary_frame_proc()
        
             
    def return_to_parent(self):
        self.driver.switch_to.default_contenct()

    
    def execute_action_from_more_actions_bar(self, action_type, with_dialog_prompt=False, confirm=True):
        '''
        execute the action in the more actions bar
        '''
        self._common_enter_summary_frame_proc()
        xpath = '//html/body/div/form/div/table/tbody/tr/td[2]/div/ul/li[%d]/a' % action_type
        elemt = self.driver.find_element(By.XPATH, xpath)
        elemt.click()
        time.sleep(1)
        
        if with_dialog_prompt:
            alert_dialog = self.driver.switch_to_alert()
        assert alert_dialog
        
        time.sleep(1)
        if confirm:
            alert_dialog.accept()
        else:
            alert_dialog.cancel()
        time.sleep(1)
        self._common_exit_summary_frame_proc()
        
        
    def click_register_IP_link(self):
        self.execute_action_from_more_actions_bar(VM_Summary_UIMap.ACTION_REGISTER_IP)
    
    
    def click_remove_vm_link(self):
        self.execute_action_from_more_actions_bar(VM_Summary_UIMap.ACTION_REMOVE, with_dialog_prompt=True, confirm=True)
        
        
    def is_loading_getvminfo(self):
        '''
        <div id="loading_overlay_getvminfo" style="position: fixed; z-index: 0; top: 325.8px; left: 304.5px; display: none;">
        <a class="close"></a>
        <img src="/images/loading.gif" alt="">
        <p>正在获取虚拟机信息</p>
        </div>
        '''
        utils_misc.set_implicity_wait_timeout(self.driver)
        elem = None
        try:
            xpath = '//*[@id="loading_overlay_getvminfo"]/a'
            elem = self.driver.find_element(By.XPATH, xpath)
            class_value = elem.get_attribute('class')
            PD_DebugLog.debug_print("The element's class value is " + class_value)
            utils_misc.restore_implicity_wait_timeout(self.driver)
        except:
            return False
            
        if elem and class_value != 'close':
            return True
        else:
            return False
