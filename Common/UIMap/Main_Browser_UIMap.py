# -*- coding: utf-8 -*-
'''
Created on 2014年7月11日

@author: stm
'''
from selenium.webdriver.common.by import By
from Common.Utils import PD_DebugLog

class Main_Browser_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    PLATFORM, STORAGE, IMAGE, NETWORK, WORDLOAD = range(1, 6)
    LeftPanelID = 'leftpanel'
    
    def __init__(self, driver):
        self.driver = driver       
        
    def get_register_platform_btn(self):
        '''
        get the register platform button element
        '''
        return self.driver.find_element_by_id("link_register_platform")
    
    def get_create_vm_btn(self):
        '''
        get the create virtual machine button element
        '''
        return self.driver.find_element_by_id("link_create_vm")
    
    def get_upload_iso_btn(self):
        '''
        get the upload iso button element
        '''
        return self.driver.find_element_by_id("link_upload_os")
    
    def get_register_vol_btn(self):
        '''
        get the register volume button element
        '''
        return self.driver.find_element_by_id("link_register_volume") 
    
    def get_current_task_btn(self):
        '''
        get the current task button show the tasks
        '''
        return self.driver.find_element_by_id("btn_toggle_tasks")   
    
    def get_popup_tasks(self):
        '''
        popup the task frame window
        '''
        return self.driver.find_element_by_id("popup_tasks")

    def switch_to_default_content(self):
        self.driver.switch_to_default_content()
        
    def get_tab_from_leftpanel(self, tab_idx):
        '''
        get the tab element for platform resource
        '''
        # //*[@id="tab"]/li[2]/a
        tab = self.driver.find_element(By.XPATH, '//*[@id="tab"]/li[%d]/a' % tab_idx )
        #tab = tab_elemts.find_elements(By.XPATH, '//li[%d]' % (tab_idx))
        #xpath_ptn = '//li[%d]' % (tab_idx)
        # /html/body/div[2]/div/ul/li[4]
        # tab_elmt = ta#tab_elemts[tab_idx-1]
        if PD_DebugLog.DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The tab text is: " + tab.text)
        return tab
    
    def get_platform_resource_tab(self):
        return self.get_tab_from_leftpanel(Main_Browser_UIMap.PLATFORM)
    
    def get_storage_resource_tab(self):
        return self.get_tab_from_leftpanel(Main_Browser_UIMap.STORAGE)
    
    def get_image_library_tab(self):
        return self.get_tab_from_leftpanel(Main_Browser_UIMap.IMAGE)
    
    def get_network_resource_tab(self):
        return self.get_tab_from_leftpanel(Main_Browser_UIMap.NETWORK)
    
    def get_workload_resource_tab(self):
        return self.get_tab_from_leftpanel(Main_Browser_UIMap.WORDLOAD)
    
    def is_tab_current_selected(self, tab_idx):
        '''
        return bool value to represent whether the tab is current selected
        '''
        cur_selected = False
        tab_elm = self.get_tab_from_leftpanel(tab_idx)
        attr = tab_elm.get_attribute('class')
        if PD_DebugLog.DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The current tab attribute is: " + attr)
        if 'current' == attr:
            cur_selected = True
            
        return cur_selected
            
    def get_submenu_tree(self, submenu_idx):
        ##platform_tree //*[@id="pane"]/div[1]
        # //*[@id="pane"]/div[1]/ul/li
        left_panel = self.driver.find_element(By.ID, Main_Browser_UIMap.LeftPanelID)
        xpath = '//*[@id="pane"]/div[%d]/ul/li/ul/li' % (submenu_idx)
        submenu = left_panel.find_element(By.XPATH, xpath)
        if PD_DebugLog.DEBUG_LOG_PRINT:
            if submenu is list:
                for menu in submenu:
                    PD_DebugLog.debug_print("The sub menu text is: " + menu.text)
            else:
                PD_DebugLog.debug_print("The sub menu text is: " + submenu.text)
            
        return submenu
            
    def get_platform_sub_menu_tree(self):
        return self.get_submenu_tree(Main_Browser_UIMap.PLATFORM)
    
    def get_storage_sub_menu_tree(self):
        return self.get_submenu_tree(Main_Browser_UIMap.STORAGE)
    
    def get_image_sub_menu_tree(self):
        return self.get_submenu_tree(Main_Browser_UIMap.IMAGE)
        
    def get_workload_sub_menu_tree(self):
        return self.get_submenu_tree(Main_Browser_UIMap.WORDLOAD)
    
    def get_sub_menu_tree_title(self, tabid):
        # //*[@id="pane"]/div[%d]/ul/li/span
        # /html/body/div[2]/div/div[2]/div[%d]/ul/li/span
        left_panel = self.driver.find_element(By.ID, Main_Browser_UIMap.LeftPanelID)
        xpath = '//*[@id="pane"]/div[%d]/ul/li/span' % (tabid)
        submenu = left_panel.find_element(By.XPATH, xpath)
        if PD_DebugLog.DEBUG_LOG_PRINT:
            if submenu is list:
                for menu in submenu:
                    PD_DebugLog.debug_print("The sub menu text is: " + menu.text)
            else:
                PD_DebugLog.debug_print("The sub menu text is: " + submenu.text)
            
        return submenu.text
