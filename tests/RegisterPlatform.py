# -*- coding: utf-8 -*-
'''
Created on 2014年7月1日

@author: stm
'''
import logging
import sys
import threading
import time
import unittest

import SendKeys
from selenium.webdriver.common.by import By

from Common import PD_Login
from Common import WindowFinder
from Common.Basejob import Basejob
from Common.TestSpeedControl import TestSpeedControl
from Common.UIMap.Main_Browser_UIMap import Main_Browser_UIMap
from Common.UIMap.Platform_Summary_UIMap import Platform_Summary_UIMap
from Common.UIMap.Platform_Tree import Platform_Tree
from Common.UIMap.Register_Platfrom_Frame_UIMap import Register_Platfrom_Frame_UIMap
from Common.Utils import PD_DebugLog


class RegisterPlatform(Basejob):
    
    def setUp(self):
        Basejob.setUp(self)


    def check_if_platform_ip_existing(self, driver, platform_ip, platform_name):
        '''
        To get platform node from the web page
        And enter into the page, and get the elements info.
        '''
        cur_platform_ip = ''
        cur_platform_name = ''
        
        default_main_browser = Main_Browser_UIMap(driver)
        subtree = default_main_browser.get_platform_sub_menu_tree()
        platform_subtree = Platform_Tree(driver, subtree)
        count = platform_subtree.get_platform_count()
        for index in range(count):
            #elem = platform_subtree.get_platform_item(index)  #platformNode.switch_to_page()
            platform_subtree.enter_platform_summary_page(index)
            # elem.click()    # switch into the platform tree node
            # elem_page_driver = Platform_Summary_UIMap(default_main_browser)
            cur_platform_name = platform_subtree.get_platform_name(index)
            cur_platform_ip = platform_subtree.get_platform_ip() #index
            if platform_name == cur_platform_name:
                break 
        
        PD_DebugLog.debug_print("")
        if platform_ip != cur_platform_ip or platform_name != cur_platform_name:
            return False
        else:
            return True
    
    
    def register_platform_prc(self, caller_func_name, platform_ip, platform_name):
        '''
        The procedure is for registering platform and at the same time to check if 
        the platform and ip are already existing.
        '''
        def _action_on_trigger_element(_element):
            _element.click()
            
            
        logging.debug("Test RegisterPlatform debug info")
        # Step 1: Login and pass in with username, password, server and port
        PD_DebugLog.stepinfo("Login PowerDirector")
        pd_login_username = self.shared_config.get('DEFAULT', 'pd_login_username')
        pd_login_password = self.shared_config.get('DEFAULT', 'pd_login_password')
        
        pd_client_browser = PD_Login.login(self.driver, pd_login_username, pd_login_password)
        
        # Todo:
        # Need check if the current ip and platform is already registered
        # 1) click the tree nodes, expand the node
        # 2) jump to the summary frame page
        
        platform_ip_existing = self.check_if_platform_ip_existing(pd_client_browser, 
                                                                  platform_ip, 
                                                                  platform_name)
     
        # If the function is called by register_platform_check case
        cur_test_func_name = caller_func_name
        PD_DebugLog.debug_print("The current test function is: " + cur_test_func_name)
        if cur_test_func_name.lower().endswith('check'):
            msg = "The platform and IP are not registered"
            self.assertTrue(platform_ip_existing, msg)
            return
        else:
            self.assertFalse(platform_ip_existing)
        
        # If not, the function is executed by the normal register procedure
        # And go on to next step
        
        # Step 2: Click the register_platform button
        print("select and click the register platform button")
        #reg_pltfm_btn = pd_client_browser.find_elements(By.XPATH, "//*[@id=\"link_register_platform\"]")
        #reg_pltfm_btn.click()
        pd_client_browser.switch_to.default_content()
        reg_pltfm_elm = pd_client_browser.find_element_by_id("link_register_platform")
        reg_pltfm_elm.click()
        time.sleep(1)
        
        # Step 3: input the information for platform registering 
        pd_browser_map = Register_Platfrom_Frame_UIMap(pd_client_browser)
        ip_register_input = pd_browser_map.get_ip_register_input()
        ip_register_input.send_keys(platform_ip)
        platform_name_input = pd_browser_map.get_platform_name_input()
        platform_name_input.send_keys(platform_name)
        
        #pd_browser_map.update_file_select_text("E:\\TEAMSUN\\Lic\\060556A_8246-L2D_111.LIC")
    
        username_input = pd_browser_map.get_username_input()
        username_input.send_keys("padmin") 
        password_input = pd_browser_map.get_userpasswd_input()
        password_input.send_keys("padmin") 
        
        
        lic_file_path = "E:\\TEAMSUN\\Lic\\060556A_8246-L2D_111.LIC"
        file_select_btn = pd_browser_map.get_file_select_btn()
        
        #select_file_btn_elm.click()
        th = threading.Thread(target = _action_on_trigger_element, args =[
                                  file_select_btn])
        th.start()
        time.sleep(1)
            
        # Call WindowFinder Class
        upload_file_dialog_title = "文件上传"
        enter_str = "{ENTER}"
        win = WindowFinder.WindowFinder()
        win.find_window_wildcard(".*Open file.*")
        win.set_foreground()
        result_status = True
        try:
            time.sleep(1)
            SendKeys.SendKeys(lic_file_path)
            time.sleep(1)
            SendKeys.SendKeys(enter_str)
            time.sleep(3)
            assert(not th.isAlive())
        except:
            result_status = False
        
        time.sleep(2)
     
    #     pd_client_browser.switch_to_window(parent_h)  
        
        time.sleep(2)
        try:
            submit_btn = pd_browser_map.get_submit_btn()
            #saved_wnd = pd_client_browser.current_window_handle
            submit_btn.click()
            #current_wnd = pd_client_browser.current_window_handle
            count_to_try = 10 #1000
            iTry = 0
            
            while iTry < count_to_try:
                if pd_browser_map.is_alert_present():
                    alert_text = pd_browser_map.close_alert_and_get_its_text()
                    print("Get the alert text : " +  alert_text)
                    self.assertEqual(u"平台IP地址已存在", alert_text)
                    time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
                    break
                    
                time.sleep(5)
                iTry = iTry + 1
                      
            # Wait for a while to detect whether there is a popup dialog
            # If there is a dialog, then the test would terminate

            time.sleep(1)
            #pd_client_browser.close()
            print("Test pass")
        finally:
            pass
#         except:
#             #alert = pd_client_browser.switch_to_window(window_name)
#             js = '''html = document.getElementsByTagName('html')[0];
#                   return html.outerHTML;'''
#             #html = alert.
#             #print(html)
#             
#             parent_h = pd_client_browser.current_window_handle
#             # click on the link that opens a new window
#             handles = pd_client_browser.window_handles # before the pop-up window closes
#             #handles.remove(parent_h)
#             pd_client_browser.switch_to_window(handles.pop())
#             #pd_client_browser.find_element_by_id("file").send_keys("abc")
#             logging.debug(pd_client_browser.title)
#             #logging.debug(pd_client_browser.)
#             # do stuff in the popup
#             #pd_client_browser
#             # popup window closes
#             pd_client_browser.switch_to_window(parent_h)
#             pd_client_browser.close()
#             pd_client_browser.switch_to_default_content()
#             pd_client_browser.quit()    
    
    def test_Register_Platform_Check(self):
        u'''注册平台 后检查是否已经存在该Platform和IP'''
        platform_ip = "172.24.23.111"
        platform_name = "PLTFM_AUTO_TEST"
        
        caller_func_name = sys._getframe().f_code.co_name
        self.register_platform_prc(caller_func_name, platform_ip, platform_name)
        
    def test_Register_Platform(self):
        u'''注册平台 '''
        platform_ip = "172.24.23.111"
        platform_name = "PLTFM_AUTO_TEST"
        
        caller_func_name = sys._getframe().f_code.co_name
        self.register_platform_prc(caller_func_name, platform_ip, platform_name)
        
