# -*- coding: utf-8 -*-
'''
Created on 2014��10��15��

@author: stm
'''
from selenium.webdriver.common.by import By
from Common.Utils.PD_DebugLog import DEBUG_LOG_PRINT
import re
from Common.Utils import PD_DebugLog

class PD_HistoryTasks_UIMap(object):
    """
    Map the UI elements in current task popup frame.
    Such as the progress bar, task name, percentage etc.
    """
    def __init__(self, driver):
        self.driver = driver      
        
    def get_task_table(self):
        '''
        get the task table element
        '''
        return self.driver.find_element(By.ID, "task_table")
    
    def get_history_tasks_count(self):
        '''
        get all the history tasks count
        '''
        task_status_text = self.driver.find_element(By.XPATH, 
                            "/html/body/div/div[2]/div[6]/div[1]/div[6]/div[6]/span").text
        if (DEBUG_LOG_PRINT):
            PD_DebugLog.debug_print("History task status:" +  task_status_text)
        
        ptn = re.compile(r'\d+')      
        count = re.findall(ptn, task_status_text)
        PD_DebugLog.debug_print("count is: " + count)
        return int(count)
        
    def get_task_description(self, task_type, task_target):
        '''
        get the task name for the table row0 field 0
        '''
        table_elm = self.get_task_table()
        result = ''
        desc = ''
        for rowid in range(1, 10):
            xpath_str = '//tbody/tr[%d]/td[1]/div' % (rowid)
            elem = table_elm.find_element(By.XPATH, xpath_str)
            task_type_text = elem.text
            PD_DebugLog.debug_print("Task type is: " + task_type_text)
            xpath_str = '//tbody/tr[%d]/td[4]/div' % (rowid)
            elem = table_elm.find_element(By.XPATH, xpath_str)
            task_target_text = elem.text
            PD_DebugLog.debug_print("Task type is: " + task_target_text)
            
            if task_type == task_type_text and task_target == task_target_text:
                xpath_str = '//tbody/tr[%d]/td[6]/div' % (rowid)
                elem = table_elm.find_element(By.XPATH, xpath_str)
                result = elem.text
                PD_DebugLog.debug_print("Get the task status: " + result)
                
                desc_xpath_str = '//tbody/tr[%d]/td[7]/div' % (rowid)
                elem = table_elm.find_element(By.XPATH, desc_xpath_str)
                desc = elem.text
                PD_DebugLog.debug_print("Get the task status description: " + desc)

        return result, desc

        