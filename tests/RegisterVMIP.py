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
from Common.UIMap.Register_VM_IP_Frame_UIMap import Register_VM_IP_Frame_UIMap



class RegisterVMIP(Basejob):
    
    def __init__(self, methodName, need_config=True):
        Basejob.__init__(self, methodName, need_config)
        self.pd_browser_main_map = None
        self.pd_client_browser = None
       
    
    def setUp(self):
        # 继承父类Basejob，调用环境设置过程
        # 设置了日志输出文件接口：PD_DebugLog.xxx
        # 浏览器对象使用self.driver
        PD_DebugLog.info_print("Call the parent method setUp")
        Basejob.setUp(self)  
    
    
    def determine_ip_is_set(self):
        '''
        compare the ip between the target ip and the static label value
        '''
        #vm_summary_page = VM_Summary_UIMap(self.driver)
        vm_summary_page = VM_Summary_UIMap(self.pd_client_browser)
        got_ip = vm_summary_page.get_vm_ip()
        if got_ip == self.config.get("vm", "ip_addr"):
            return True
        else:
            return False
        
    
    def test_register_vm_ip_normally(self):
        u'''为指定的已经存在虚拟机登记IP地址'''
        #
        # The id starts from 1.
        vm_id = 4   
        vm_name = "AutoTest_VM%02d" % vm_id
        vm_name = "PD3_Cluster_VM123"
        host_name = "localhost"
        vm_name = "JAVA_VM62"
        
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
        
        vm_summary_page = self.vm_summary_page = VM_Summary_UIMap(pd_client_browser)
        
        # Step 4: expand the more actions bar
        
        vm_summary_page.expand_more_actions_bar()
        
        # Step 5: click Register IP button link
        vm_summary_page.click_register_IP_link()
        
        # Step 6: input the ip... value in the register ip form
        register_vm_ip_form = Register_VM_IP_Frame_UIMap(self.driver)
        register_vm_ip_form.get_ip_addr_input().send_keys("172.30.126.62")
        register_vm_ip_form.get_netmask_input().send_keys("255.255.255.0")
        register_vm_ip_form.get_gateway_input().send_keys("172.30.126.254")
        register_vm_ip_form.get_dns_input().send_keys("202.106.0.20")
        register_vm_ip_form.get_seconddns_input().send_keys("202.106.196.115")
        register_vm_ip_form.get_submit_btn().click()
        
        register_vm_ip_form.return_main_page()
        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        
        result = utils_misc.wait_for(self.determine_ip_is_set, 20, 1, 1, "The ip is not set successfully.")
        
        if not result:
            self.fail("The ip is not set successfully.")
        else:
            PD_DebugLog.info_print("The ip is set done.")
        
        
#         if not utils_misc.is_valid_ip(target_vm_ipaddr):
#             self.fail("Get VM IP failed")
#             
#         # Step 6: Check the vm current status, it would turn into "in shutdown progress"
#         ping_output = utils_misc.ping(target_vm_ipaddr)
#         PD_DebugLog.debug_print("Print the ping output : " + ping_output)
#         
#         if utils_misc.get_loss_ratio(ping_output) > 0:
#             self.fail("Ping failed" + ping_output)

        time.sleep(TestSpeedControl.TEST_STEP_INTERVAL)
        