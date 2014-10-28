# -*- coding: utf-8 -*-
'''
Created on 2014.10.13

@author: stm
'''
import ConfigParser
from Common.Utils import PD_DebugLog
import os
from Common.Basejob import Basejob
from Common.Connect import PD_Connection
import time
import subprocess
import re
import ipaddress




def readconfig(classname):
    
    config = ConfigParser.ConfigParser()
    config_file = 'cfg\\' + classname + '.cfg'
    PD_DebugLog.debug_print("The self.config_file is " + config_file)
    config_file = os.path.join(Basejob.TESTCASE_DIR, config_file)
    PD_DebugLog.debug_print("The self.config_file is " + config_file)
    if config_file and os.path.exists(config_file):
        config.read(config_file)
        return config
    else:
        return None
    
def save_screenshot(driver, path, filename):
    '''
    To save the screenshot for the failed case
    '''
    screenshot_filename = os.path.join(path, filename)
    PD_DebugLog.debug_print("The saved file is " + screenshot_filename)
    
    driver.save_screenshot(screenshot_filename)
    
    
def set_script_timeout(driver, timeout=0.5):
    '''
    Set webdriver timeout 
    '''
    driver.set_script_timeout(timeout)
    

def restore_script_timeout(driver):
    '''
    Restore the timeout for the webdriver timeout value
    '''
    driver.set_script_timeout(PD_Connection.IMPLICITY_WAIT_TIMEOUT)
    

def set_implicity_wait_timeout(driver, timeout=0.5):
    '''
    Set webdriver timeout 
    '''
    driver.implicitly_wait(timeout)
    

def restore_implicity_wait_timeout(driver):
    '''
    Restore the timeout for the webdriver timeout value
    '''
    driver.implicitly_wait(PD_Connection.IMPLICITY_WAIT_TIMEOUT)
    
    
def wait_for(func, timeout, first=0.0, step=1.0, text=None):
    """
    If func() evaluates to True before timeout expires, return the
    value of func(). Otherwise return None.

    @brief: Wait until func() evaluates to True.

    :param timeout: Timeout in seconds
    :param first: Time to sleep before first attempt
    :param steps: Time to sleep between attempts in seconds
    :param text: Text to print while waiting, for debug purposes
    """
    start_time = time.time()
    end_time = time.time() + timeout

    time.sleep(first)

    while time.time() < end_time:
        if text:
            PD_DebugLog.debug_print("%s (%f secs)" % ( text, (time.time() - start_time)))

        output = func()
        if output:
            return output

        time.sleep(step)

    return None

def ping(target_vm_ipaddr):
    return subprocess.check_output("ping %s" % target_vm_ipaddr)
    
    #return os.system("ping %s" % target_vm_ipaddr)


def is_valid_ip(target_vm_ip):
    
    try:
        ip_addr = ipaddress.ip_address(target_vm_ip)
    except:
        ip_addr = None
        
    if ip_addr:
        return True
    else:
        return False


def get_loss_ratio(output):
    """
    Get the packet loss ratio from the output of ping.

    :param output: Ping output.
    """
    try:
        # packet loss
        return int(re.findall(u'(\d+)% 丢失', output)[0])
    except IndexError:
        PD_DebugLog.debug_print(output)
        return -1


