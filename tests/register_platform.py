# -*- coding: utf-8 -*-
'''
Created on 2014年5月19日

@author: hanxm
'''
import threading
from Common import WindowFinder
import SendKeys
'''
Register the platform
'''
import os
import time

import PD_Common
import PD_Login

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def _action_on_trigger_element(_element):
            _element.click()
            
if __name__ == '__main__':
    
    # Step 1: Login and pass in with username, password, server and port
    print("Login PowerDirector")
    pd_client_browser = PD_Login.login("admin", "123456", "172.24.23.111", "8080")
    
    # Step 2: Click the register_platform button
    print("select and click the register platform button")
    reg_pltfm_btn = pd_client_browser.find_elements(By.XPATH, "//*[@id=\"link_register_platform\"]")
    #reg_pltfm_btn.click()
    pd_client_browser.switch_to.default_content()
    reg_pltfm_elm = pd_client_browser.find_element_by_id("link_register_platform")
    reg_pltfm_elm.click()
    time.sleep(1)
    
    # Step 3: input the information for platform registering 
    pd_browser_map = PD_Common.Register_Platfrom_Frame_UIMap(pd_client_browser)
    ip_register_input = pd_browser_map.get_ip_register_input()
    ip_register_input.send_keys("172.24.23.111")
    platform_name_input = pd_browser_map.get_platform_name_input()
    platform_name_input.send_keys("PLTFM_AUTO_TEST")
    
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
    #win.set_foreground()
    result_status = True
    try:
        SendKeys.SendKeys(lic_file_path)
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
        submit_btn.click()
        time.sleep(100)
        #pd_client_browser.close()
        print("Test pass")
    except:
        #alert = pd_client_browser.switch_to_window(window_name)
        js = '''html = document.getElementsByTagName('html')[0];
              return html.outerHTML;'''
        #html = alert.
        #print(html)
        
        parent_h = pd_client_browser.current_window_handle
        # click on the link that opens a new window
        handles = pd_client_browser.window_handles # before the pop-up window closes
        #handles.remove(parent_h)
        pd_client_browser.switch_to_window(handles.pop())
        #pd_client_browser.find_element_by_id("file").send_keys("abc")
         
        # do stuff in the popup
        #pd_client_browser
        # popup window closes
        pd_client_browser.switch_to_window(parent_h)
        pd_client_browser.close()
        pd_client_browser.switch_to_default_content()
        pd_client_browser.quit()
        
    

    