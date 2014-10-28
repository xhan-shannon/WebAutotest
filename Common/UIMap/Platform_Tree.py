# -*- coding: utf-8 -*-
'''
Created on 2014年7月14日

@author: stm
'''
import time

from selenium.selenium import selenium

from Common.UIMap import Platform_Summary_UIMap
from Common.Utils import PD_DebugLog


class Platform_Tree(object):
    '''
    To parse the platform tree

    <ul id="platform_tree_1_ul" class="level0 ">
       <li id="platform_tree_2" class="level1" tabindex="0" hidefocus="true" treenode="">
          <span id="platform_tree_2_switch" title="" class="button level1 switch center_close" treenode_switch=""></span>
          <a id="platform_tree_2_a" class="level1" treenode_a="" onclick="" href="/PlatformAction.do?method=toPlatformOverview&amp;platformPcid=4e9676b0-0ea4-41c6-bb23-24a62c0abdff" target="_stage" style="" title="PLTFM_AUTO_TEST">
             <span id="platform_tree_2_ico" title="" treenode_ico="" class="button ico_close" style="background:url(/images/icons/16x16/platform.png) 0 0 no-repeat;"></span>
             <span id="platform_tree_2_span">PLTFM_AUTO_TEST</span>
          </a>
       </li>
       <li id="platform_tree_3" class="level1" tabindex="0" hidefocus="true" treenode="">
          <span id="platform_tree_3_switch" title="" class="button level1 switch bottom_close" treenode_switch=""></span>
          <a id="platform_tree_3_a" class="level1" treenode_a="" onclick="" href="/PlatformAction.do?method=toPlatformOverview&amp;platformPcid=63c94220-356e-4ddf-902a-ab44a3718992" target="_stage" style="" title="PLATFORM_AUTO_IVM111">
             <span id="platform_tree_3_ico" title="" treenode_ico="" class="button ico_close" style="background:url(/images/icons/16x16/platform.png) 0 0 no-repeat;"></span>
             <span id="platform_tree_3_span">PLATFORM_AUTO_IVM111</span>
          </a>
       </li>
    </ul>
    
    '''

    
    def get_tree_node_elemt_title(self, node):
        '''
        Get the node element title in a tree.
        '''
        
        # //*[@id="platform_tree_1_span"]
        xpath = './/a/span[2]'
        title_text_elmt = node.find_element_by_xpath(xpath)
        title_text = title_text_elmt.text
        title_text = unicode(title_text.strip())
        return title_text
    
    
    def __init__(self, driver, root_elemt):
        '''
        Constructor
        '''
        self.driver = driver
        self.root = root_elemt
        expected_root_title = "DataCenter"
        PD_DebugLog.debug_print("The expected root title is: " + expected_root_title)
        self.platform_total_num = 0
        self.platform_summary = None
        
        root_elemt_title = self.get_tree_node_elemt_title(self.root)
        PD_DebugLog.debug_print("The fetched root title is: " + root_elemt_title)
        assert(expected_root_title == root_elemt_title)
        
    def get_platform_item(self, index):
        '''
        Get the platform item node
        '''
        assert(index < self.platform_total_num)
        xpath = './/ul/li[%d]' % (index + 1)
        item = self.root.find_element_by_xpath(xpath)
        
        return item
        
    def get_platform_name(self, index):
        '''
        Get the platform name
        '''
        item = self.get_platform_item(index)
        platform_name = self.get_tree_node_elemt_title(item)
        return platform_name
    
    def get_platform_count(self):
        '''
        Get the platform total number
        '''
        platform_items = self.root.find_elements_by_xpath(".//ul/li")
        count = len(platform_items)
        self.platform_total_num = count
        return self.platform_total_num

    
    def enter_platform_summary_page(self, index):
        ''' click the platform node item, and switch the summary page '''
        PD_DebugLog.debug_print("To enter the platform summary page")
        elem = self.get_platform_item(index)
        PD_DebugLog.debug_print(str(elem))
        PD_DebugLog.debug_print("Get the platform node in the left tree")
        #xpath = './/a/span[1]'
        #elem_ico = elem.find_element_by_xpath(xpath)
        #elem_ico.click()
        
        PD_DebugLog.debug_print("Click the platform node")
        time.sleep(1)
        xpath = './/a/span[2]'
        elem.find_element_by_xpath(xpath).click()
        PD_DebugLog.debug_print("Get the second platform node and click")
        time.sleep(1)
        PD_DebugLog.debug_print(unicode(self.driver.page_source))
        
        #self.driver.switch_to_default_content()
        # /html/body/div[2]/div[2]/iframe
        # /html/body/div/div[2]/div/iframe
        #self.driver.switch_to_frame('_summary')
        #time.sleep(1)
        #PD_DebugLog.debug_print(unicode(self.driver.page_source))
        
        # /html/body/div/div[2]/div/iframe
        time.sleep(2)
        self.platform_summary = Platform_Summary_UIMap.Platform_Summary_UIMap(self.driver)

    
    def get_platform_ip(self):
        '''Get the platform ip from the ip page '''
        
        ip_text = ''
        if self.platform_summary:
            ip_text = self.platform_summary.get_platform_ip()
            
        if PD_DebugLog.DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The IP text is: " + ip_text)
        return ip_text
    
    
    
    
        
        
        
        
