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
from Common.Basejob import Basejob
from Common.Utils import PD_DebugLog
from Common.Messages import Messages
from Common.UIMap.Main_Browser_UIMap import Main_Browser_UIMap
from Common.TestSpeedControl import TestSpeedControl

from Common.UIMap.Register_Image_Frame_UIMap import Register_Image_Frame_UIMap
from Common.Utils import utils_misc
from Common.UIMap.Image_Summary_UIMap import ImageLib_Summary_UIMap
from Common.TestError import ElemNotExisted






class RegisterIMG(Basejob):
    
    def setUp(self):
        # 继承父类Basejob，调用环境设置过程
        # 设置了日志输出文件接口：PD_DebugLog.xxx
        # 浏览器对象使用self.driver
        PD_DebugLog.debug_print("Call the parent method setUp")
        Basejob.setUp(self)

   
    
    def test_register_image(self):
        u'''
                         在PDHelper中配置了‘镜像库’地址和共享目录
                         注册平台 后,注册模板镜像用于安装虚拟机
         '''
        register_image_config = utils_misc.readconfig(self.__class__.__name__)
            
        u'''？？？平台注册后，有什么标志可以用来检测判断已经成功注册'''
        # Step 1: 登陆PD Web界面（用户名密码在配置文件tests-shared.cfg）
        PD_DebugLog.stepinfo(Messages.LOGIN_POWERDIRECTOR) #"Login PowerDirector"
        pd_client_browser = self.driver
        pd_client_browser.implicitly_wait(30)
        pd_client_browser.maximize_window()
        
        # :输入用户名，密码 Login and pass in with username, password, server and port
        self.pd_login()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 2: 选择镜像库标签
        PD_DebugLog.stepinfo(Messages.IMAGE_LIB)
        PD_DebugLog.stepinfo(Messages.SELECT_CLICK_IMAGELIB_TAB)
        pd_browser_main_map = Main_Browser_UIMap(pd_client_browser)
        imagelib_tab = pd_browser_main_map.get_image_library_tab()
        imagelib_tab.click()
        
        # 确认当前页面已经切换到镜像库页面
        #　通过检查左侧树形标题/html/body/div[2]/div/div[2]/div[3]/ul/li/span
        expect_title = u"镜像"
        PD_DebugLog.info_print(u"期望在左侧树形面板标题获得“镜像”文本")
        got_title = pd_browser_main_map.get_sub_menu_tree_title(
                        Main_Browser_UIMap.IMAGE)
        
        PD_DebugLog.debug_print("expect_title: " + expect_title)
        PD_DebugLog.debug_print("got_title: " + got_title)
        assert expect_title == got_title
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 3: 选择镜像库标签->"注册镜像"链接
        pd_imagelib_summary_map = ImageLib_Summary_UIMap(pd_client_browser)
        pd_imagelib_summary_map.click_register_image_link()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 4: 在注册镜像对话框中输入镜像对应的目录名
        # Step 4: input the image or iso file name under the nfs template 
        #         directory.
        iso_image_file_name = register_image_config.get("images", "rh64_template_img")
        
        if not iso_image_file_name:
            iso_image_file_name = "RedHat_6.4_image"
        
        pd_image_register_uimap = Register_Image_Frame_UIMap(pd_client_browser)
        image_alias_input_elem = pd_image_register_uimap.get_image_alias_input()
        image_alias_input_elem.send_keys(iso_image_file_name)
        
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        image_location_input_elem = pd_image_register_uimap.get_image_file_location_input()
        image_location_input_elem.send_keys(iso_image_file_name)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 5: select file type as ISO or IMG
        # Step 5: 选择文件类型为ISO或IMG 
        file_type_img_radiobtn = pd_image_register_uimap.get_file_type_img_radiobtn()
        
        if not file_type_img_radiobtn:
            raise ElemNotExisted
        
        file_type_img_radiobtn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 6: select the proper OS type
        # Step 6: 选择合适的操作系统类型    
        os_type = register_image_config.get("images", "os_type")
        pd_image_register_uimap.select_ostype_by_value(os_type)
        
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        os_name = register_image_config.get("images", "os_name")
        try:
            pd_image_register_uimap.select_osname_by_value(os_name)
        except:
            register_isoimage_fail_file = "register_isoimage_fail_file.png"
            utils_misc.save_screenshot(self.driver, self.testcasedir, 
                                       register_isoimage_fail_file)
            
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 7: click submit
        # Step 7: 点击提交按钮
        submit_btn = pd_image_register_uimap.get_submit_btn()
        submit_btn.click()
        #time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 8: verify alert is present 
        # Step 8: 确认成功对话框弹出
        #time.sleep(3)  # 等待时间不能太短
            
        # wait to alert dialog pops up
        orig_window_handles = self.driver.window_handles
        
        time_out = 100
        curtime = 0
        
        # True:  return alert dialog
        # False: error message is returned 
        alert_reponse_returned = False  
        error_message_present = False
        while curtime < time_out:
            # to wait the response
            # determine if it gets the success response: alert dialog
            # or gets the error message.
            PD_DebugLog.debug_print("In the while loop: %d" % curtime)
            try:
                cur_window_handles = self.driver.window_handles
                PD_DebugLog.debug_print("The original windows number is: %d" % len(orig_window_handles))
                PD_DebugLog.debug_print("The current windows number is: %d" % len(cur_window_handles))
                
                if pd_image_register_uimap.is_notify_msg_present():
                    PD_DebugLog.debug_print("In is_notify_msg_present branch")
                    error_message_present = True
                    PD_DebugLog.debug_print("Found the error message")
                    break
                
                if pd_image_register_uimap.is_alert_present():
                #if len(orig_window_handles) != len(cur_window_handles):
                    PD_DebugLog.debug_print("In is_alert_present branch")
                    alert_reponse_returned = not alert_reponse_returned
                    PD_DebugLog.debug_print("Found the alert dialog")
                    break
                        
                if pd_image_register_uimap.is_loading_getvminfo():
                    PD_DebugLog.debug_print("In is_loading_getvminfo branch")
                    continue
            
            finally:
                time.sleep(0.2)
                curtime = curtime + 1
                
        self.assertTrue(alert_reponse_returned or error_message_present,
                        "Register ISO could not get the reponse in time.")
        
        if alert_reponse_returned or error_message_present: 
            if alert_reponse_returned:
                expectmsg = register_image_config.get("images", "response_register_img")
                PD_DebugLog.debug_print(expectmsg)
                expectmsg = u'注册成功'
                respmsg = pd_image_register_uimap.close_alert_and_get_its_text()
                respmsg = unicode(respmsg.strip())
                PD_DebugLog.info_print("Step info: " + 
                             "Got the response message, " +
                             respmsg )
                self.assertEqual(expectmsg, respmsg)
            else:
                respmsg = pd_image_register_uimap.get_notify_msg()
                respmsg = unicode(respmsg.strip())
                PD_DebugLog.debug_print("Step info: " + 
                             "Got the response message, " +
                             respmsg )
                self.assertFalse(error_message_present, respmsg)
        
                
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
    
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL) 

        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
      
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)