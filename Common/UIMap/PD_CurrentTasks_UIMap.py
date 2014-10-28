# -*- coding: utf-8 -*-
'''
Created on 2014��10��15��

@author: stm
'''
from selenium.webdriver.common.by import By
import re
from Common.Utils.PD_DebugLog import DEBUG_LOG_PRINT
from Common.Utils import PD_DebugLog

class PD_CurrentTasks_UIMap(object):
    """
    Map the UI elements in current task popup frame.
    Such as the progress bar, task name, percentage etc.
    """
    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.frame("_tasks")        
        
    def get_task_table(self):
        '''
        get the task table element
        '''
        return self.driver.find_element(By.ID, "tasktable")
    
    def get_task_summary(self):
        '''
        get the task table element
        '''
        table_elm = self.driver.find_element(By.ID, "tasktable")
        summary_text = table_elm.get_attribute("summary")
        return summary_text
    
    def get_task_count(self):
        '''
        get the task table element
        '''
        summary_text = self.get_task_summary()
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("Summary text is: " + summary_text)
        ptn = re.compile(r'\d+')
        result = re.findall(ptn, summary_text)
        count = result[0]
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The count in summary is: " + count)
        return count
    
    def get_task_name(self):
        '''
        get the task name for the table row0 field 0
        '''
        table_elm = self.get_task_table()
        return table_elm.find_element(By.XPATH, 
                               '//tr[1]/td[1]/span').text
    
    def get_task_id(self, vm_name):
        '''
        '''
        table_elm = self.get_task_table()
        ret_val = 0
        
        task_count = int(self.get_task_count())
        for tid in range(1, task_count+1):
            vm_name_in_task = table_elm.find_element(By.XPATH, 
                                  '//tr[1]/td[2]/span[1]').text
            vm_name_in_task = vm_name_in_task.split(':')[1].strip()
            if DEBUG_LOG_PRINT:
                PD_DebugLog.debug_print("task name " + vm_name_in_task)
                
            if vm_name == vm_name_in_task:
                ret_val = tid + 1
                break
        
        return ret_val
        
    def get_task_percentage(self, task_idx):
        '''
        get the task name for the table row0 field 0
        '''
        table_elm = self.get_task_table()
        xpath_str = '//tr[%d]/td[3]/div/div[2]' % (task_idx)
        elem = table_elm.find_element(By.XPATH, xpath_str)
        percentage_text = elem.text
        ptn = re.compile(r'\d+')
        result = re.findall(ptn, percentage_text)
        percentage = result[0]
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("the percentage text is " + percentage_text)
        return percentage


    def get_task_starttime(self, task_idx):
        '''
        get the task name for the table row0 field 0
        '''
        table_elm = self.get_task_table()
        xpath_str = '//tr[%d]/td[1]/span[2]' % (task_idx)
        elem = table_elm.find_element(By.XPATH, xpath_str)
        starttime_text = elem.text

        return starttime_text

    
    def get_history_task_link(self):
        '''
        get the history task link button
        '''
        return self.driver.find_element(By.ID, 'link_task_history')
