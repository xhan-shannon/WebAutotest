#!/usr/bin/python
# -*-coding: utf-8 -*-
'''
Created on 

@author: stm
'''

import time

import PD_Common
import PD_Login
import PD_CurrentTasks
import PD_Debug
import PD_SubmenuTree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

DEBUG_PRINT_LOG = False

DEBUG_PRINT_LOG = PD_Debug.PD_DEBUG_LOG

if __name__ == '__main__':
    
    vm_name = "AutoTest_VM21"
    
    # Step 1: Login and pass in with username, password, server and port
    print("Login PowerDirector")
    pd_client_browser = PD_Login.login("admin", "123456", "172.24.23.111", "8080")
    pd_client_browser.maximize_window()
    
    # Step 2: Make sure the host resource tab is selected
    print("click and select the host resource tab")
    pd_client_browser.implicitly_wait(3)
    pd_browser_main_map = PD_Common.Main_Browser_UIMap(pd_client_browser)
    platform_resource_tab = pd_browser_main_map.get_platform_resource_tab()
    platform_resource_tab.click()
    time.sleep(1)
    
    # Step 3: Got the directory tree frame and check all the levels
    # travel around the leaves elements
    sub_tree = pd_browser_main_map.get_platform_sub_menu_tree()
    sub_menu_tree_elem = sub_tree[0]
    platform_tree = PD_SubmenuTree.Submenu_Tree(sub_menu_tree_elem)
    if DEBUG_PRINT_LOG:
        print("The tree id is: " + platform_tree.get_submenu_tree_id())
    
    tree_node = PD_SubmenuTree.TreeNode(sub_menu_tree_elem)
    elemts = tree_node.get_all_child_nodes()
    fst_lvl_node_elm = elemts[0]
    fst_lvl_node = PD_SubmenuTree.TreeNode(fst_lvl_node_elm)
    print("First level child node text is :" + fst_lvl_node.get_node_title() )
    
#     fst_lvl_node.click()
#     time.sleep(1)
#     if fst_lvl_node.has_child_node():
#         scnd_lvl_node_elmts = fst_lvl_node.get_all_child_nodes()
#         scnd_lvl_node_elm = scnd_lvl_node_elmts[0]
#         scnd_lvl_node = PD_SubmenuTree.TreeNode(scnd_lvl_node_elm)
#         print("Second level child node text is :" + scnd_lvl_node.get_node_title() )
#     
#         scnd_lvl_node.click()
#         time.sleep(1)
#         thd_lvl_node_elmts = scnd_lvl_node.get_all_child_nodes()
#         thd_lvl_node_elm = thd_lvl_node_elmts[0]
#         thd_lvl_node = PD_SubmenuTree.TreeNode(thd_lvl_node_elm)
#         print("Third level child node text is :" + thd_lvl_node.get_node_title() )
#         
#         thd_lvl_node.click()
#         time.sleep(1)
#         fth_lvl_node_elmts = thd_lvl_node.get_all_child_nodes()
#         if fth_lvl_node_elmts:
#             fth_lvl_node_elm = fth_lvl_node_elmts[0]
#             fth_lvl_node = PD_SubmenuTree.TreeNode(fth_lvl_node_elm)
#             print("Third fourth child node text is :" + fth_lvl_node.get_node_title() )
#         
    
    #platform_tree.travel_around_child_nodes()
    
    elem = platform_tree.find_element_by_vmname(vm_name)
    if elem:
        elem_node = PD_SubmenuTree.TreeNode(elem[0])
        print("Find the elem, the title is " + elem_node.get_node_title())
        elem_node.click()
    #sub_menu_tree_elem.click()
    
    # //*[@id="actions"]/ul/li[4]
    time.sleep(20)
    
    pd_client_browser.close()

