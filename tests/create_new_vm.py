# -*- coding: utf-8 -*-
'''
Created on 2014年5月19日
Create new VM
@author: hanxm
'''

import os
import time

import PD_Common
import PD_Login
import PD_CurrentTasks


TEST_SPEED  = 3 
SLEEP_BETW_CLICK = 1

if __name__ == '__main__':
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
    print("Login PowerDirector")
    pd_client_browser = PD_Login.login("admin", "123456", "172.24.23.111", "8080")
    pd_client_browser.maximize_window()
    
    # Step 2: Click the create virtual machine button
    print("select and click the create virtual machine button")
    pd_client_browser.implicitly_wait(30)
    pd_browser_main_map = PD_Common.Main_Browser_UIMap(pd_client_browser)
    create_vm_btn = pd_browser_main_map.get_create_vm_btn()
    time.sleep(TEST_SPEED)
    create_vm_btn.click()
    time.sleep(SLEEP_BETW_CLICK)
    
    # Step 3: verify the text of the header in the popup window 
    pd_create_vm_uimap = PD_Common.Create_VM_UIMap(pd_client_browser)
    expect_title = "创建虚拟机"
    print("The title is: " + pd_create_vm_uimap.get_header().text)
    #assert expect_title == pd_create_vm_uimap.get_header().text
    time.sleep(TEST_SPEED)
        
    # Step 4: click the next button
    next_btn = pd_create_vm_uimap.get_next_button()
    time.sleep(TEST_SPEED)
    next_btn.click()
    time.sleep(SLEEP_BETW_CLICK)

    # Step 5: input the virtual machine name (in Page 2:vmname)
    vm_name_input = pd_create_vm_uimap.get_vm_name_input()
    vm_name_input.send_keys(vm_name)
    time.sleep(TEST_SPEED)
    next_btn.click()
    time.sleep(SLEEP_BETW_CLICK)  
    
    # Step 6: select one image (in Page 3:image)
    from_template_rdio_btn = pd_create_vm_uimap.get_template_radio_btn()
    from_template_rdio_btn.click()
    pd_create_vm_uimap.select_template_from_table_by_name("redhat6.4")
    time.sleep(TEST_SPEED)
    next_btn.click()
    time.sleep(SLEEP_BETW_CLICK)
    
    # Step 7: edit cpu configuration (in Page 4:cpu)
    next_btn.click()
    time.sleep(TEST_SPEED)
    
    # Step 8: edit memory configuration (in Page 5: memory)
    next_btn.click()
    time.sleep(TEST_SPEED)
    
    # Step 9: edit storage configuration (in Page 6: storage)
    next_btn.click()
    time.sleep(TEST_SPEED)
    
    # Step 10: edit network configuration (in Page 7: network)
    next_btn.click()
    time.sleep(TEST_SPEED)
    
    # Step 11: edit network configuration (in Page 8: confirmation)
    confirm_btn = pd_create_vm_uimap.get_confirm_button()
    time.sleep(TEST_SPEED)
    confirm_btn.click()
    time.sleep(SLEEP_BETW_CLICK)
    
    # Step 12: to check task status and wait the task finishes
    # if popup_task is not open, click the button again
    pd_browser_main_map.switch_to_default_content()
    current_tasks_btn = pd_browser_main_map.get_current_task_btn()
    current_tasks_btn.click()
    time.sleep(SLEEP_BETW_CLICK)
    tasks_popup = pd_browser_main_map.get_popup_tasks()
    tasks_popup_cls_attr = tasks_popup.get_attribute("class")
    print("The current task: " + tasks_popup_cls_attr)
    if not "open-state" in tasks_popup_cls_attr:
        # click the button again
        current_tasks_btn.click()
        time.sleep(SLEEP_BETW_CLICK)
        
    # Step 13: show the task name
    pd_browser_current_task_map = PD_CurrentTasks.PD_CurrentTasks_UIMap(pd_client_browser)
    #task_name_txt = pd_browser_current_task_map.get_task_name()
    tasks_count = int(pd_browser_current_task_map.get_task_count())
    if tasks_count <= 0:
        print("There is no tasks")
        pd_client_browser.close()
    else:
        summary_text = pd_browser_current_task_map.get_task_summary()
        print("The task summary is : " + summary_text)
        
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
            print("The test finishes GOOD")
        else:
            print("The test finishes FAILED")

    