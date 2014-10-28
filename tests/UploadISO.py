# -*- coding: utf-8 -*-
'''
Created on 2014年7月29日

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
from Common.Messages import Messages
from Common.TestSpeedControl import TestSpeedControl
from Common.UIMap.Main_Browser_UIMap import Main_Browser_UIMap
from Common.UIMap.Platform_Summary_UIMap import Platform_Summary_UIMap
from Common.UIMap.Platform_Tree import Platform_Tree
from Common.UIMap.Register_Platfrom_Frame_UIMap import Register_Platfrom_Frame_UIMap
from Common.UIMap.Upload_ISO_UIMap import Upload_ISO_UIMap
from Common.Utils import PD_DebugLog


class UploadISO(Basejob):
    
    def setUp(self):
        # 继承父类Basejob，调用环境设置过程
        # 设置了日志输出文件接口：PD_DebugLog.xxx
        # 浏览器对象使用self.driver
        PD_DebugLog.debug_print("Call the parent method setUp")
        Basejob.setUp(self)

   
    
    def test_upload_iso(self):
        u'''注册平台 后,需要上传ISO镜像用于安装虚拟机'''
        
        u'''？？？平台注册后，有什么标志可以用来检测判断已经成功注册'''
        # Step 1: 登陆PD Web界面（用户名密码在配置文件tests-shared.cfg）
        PD_DebugLog.stepinfo(Messages.LOGIN_POWERDIRECTOR) #"Login PowerDirector"
        pd_client_browser = self.driver
        pd_client_browser.implicitly_wait(30)
        pd_client_browser.maximize_window()
        
        # Login and pass in with username, password, server and port
        self.pd_login()
        
        # Step 2: 选择上传镜像快捷按钮
        print("select and click the upload image button")
        PD_DebugLog.stepinfo(Messages.SELECT_CLICK_UPLOAD_IMG)
        pd_browser_main_map = Main_Browser_UIMap(pd_client_browser)
        upload_iso_btn = pd_browser_main_map.get_upload_iso_btn()
        upload_iso_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 3: verify the text of the header in the popup window 
        pd_register_vg_uimap = Upload_ISO_UIMap(pd_client_browser)
        expect_title = u"上传镜像"
        print("The title is: " + pd_register_vg_uimap.get_header().text)
        assert expect_title == pd_register_vg_uimap.get_header().text
        time.sleep(1)
            
        # Step 4: input the image name    
        image_name_input = pd_register_vg_uimap.get_image_name_input()
        image_name_input.send_keys('E:\\VMWare\\ubuntu_server\\start-download.iso')
        
        # Step 5: select iso radio button
        # ... the default selection is iso ...
        next_btn = pd_register_vg_uimap.get_next_button()
        time.sleep(1)
    
        # Step 6: select Toolkit 
        # ... default Toolkit ...
        time.sleep(1)  
        
        # Step 7: select OS name 
        pd_register_vg_uimap.select_osname_by_name("IBM ToolKit v54")
        time.sleep(1)
    
      
        next_btn.click()
        time.sleep(0.5)