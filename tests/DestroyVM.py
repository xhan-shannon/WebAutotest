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
from Common.PD_SubmenuTree import Submenu_Tree, TreeNode

from Common.UIMap.Register_Image_Frame_UIMap import Register_Image_Frame_UIMap
from Common.Utils import utils_misc
from Common.UIMap.Image_Summary_UIMap import ImageLib_Summary_UIMap
from Common.TestError import ElemNotExisted
from Common.UIMap.Create_VM_UIMap import Create_VM_UIMap
from Common.UIMap.PD_CurrentTasks_UIMap import PD_CurrentTasks_UIMap
from Common.UIMap.VM_Summary_UIMap import VM_Summary_UIMap
from Common.UIMap.PD_HistoryTasks_UIMap import PD_HistoryTasks_UIMap
from Common.UIMap.Remove_VM_Frame_UIMap import Remove_VM_Frame_UIMap


class DestroyVM(Basejob):
    
    def __init__(self, methodName, need_config=False):
        Basejob.__init__(self, methodName, need_config)
        self.pd_browser_main_map = None
        self.pd_client_browser = None
       
    
    def setUp(self):
        # 继承父类Basejob，调用环境设置过程
        # 设置了日志输出文件接口：PD_DebugLog.xxx
        # 浏览器对象使用self.driver
        PD_DebugLog.info_print("Call the parent method setUp")
        Basejob.setUp(self)


    def shutdown_task_appears(self):
        '''
        To test if there is new task item in current tasks list
        '''
        self.pd_browser_main_map.switch_to_default_content()
        current_tasks_btn = self.pd_browser_main_map.get_current_task_btn()
        current_tasks_btn.click()
        #time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        tasks_popup = self.pd_browser_main_map.get_popup_tasks()
        tasks_popup_cls_attr = tasks_popup.get_attribute("class")
        PD_DebugLog.debug_print("The current task: " + tasks_popup_cls_attr)
        if not "open-state" in tasks_popup_cls_attr:
            # click the button again
            current_tasks_btn.click()
            time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 13: show the task name
        pd_browser_current_task_map = PD_CurrentTasks_UIMap(self.pd_client_browser)
        #task_name_txt = pd_browser_current_task_map.get_task_name()
        tasks_count = int(pd_browser_current_task_map.get_task_count())
        if tasks_count <= 0:
            PD_DebugLog.debug_print("There is no tasks")
            return False
        else:
            summary_text = pd_browser_current_task_map.get_task_summary()
            PD_DebugLog.debug_print("The task summary is : " + summary_text)
            return True
            
    
    
    def get_task_starttime(self, task_type, vm_name, host_name):
        '''
        Now retrieve task info, the result is only task start time.
        '''
        self.pd_browser_main_map.switch_to_default_content()
        current_tasks_btn = self.pd_browser_main_map.get_current_task_btn()
        current_tasks_btn.click()
        #time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        tasks_popup = self.pd_browser_main_map.get_popup_tasks()
        tasks_popup_cls_attr = tasks_popup.get_attribute("class")
        PD_DebugLog.debug_print("The current task: " + tasks_popup_cls_attr)
        if not "open-state" in tasks_popup_cls_attr:
            # click the button again
            current_tasks_btn.click()
            #time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 13: show the task name
        pd_browser_current_task_map = PD_CurrentTasks_UIMap(self.pd_client_browser)
        #task_name_txt = pd_browser_current_task_map.get_task_name()
        task_idx = pd_browser_current_task_map.get_task_id(vm_name)
        
        info = pd_browser_current_task_map.get_task_starttime(task_idx)
        return info
    
    
    def shutdown_task_disappears(self):
        return not self.shutdown_task_appears()
    
    
    def get_task_status_from_history_task(self, task_type, vm_name, host_name, taskstarttime):
        '''
        Get task status from the history task list
        '''
        self.pd_browser_main_map.switch_to_default_content()
        current_tasks_btn = self.pd_browser_main_map.get_current_task_btn()
        current_tasks_btn.click()
        #time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        tasks_popup = self.pd_browser_main_map.get_popup_tasks()
        tasks_popup_cls_attr = tasks_popup.get_attribute("class")
        PD_DebugLog.debug_print("The current task: " + tasks_popup_cls_attr)
        if not "open-state" in tasks_popup_cls_attr:
            # click the button again
            current_tasks_btn.click()
            time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
            
        # Step 13: show the task name
        pd_browser_current_task_map = PD_CurrentTasks_UIMap(self.pd_client_browser)
        history_link_btn = pd_browser_current_task_map.get_history_task_link()
        
                
        now_handle = self.pd_client_browser.current_window_handle #得到当前窗口句柄
        history_link_btn.click()
        all_handles = self.pd_client_browser.window_handles #获取所有窗口句柄
        
        task_result = 'SUCCESS'
        for handle in all_handles:
            if handle != now_handle:
                self.pd_client_browser.switch_to_window(handle)
                time.sleep(1)
                
        # check the history log
        pd_browser_history_task_map = PD_HistoryTasks_UIMap(self.pd_client_browser)
        time.sleep(1)

        task_target = vm_name
        task_result, task_desc = pd_browser_history_task_map.get_task_description(
                              task_type, task_target)
        time.sleep(1)
        self.pd_client_browser.switch_to_window(now_handle)
         
        return task_result, task_desc       
        #if task_result == "SUCCESS":
        #    print("The test finishes GOOD")
        #else:
        #    print("The test finishes FAILED")
        
    
    def get_task_description_from_history_task(self, task_type, vm_name, host_name):
        '''
        Get the task fail description from the history task list.
        '''
    
    
    def test_destroy_vm_normally(self):
        u'''删除指定的已经存在虚拟机'''
        #
        # The id starts from 1.
        
        vm_name = "PD3_Cluster_VM123"
        host_name = "localhost"


        '''
        Find the virtual machine first,
        Then, decide if it is running.
        If yes, shutdown the virtual machine.
        The third is to delete it.
        And at the same to watch history or task bar to detect if the deletion is running or finished.  
        
        '''
        
        # Step 1: Login and pass in with username, password, server and port
        pd_client_browser = self.pd_login()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        self.pd_client_browser = pd_client_browser
        
        # Step 2: Make sure the host resource tab is selected
        PD_DebugLog.stepinfo("click and select the host resource tab")
        
        pd_browser_main_map = Main_Browser_UIMap(pd_client_browser)
        self.pd_browser_main_map = pd_browser_main_map
        
        platform_resource_tab = pd_browser_main_map.get_platform_resource_tab()
        platform_resource_tab.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        # Step 3: Got the directory tree frame and check all the levels
        # travel around the leaves elements
        sub_tree = pd_browser_main_map.get_platform_sub_menu_tree()
        
        if type(sub_tree) is list:
            sub_menu_tree_elem = sub_tree[0]
        else:
            sub_menu_tree_elem = sub_tree
            
        platform_tree = Submenu_Tree(sub_menu_tree_elem)
        
        PD_DebugLog.debug_print("The tree id is: " + platform_tree.get_submenu_tree_id())
        
        tree_node = TreeNode(sub_menu_tree_elem)
        elemts = tree_node.get_all_child_nodes()
        
        if type(elemts) is list:
            fst_lvl_node_elm = elemts[0]
        else:
            fst_lvl_node_elm = elemts
        fst_lvl_node = TreeNode(fst_lvl_node_elm)
        PD_DebugLog.info_print("First level child node text is :" + fst_lvl_node.get_node_title() )      
        
        #platform_tree.travel_around_child_nodes()
        utils_misc.set_script_timeout(pd_client_browser, 0.2)
        pd_client_browser.implicitly_wait(6)
        elem = platform_tree.find_element_by_vmname(vm_name)
        if elem:
            elem_node = TreeNode(elem[0])
            PD_DebugLog.info_print("Find the elem, the title is " + elem_node.get_node_title())
            elem_node.click()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        utils_misc.restore_script_timeout(pd_client_browser)
        
        vm_summary_page = VM_Summary_UIMap(pd_client_browser)
        
        #task_startup_abouttime = time.time()
        # The testcase running machine time is not same as the AIX machine under test.  
        vm_summary_page.execute_powerdown_system(True)
        
        # Step 4: Check the vm current status, it would turn into "in shutdown progress"
        check_return = utils_misc.wait_for(vm_summary_page.is_vm_in_shutdown_progress, 10, 0, 0.1, "Check if vm goes into shutdown status")
        self.assert_(check_return, "After execution of shutdown action, vm must go into 'in shutdown progess'")
        
        if check_return:
            # find the task item to get the item information: starttime, name and description
            # Then to watch when it disappears
            # The end, check it in the history of task to get the final status, success or fail.
            # If it failed, get the failure description.
            
            # Step 5: to check task status and wait the task finishes
            # if popup_task is not open, click the button again
            
            task_type = u'关闭虚拟机'
            utils_misc.wait_for(self.shutdown_task_appears, 10, 0, 0.1, "Shutdown vm task should appear in current tasks list")
            taskstarttime = self.get_task_starttime(task_type, vm_name, host_name)
            utils_misc.wait_for(self.shutdown_task_disappears, 10, 0, 0.1, "Shutdown vm task should finish and go into the history tasks list")
            status,fail_desc = self.get_task_status_from_history_task(task_type, vm_name, host_name, taskstarttime)

            if status == Messages.FAIL_STATUS_STR:
                self.fail("The task failed: " + fail_desc)
            else:
                PD_DebugLog.debug_print("The task finished successfully.")
                             
         
        # click the "remove vm" link from more actions bar
        vm_summary_page = self.vm_summary_page = VM_Summary_UIMap(pd_client_browser)
        
        # Step 4: expand the more actions bar
        vm_summary_page.expand_more_actions_bar()
        
        # Step 5: click Remove VM button link
        vm_summary_page.click_remove_vm_link()
        
        # Step 6: wait for the loading vminfo(loading_overlay_getvminfo) appears
        check_return = utils_misc.wait_for(vm_summary_page.is_loading_getvminfo(), 10, 0, 0.1, "Check if loading dialog shows")
        self.assert_(check_return, "After execution of shutdown action, vm must go into 'in shutdown progess'")
        
        # Step 6: check if the vm goes into deleting progress
        check_return = utils_misc.wait_for(vm_summary_page.is_vm_in_deleting_progress, 10, 0, 0.1, "Check if vm goes into shutdown status")
        self.assert_(check_return, "After execution of shutdown action, vm must go into 'in shutdown progess'")
        
        if check_return:
            # find the task item to get the item information: starttime, name and description
            # Then to watch when it disappears
            # The end, check it in the history of task to get the final status, success or fail.
            # If it failed, get the failure description.
            
            # Step 5: to check task status and wait the task finishes
            # if popup_task is not open, click the button again
            
            task_type = u'删除虚拟机'
            utils_misc.wait_for(self.shutdown_task_appears, 10, 0, 0.1, "Shutdown vm task should appear in current tasks list")
            taskstarttime = self.get_task_starttime(task_type, vm_name, host_name)
            utils_misc.wait_for(self.shutdown_task_disappears, 10, 0, 0.1, "Shutdown vm task should finish and go into the history tasks list")
            status,fail_desc = self.get_task_status_from_history_task(task_type, vm_name, host_name, taskstarttime)

            if status == Messages.FAIL_STATUS_STR:
                self.fail("The task failed: " + fail_desc)
            else:
                PD_DebugLog.debug_print("The task finished successfully.")
        
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        