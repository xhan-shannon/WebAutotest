# -*- coding: utf-8 -*-
'''
@author: stm
'''
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from Common.Utils import PD_DebugLog
from Common.TestError import TestError
from Common.PD_Login import Login_Error
from webbrowser import Chrome
from selenium.webdriver import chrome




class PD_Connection(object):
    '''
    Connect firefox
    '''

    IMPLICITY_WAIT_TIMEOUT = 30
    def __init__(self, svrip, svrport):
        '''
        initialize the connection
        '''
        self.url = "http://%s:%s" % (svrip, svrport)

    def start(self, browser_type="Chrome", implicity_wait_timeout=IMPLICITY_WAIT_TIMEOUT):
        '''
        To open a browser
        '''
        browser = None
        if browser_type.startswith('Chrome'):
            chromedriver = os.path.join(os.environ["AUTODIR"], "webdriver", "chromedriver.exe")
            PD_DebugLog.debug_print("To print the chromedirver path: " + chromedriver)
            chromedriver = os.path.abspath(chromedriver)
            os.environ["webdriver.chrome.driver"] = chromedriver

            #chrome_options = Options()
            #chrome_options.add_argument("--ignore-certificate-errors")
            #chrome_options.add_argument("--disable-popup-blocking")
            
            
            options = webdriver.ChromeOptions()
            # set some options
            #driver = webdriver.Remote(desired_capabilities=options.to_capabilities())
            options.add_argument("--always-authorize-plugins")
            
            
            #for opt in options.arguments():
            #    PD_DebugLog.info_print("option : " + opt)
                
            browser_chrome = webdriver.Chrome(chromedriver, 
                                              chrome_options=options)
            
            browser = browser_chrome
        else:
            browser_firefox = webdriver.Firefox()
            browser = browser_firefox
        #browser = webdriver.Firefox()
        
        if not browser:
            raise(TestError("No browser opened"))
        
        browser.implicitly_wait(implicity_wait_timeout)
        browser.maximize_window()
        browser.get(self.url)

        return browser
    
    def start_htmlunit(self, implicity_wait_timeout=60):
        browser = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
        browser.implicitly_wait(implicity_wait_timeout)
        browser.get(self.url)
        
    
    def pd_login(self, driver, username, password):
        '''
        Use default configurations in shared_config file to login PD
        '''
            
        pd_browser_client = driver
    
        PD_DebugLog.stepinfo("Login PowerDirector")
        PD_DebugLog.debug_print("client browser title is " + pd_browser_client.title)
        assert "PowerDirector" in pd_browser_client.title
        PD_DebugLog.info_print("Page title: " + pd_browser_client.title)
    
        uid_input = pd_browser_client.find_element_by_id("uid")
        uid_input.send_keys(username)
        p_input = pd_browser_client.find_element_by_id("pword")
        p_input.send_keys(password)
        login_button = pd_browser_client.find_element_by_xpath("/html/body/div/form/div/p[4]/input")
        login_button.click()
        expect_welcome_panel = pd_browser_client.find_element_by_id("user_panel")
        welcome_text = "PowerDirector"
    
        try:
           if welcome_text in expect_welcome_panel.text:
                PD_DebugLog.debug_print(expect_welcome_panel.text)
        except:
            raise Login_Error("Login fails")
            pd_browser_client.quit()
    
        return pd_browser_client
