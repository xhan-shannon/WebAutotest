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
from Common.UIMap.Create_VM_UIMap import Create_VM_UIMap
from Common.UIMap.PD_CurrentTasks_UIMap import PD_CurrentTasks_UIMap


class CreateVM(Basejob):
    def __init__(self, methodName, need_config=True):
        Basejob.__init__(self, methodName, need_config)
    
    def setUp(self):
        # 继承父类Basejob，调用环境设置过程
        # 设置了日志输出文件接口：PD_DebugLog.xxx
        # 浏览器对象使用self.driver
        PD_DebugLog.debug_print("Call the parent method setUp")
        Basejob.setUp(self)


    def test_create_vm_from_image(self):
        u'''
                         安装PD2.5后，在PDHelper中配置了镜像库地址；接着做“注册平台”、“注册”
                         之后可以进行安装虚拟机
         '''
        
        '''
        Create virtual machine 
        In demo, create from a template
        Need step1 to step13, 
        At last the steps are for tasks checking
        '''
        
        # The id starts from 1.
        vm_id = 4   
        vm_name = "AutoTest_VM%02d" % vm_id 
        
        # Step 1: Login and pass in with username, password, server and port
        self.pd_login()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        pd_client_browser = self.driver
        
        # Step 2: Click the create virtual machine button
        PD_DebugLog.debug_print("select and click the create virtual machine button")

        pd_browser_main_map = Main_Browser_UIMap(pd_client_browser)
        create_vm_btn = pd_browser_main_map.get_create_vm_btn()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        create_vm_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 3: verify the text of the header in the popup window 
        pd_create_vm_uimap = Create_VM_UIMap(pd_client_browser)
        expect_title = u"创建虚拟机"
        PD_DebugLog.debug_print("The title is: " + pd_create_vm_uimap.get_header().text)
        #assert expect_title == pd_create_vm_uimap.get_header().text
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 4: click the next button
        next_btn = pd_create_vm_uimap.get_next_button()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
    
        # Step 5: input the virtual machine name (in Page 2:vmname)
        vm_name_input = pd_create_vm_uimap.get_vm_name_input()
        vm_name_input.send_keys(vm_name)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)  
        
        # Step 6: select one image (in Page 3:image)
        from_template_rdio_btn = pd_create_vm_uimap.get_template_radio_btn()
        from_template_rdio_btn.click()
        
        # TODO: add parameters template_image_name = redhat6.4
        # high priority to use the parameter from command line
        # then use the value from cfg file
        #
        image_template_name = self.config.get("redhat_normal_images", "image_template_name")
        PD_DebugLog.debug_print("The template image name is : " + image_template_name)
        pd_create_vm_uimap.select_template_from_table_by_name(image_template_name)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 7: edit cpu configuration (in Page 4:cpu)
        
        # click the cpu type radio button
        cpu_type_rdobtn = pd_create_vm_uimap.get_shared_cpu_type_radio_btn()
        cpu_type_rdobtn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        
        # TODO:
        # need get an algorithm to calculate the cpu units number and vm cpu number
        cpu_num_min_value = '0.2'
        cpu_num_expect_value = '0.2'
        cpu_num_max_value = '0.2'
        
        cpu_num_min_input_elem = pd_create_vm_uimap.get_cpu_num_min_input_elem()
        cpu_num_min_input_elem.clear()
        cpu_num_min_input_elem.send_keys(cpu_num_min_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        cpu_num_expect_input_elem = pd_create_vm_uimap.get_cpu_num_expect_input_elem()
        cpu_num_expect_input_elem.clear()
        cpu_num_expect_input_elem.send_keys(cpu_num_expect_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        cpu_num_max_input_elem = pd_create_vm_uimap.get_cpu_num_max_input_elem()
        cpu_num_max_input_elem.clear()
        cpu_num_max_input_elem.send_keys(cpu_num_max_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        
        vmcpu_num_min_value = '2'
        vmcpu_num_expect_value = '2'
        vmcpu_num_max_value = '2'
        
        vmcpu_num_min_input_elem = pd_create_vm_uimap.get_vmcpu_num_min_input_elem()
        vmcpu_num_min_input_elem.clear()
        vmcpu_num_min_input_elem.send_keys(vmcpu_num_min_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        vmcpu_num_expect_input_elem = pd_create_vm_uimap.get_vmcpu_num_expect_input_elem()
        vmcpu_num_expect_input_elem.clear()
        vmcpu_num_expect_input_elem.send_keys(vmcpu_num_expect_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        vmcpu_num_max_input_elem = pd_create_vm_uimap.get_vmcpu_num_max_input_elem()
        vmcpu_num_max_input_elem.clear()
        vmcpu_num_max_input_elem.send_keys(vmcpu_num_max_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 8: edit memory configuration (in Page 5: memory)
        mem_unit ="GB"
        pd_create_vm_uimap.select_GB_unit()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        mem_num_min_value = '4'
        mem_num_avail_value = '4'
        mem_num_max_value = '4'
        
        mem_num_min_input_elem = pd_create_vm_uimap.get_mem_num_min_input_elem()
        mem_num_min_input_elem.clear()
        mem_num_min_input_elem.send_keys(mem_num_min_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        mem_num_expect_input_elem = pd_create_vm_uimap.get_mem_num_expect_input_elem()
        mem_num_expect_input_elem.clear()
        mem_num_expect_input_elem.send_keys(mem_num_avail_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        mem_num_max_input_elem = pd_create_vm_uimap.get_mem_num_max_input_elem()
        mem_num_max_input_elem.clear()
        mem_num_max_input_elem.send_keys(mem_num_max_value)
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
                
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 9: edit storage configuration (in Page 6: storage)
        pd_create_vm_uimap.select_storage_type_vg()
        pd_create_vm_uimap.select_volume_name_datavg()
        pd_create_vm_uimap.unselect_existed_volume()
        pd_create_vm_uimap.select_vol_size_GB_unit()
        pd_create_vm_uimap.set_storage_vol_size(20, 'GB')

        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
                
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 10: edit network configuration (in Page 7: network)
        pd_create_vm_uimap.assign_ip_addr(self.config.get('redhat_normal_images', 'ip_addr'))
        pd_create_vm_uimap.assign_submask(self.config.get('redhat_normal_images', 'submask'))
        pd_create_vm_uimap.assign_gateway(self.config.get('redhat_normal_images', 'gateway'))
        pd_create_vm_uimap.assign_dns(self.config.get('redhat_normal_images', 'dns'))
        pd_create_vm_uimap.assign_slavedns(self.config.get('redhat_normal_images', 'slavedns'))
        pd_create_vm_uimap.assign_vlan(self.config.get('redhat_normal_images', 'vlanid1'))
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        next_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 11: edit network configuration (in Page 8: confirmation)
        confirm_btn = pd_create_vm_uimap.get_confirm_button()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        confirm_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 12: to check task status and wait the task finishes
        # if popup_task is not open, click the button again
        pd_browser_main_map.switch_to_default_content()
        current_tasks_btn = pd_browser_main_map.get_current_task_btn()
        current_tasks_btn.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        tasks_popup = pd_browser_main_map.get_popup_tasks()
        tasks_popup_cls_attr = tasks_popup.get_attribute("class")
        PD_DebugLog.debug_print("The current task: " + tasks_popup_cls_attr)
        if not "open-state" in tasks_popup_cls_attr:
            # click the button again
            current_tasks_btn.click()
            time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 13: show the task name
        pd_browser_current_task_map = PD_CurrentTasks_UIMap(pd_client_browser)
        #task_name_txt = pd_browser_current_task_map.get_task_name()
        tasks_count = int(pd_browser_current_task_map.get_task_count())
        if tasks_count <= 0:
            PD_DebugLog.debug_print("There is no tasks")
            pd_client_browser.close()
        else:
            summary_text = pd_browser_current_task_map.get_task_summary()
            PD_DebugLog.debug_print("The task summary is : " + summary_text)
            
            task_id = pd_browser_current_task_map.get_task_id(vm_name)       
            poll_time = 0.5
            timeout = 7600
            time_passed = 0
            while time_passed < timeout:
                time.sleep(poll_time)
                progress_bar_percentage = int(pd_browser_current_task_map.get_task_percentage(task_id))
                if progress_bar_percentage <= 100:
                    time_passed = time_passed + poll_time
                else:
                    timer_expired = False
                    break 
            
            task_result = pd_browser_current_task_map.get_taask_result()
            if task_result == "SUCCESS":
                PD_DebugLog.debug_print("The test finishes GOOD")
            else:
                PD_DebugLog.debug_print("The test finishes FAILED")