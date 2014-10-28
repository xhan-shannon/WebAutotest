# -*- coding: utf-8 -*-
'''
Created on 2014��10��15��

@author: stm
'''
from selenium.webdriver.common.by import By
from Common.Utils import PD_DebugLog

class Create_VM_UIMap(object):
    """
    Map the PowerDirector elements to the convenience interface.
    Such as the label, input editor, button or frames.
    """
    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.frame("_large_frame")        
        
    def get_header(self):
        '''
        get the header element text
        '''
        return self.driver.find_element(By.XPATH, '//*[@id="vmform"]/h2')  
    
    def get_next_button(self):
        '''
        get the next button
        '''
        return self.driver.find_element(By.ID, "btn_next") 
    
    def get_confirm_button(self):
        '''
        get the confirm button to submit the configuration
        '''
        return self.driver.find_element(By.ID, "btn_confirm") 
    
    def get_vm_name_input(self):
        '''
        get the next button
        '''
        return self.driver.find_element(By.ID, "vmName")
    
    def get_iso_radio_btn(self):
        '''
        get the iso radio button
        '''
        return self.driver.find_element(By.ID, 'rdo_from_iso')
     
    def get_template_radio_btn(self):
        '''
        get the from template radio button
        '''
        return self.driver.find_element(By.ID, 'rdo_from_template')
    
    def get_iso_table(self):
        '''
        get the iso table
        '''
        table = self.driver.find_element(By.ID, 'rdo_from_iso')
        ##iso_table > tbody > tr:nth-child(1)
        #table_records = table.find_elements_by_tag_name("tr")
        #PD_DebugLog.debug_print("table count is : %d " % len(table_records))
        table_records = self.driver.find_elements_by_xpath('//*[@id="iso_table"]/tbody/tr')
        PD_DebugLog.debug_print("table count is : %d " % len(table_records))
        for tr in table_records:
            field2_elm = self.driver.find_element_by_xpath('//*[@id="iso_table"]/tbody/tr[2]/td[2]/div')
            field2_txt = field2_elm.text
            PD_DebugLog.debug_print("The table field[1] is :" + field2_txt)
        # //*[@id="templates_table"]/tbody/tr[2]/td[2]/div
    
    def select_template_from_table_by_name(self, name):
        # //*[@id="templates_table"]/tbody/tr[2]/td[2]/div
        table_records = self.driver.find_elements_by_xpath('//*[@id="templates_table"]/tbody/tr')
        PD_DebugLog.debug_print("table count is : %d " % len(table_records))
        # select the table record and click the radio button
        for nid in range(len(table_records)):
            field2_elm = self.driver.find_element_by_xpath('//*[@id="templates_table"]/tbody/tr[%d]/td[2]/div' % (nid + 1) )
            field2_txt = field2_elm.text
            PD_DebugLog.debug_print("table element name is :" + field2_txt)
            if name in field2_txt:
                #self.driver.find_element_by_xpath('//*[@id="templates_table"]/tbody/tr[%d]/td[1]/div/[@id="imagePcid"]' % (nid + 1) ).click()
                table_records[nid].find_element(By.ID, 'imagePcid').click()
                PD_DebugLog.debug_print("Hit")
                PD_DebugLog.debug_print("The id is %d" % nid)
                #break
            
            PD_DebugLog.debug_print("The table field[%d] is : %s"  % (nid+1, field2_txt))
            #//*[@id="imagePcid"]
                
    def select_iso_from_table_by_name(self, name):
        table_records = self.driver.find_elements_by_xpath('//*[@id="iso_table"]/tbody/tr')
        PD_DebugLog.debug_print("table count is : %d " % len(table_records))
        for nid in range(len(table_records)):
            field2_elm = self.driver.find_element_by_xpath('//*[@id="iso_table"]/tbody/tr[%d]/td[2]/div' % (nid + 1) )
            field2_txt = field2_elm.text
            if name in field2_txt:
                #self.driver.find_element_by_xpath('//*[@id="iso_table"]/tbody/tr[%d]/td[1]/div/[@id="imagePcid"]' % (nid + 1) ).click()
                table_records[nid].find_element(By.ID, 'imagePcid').click()
                PD_DebugLog.debug_print("Hit")
                PD_DebugLog.debug_print("The id is %d" % nid)
                #break
            
            PD_DebugLog.debug_print("The table field[%d] is : %s"  % (nid+1, field2_txt))
            #//*[@id="imagePcid"]
            
        
    def get_shared_cpu_type_radio_btn(self):
        '''
        Get the cpu type: shared radio button
        '''
        return self.driver.find_element(By.ID, 'rdo_shared')


    def get_dedicated_cpu_type_radio_btn(self):
        '''
        Get the cpu type: dedicated radio button
        '''
        return self.driver.find_element(By.ID, 'rdo_dedicated')

    
    def get_cpu_num_min_input_elem(self):
        '''
        Get the cpu units num min value input element
        '''
        return self.driver.find_element(By.ID, 'minimumProcessingUnits')
        

    
    def get_cpu_num_expect_input_elem(self):
        '''
        Get the cpu units num expect value input element
        '''
        return self.driver.find_element(By.ID, 'assignedProcessingUnits')
        
    
    def get_cpu_num_max_input_elem(self):
        '''
        Get the cpu units num max value input element
        '''
        return self.driver.find_element(By.ID, 'maximumProcessingUnits')

    
    def get_vmcpu_num_min_input_elem(self):
        '''
        Get the virtual machine cpu num max value input element
        '''
        return self.driver.find_element(By.ID, 'minimumVirtualProcessors')
    
    
    def get_vmcpu_num_expect_input_elem(self):
        '''
        Get the virtual machine cpu num max value input element
        '''
        return self.driver.find_element(By.ID, 'assignedVirtualProcessors')
    
    
    def get_vmcpu_num_max_input_elem(self):
        '''
        Get the virtual machine cpu num max value input element
        '''
        return self.driver.find_element(By.ID, 'maximumVirtualProcessors')

    
    def get_mem_num_min_input_elem(self):
        '''
        Get the virtual machine memory value input element
        '''
        return self.driver.find_element(By.ID, 'minimumMemory')

    
    def get_mem_num_expect_input_elem(self):
        '''
        Get the virtual machine memory value input element
        '''
        return self.driver.find_element(By.ID, 'assignedMemory')

    
    def get_mem_num_max_input_elem(self):
        '''
        Get the virtual machine memory value input element
        '''
        return self.driver.find_element(By.ID, 'maximumMemory')

    
    def get_mem_unit_listbox_elem(self):
        '''
        Focus on memory unit listbox element, and return it
        '''
        return self.driver.find_element(By.ID, 'memory_unit')

    
    def select_GB_unit(self):
        '''
        Focus on memory unit listbox element, then select GB as the unit
        '''
        self._select_mem_unit("GB")
        
        
    def select_MB_unit(self):
        '''
        Focus on memory unit listbox element, then select GB as the unit
        '''
        self._select_mem_unit("MB")
        
        
    def _select_mem_unit(self, unit):
        '''
        Focus on memory unit listbox element, then select the item
        '''
        xpath = '//option[@value="%s"]' % unit
        mem_unit_listbox_elem = self.get_mem_unit_listbox_elem()
        item = mem_unit_listbox_elem.find_element(By.XPATH, xpath)
        item.click()

    
    def get_vol_size_input_elem(self):
        '''
        Get the volume size input element
        '''
        xpath = '//*[@id="step6"]/div/dl/dd[9]/input'
        return self.driver.find_element(By.XPATH, xpath)
        
    def select_vol_size_GB_unit(self):
        '''
        Focus on memory unit listbox element, then select GB as the unit
        '''
        self._select_vol_size_unit("GB")
           
        
    def _select_vol_size_unit(self, unit):
        '''
        Focus on memory unit listbox element, then select the item
        '''
        
        xpath = '//*[@id="step6"]/div/dl/dd[9]/select'
        vol_size_unit_droplist_elem = self.driver.find_element(By.XPATH, xpath)
        item_xpath = './/option[@value="%s"]' % unit
        item = vol_size_unit_droplist_elem.find_element(By.XPATH, item_xpath)
        item.click()
    
    
    def set_storage_vol_size(self, size, unit):
        '''
        Set the storage size 
        :size: the size for the volume
        :unit: the unit for the volume size, 'GB', 'MB'
        '''
        vol_size_input_elem = self.get_vol_size_input_elem()
        vol_size_input_elem.clear()
        vol_size_input_elem.send_keys(size)
        
        if unit.startswith("GB"):
            self.select_vol_size_GB_unit()
        
    
    def unselect_existed_volume(self):
        pass

    
    def select_volume_name_datavg(self):
        '''
        Select the volume name as datavg
        '''
        self._select_storage_volume_name('datavg')

    def _select_storage_volume_name(self, volname):
        '''
        Focus on storage type droplist element, then select the item
        '''
        idx = 0
        if volname.startswith("rootvg"):
            idx = 0
        elif volname.startswith("datavg"):
            idx = 1
            
        storage_type_droplist_elem = self.driver.find_element(By.NAME, 'storage_name')
        items = storage_type_droplist_elem.find_elements(By.TAG_NAME, "option")
        items[idx].click()

    
    def select_storage_type_vg(self):
        '''
        Select VG as the storage type
        '''
        self._select_storage_type('VG')
    
    def _select_storage_type(self, volname):
        '''
        Focus on storage type droplist element, then select the item
        '''
        value = 1
        if volname.startswith("VG"):
            value = 1
        elif volname.startswith("PV"):
            value = 2
        elif volname.startswith("SSP"):
            value = 3
            
        xpath = '//*[@class="storage_pool sel"]/option[@value="%d"]' % value
        storage_type_droplist_elem = self.driver.find_element(By.NAME, 'storage_pool')
        item = storage_type_droplist_elem.find_element(By.XPATH, xpath)
        item.click()

    
    def assign_ip_addr(self, ipaddr):
        '''
        assign the ip address
        '''
        self._net_adapt_assign_op('netAdapter_vmIp', ipaddr)

    
    def assign_submask(self, submask):
        '''
        assign the subnet mask
        '''
        self._net_adapt_assign_op('netAdapter_subnetMask', submask)

    
    def assign_gateway(self, gateway):
        '''
        assign the gateway
        '''
        self._net_adapt_assign_op('netAdapter_gateway', gateway)
        
    
    def assign_dns(self, dns):
        '''
        assign the dns
        '''
        self._net_adapt_assign_op('netAdapter_dns', dns)

    
    def assign_slavedns(self, slavedns):
        '''
        assign the slave dns
        '''
        self._net_adapt_assign_op('netAdapter_dnsBackup', slavedns)
    
    def _net_adapt_assign_op(self, elemtid, val):
        '''
        A common interface to abstract the operations
        '''
        xpath = './/*[@id="alone_vm"]//*[@id="%s"]' % elemtid
        input_elem = self.driver.find_element(By.XPATH, xpath)
        input_elem.clear()
        input_elem.send_keys(val)

    
    def assign_vlan(self, vlanid):
        self._net_adapt_assign_op('vlanid1', vlanid)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
    
    
    
