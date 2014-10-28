# -*- coding: utf-8 -*-
'''
Created on 2014年5月19日

@author: hanxm
'''
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Common.Utils import utils_misc

try:
    from Common.Utils import PD_DebugLog
    DEBUG_LOG_PRINT = PD_DebugLog.PD_DEBUG_LOG
except:
    DEBUG_LOG_PRINT = False
    

class TreeNode(object):
    '''
    Represent the node information
    Example in the left panel
    '''
    
    def __init__(self, node):
        '''
        node is an element
        '''
        self.node = node
    
    def get_node_title(self):
        xpath = '//*[@id="%s"]/a/span[2]' % self.get_current_node_id()
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print(self.__class__.__name__ + "The xpath is : " + xpath)
        
        return self.node.find_element(By.XPATH, xpath).text
    
    def has_child_node(self):
        child_node_existed = False

        try:
            xpath = '//*[@id="%s"]/ul' % self.get_current_node_id()
            if DEBUG_LOG_PRINT:
                PD_DebugLog.debug_print("The xpath is : " + xpath)
            elemts = self.node.find_elements(By.XPATH, xpath)
            if elemts:
                child_node_existed = True
        except:
            child_node_existed = False
            
        return child_node_existed
    
    def get_current_node_id(self):     
        id_attr = self.node.get_attribute('id')
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print(self.__class__.__name__ + " The node is: " + id_attr)
            
        return id_attr
    
    def get_all_child_nodes(self):
        xpath = '//*[@id="%s"]/li' % self.get_current_node_id()
        if self.has_child_node():
            xpath = '//*[@id="%s"]/ul/li' % self.get_current_node_id()
        
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print(self.__class__.__name__ + ":" + \
                  "get_all_child_nodes" +  \
                  "The xpath is : " + xpath)
                  
        elemts = self.node.find_elements(By.XPATH, xpath)
        return elemts
        
    def is_closed(self):
        # check if the switch is closed
        
        xpath = '//*[@id="%s"]/span' % self.get_current_node_id()
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print(self.__class__.__name__ + "The xpath is : " + xpath)
        elem = self.node.find_element(By.XPATH, xpath)
        attr = elem.get_attribute('class')
        node_closed = attr.endwith('_close') 
            
        return node_closed
        
            
    def click(self):
        xpath = '//*[@id="%s"]/a/span[1]' % self.get_current_node_id()
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print(self.__class__.__name__ + "The xpath is : " + xpath)
        elm = self.node.find_element(By.XPATH, xpath)
        elm.click()
    
class Submenu_Tree(object):
    """
    Tree operations
    1. show the sublevel or child node information
    2. fold/unfold collapse/expand the tree nodes
    3. tree around the tree nodes 
    
    The final terminal node is like: 
    <li id="platform_tree_4" class="level3" tabindex="0" hidefocus="true" treenode="">
      <span id="platform_tree_4_switch" title="" class="button level3 switch center_docu" treenode_switch=""></span>
      <a id="platform_tree_4_a" class="level3" treenode_a="" onclick="" href="/VmAction.do?method=toVmOverview&amp;vmPcid=7705a417-01e7-4f88-8113-4363a1819b35" target="_stage" style="" title="AutoTest_VM01">
        <span id="platform_tree_4_ico" title="" treenode_ico="" class="button ico_docu" style="background:url(/images/icons/16x16/vm.png) 0 0 no-repeat;"</span>
        <span id="platform_tree_4_span">AutoTest_VM01</span>
      </a>
      </li>
    
    """
    PLATFORM, STORAGE, IMAGE, NETWORK, WORDLOAD = range(1, 6)
    LeftPanelID = 'leftpanel'
    
    def __init__(self, tree):
        self.tree = tree
                    
    def get_submenu_tree(self, submenu_idx):
        ##platform_tree //*[@id="pane"]/div[1]
        # //*[@id="pane"]/div[1]/ul/li
        left_panel = self.driver.find_element(By.ID, Submenu_Tree.LeftPanelID)
        xpath = '//div[%d]/ul/li/ul' % (submenu_idx)
        submenu = left_panel.find_element(By.XPATH, xpath)
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The sub menu text is: " + submenu.text)
            
        return submenu
            
    def get_submenu_tree_id(self):
        #ul_elm = self.tree.find_element(By.XPATH, '//li/ul')
        #if DEBUG_LOG_PRINT:
        #    PD_DebugLog.debug_print("The sub tree is: " + ul_elm.text)
        
        id_attr = self.tree.get_attribute('id')
        if DEBUG_LOG_PRINT:
            PD_DebugLog.debug_print("The tree id is: " + id_attr)
            
        return id_attr
    
    def travel_around_child_nodes(self, vmname=None, find_stop=True, expand_nodes=True):
        '''
        check if there is child node, if yes, walk through all the nodes
        '''       
        def _travel_all_nodes(tree_node, vmname, find_stop, expand_nodes):
            # /html/body/div[2]/div/div[2]/div/ul/li/ul/li/ul/li/ul/li/ul/li/a/span[2]
            # //*[@id="platform_tree_1_span"]
            # /html/body/div[2]/div/div[2]/div/ul/li/ul/li/a/span[2]
            current_node = TreeNode(tree_node)
            if DEBUG_LOG_PRINT:
                PD_DebugLog.debug_print("The current node text is: " + current_node.get_node_title())
 
            if expand_nodes:
                current_node.click()
                               
            if vmname:
                PD_DebugLog.debug_print("The vmname is %s" % vmname )
                PD_DebugLog.debug_print("The current node title is %s" % current_node.get_node_title())
                if vmname == current_node.get_node_title():
                    self.found_elmts.append(tree_node)
                    if DEBUG_LOG_PRINT:
                        PD_DebugLog.debug_print("Found the vmname. ")
                    if find_stop:
                        return True
                        
            if current_node.has_child_node():
                child_nodes = current_node.get_all_child_nodes()
                if DEBUG_LOG_PRINT:
                    PD_DebugLog.debug_print("There is %d child nodes: " % (len(child_nodes)))
                for node in child_nodes:            
                    found = _travel_all_nodes(node, vmname, find_stop, expand_nodes)
                    PD_DebugLog.debug_print("_travel_all_nodes return: %r " % found)
                    if found:
                        PD_DebugLog.debug_print("Found is set True because found the child item" )
                        break
            
            PD_DebugLog.debug_print("Do not find the vm by name" )
            #return False
                          
                    
        tree_node = TreeNode(self.tree)
        if tree_node.has_child_node():
            _travel_all_nodes(self.tree, vmname, find_stop, expand_nodes)
        
        
    def find_element_by_vmname(self, vmname):
        self.found_elmts = []
        
        self.travel_around_child_nodes(vmname=vmname, find_stop=True, expand_nodes=True)
        if self.found_elmts:
            return self.found_elmts
        else:
            return None
        
        
        
  