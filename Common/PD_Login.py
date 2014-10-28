# -*- coding: utf-8 -*-
'''
Created on 2014年5月19日

@author: hanxm
'''
import os
import time
from selenium import webdriver
 

class Login_Error(Exception):
    def __init__(self, details=None):
        self.details = details

    def __str__(self):
        e_msg = "Test "
        if self.details is not None:
            e_msg += ": %s" % self.details
        return e_msg
    
#def login(username, password, server, port, keeplogin=False):
def login(driver, username, password, keeplogin=False):    
    #pd_browser_client = PD_Common.connectPD_Firefox(server, port)
    pd_browser_client = driver

    assert "PowerDirector" in pd_browser_client.title
    print("Page title: " + pd_browser_client.title)

    pd_browser_client.implicitly_wait(10)
    uid_input = pd_browser_client.find_element_by_id("uid")
    uid_input.send_keys(username)
    p_input = pd_browser_client.find_element_by_id("pword")
    p_input.send_keys(password)
    login_button = pd_browser_client.find_element_by_xpath("/html/body/div/form/div/p[4]/input")
    login_button.click()
    expect_welcome_panel = pd_browser_client.find_element_by_id("user_panel")
    welcome_text = "PowerDirector"
    #assert "欢迎！" in expect_welcome_panel.text()

    try:
        
        if welcome_text in expect_welcome_panel.text:
            print( expect_welcome_panel.text)
            
    except:
        raise Login_Error("Login fails")
        pd_browser_client.quit()

    return pd_browser_client