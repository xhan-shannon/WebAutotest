# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
import smtplib
import threading
import unittest, time, re

import SendKeys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import win32gui

from Common import HTMLTestRunner, RegisterLicUI
from Common.Basejob import Basejob
from Common.Connect import PD_Connection
import Common.RegisterLicUI
from Common.WindowFinder import WindowFinder


class FileNotExistedError(Exception):
    pass

class ActivateProduction(Basejob):
    '''
    To test product activation cases
    '''
    LICFILE_NOT_EXISTED_CASE = 0
    LICFILE_NOT_VALID = 1
    LICFILE_VALID = 2
    
    def setUp(self):
        #pd_conn = PD_Connection('172.24.23.111', '8080')
        #self.driver = self.pd_client_browser = pd_conn.start()
        Basejob.setUp(self)
        
        self.verificationErrors = []
        self.accept_next_alert = True
        self.registerLicUI = Common.RegisterLicUI.RegisterLicUI(self.driver)
        expect_title = u"产品激活"
        current_title = self.registerLicUI.get_current_title()
        logging.info("Current title is " + current_title)
        
        # 确认页面标题是“产品激活”， 如果不是退出该用例测试
        if not expect_title in current_title:
            self.driver.quit()
            self.assertTrue(False)
            
        self.assertIn(expect_title, current_title)
        self.response_msg = self.registerLicUI.get_response_msg_elm()
                
        logging.debug("Set up the log system")
        logfile_prefix = self._testMethodName
        logging.debug("Testcase name is " + logfile_prefix)
        testcasedir = os.path.join(RESULT_DIR, logfile_prefix)
        if not os.path.isdir(testcasedir):
            os.mkdir(testcasedir)
        infolog_file = logfile_prefix + '.info'
        debuglog_file = logfile_prefix + '.debug'
        
        # set log files
        infolog_file = os.path.join(testcasedir, infolog_file)
        infolvl_handler = logging.FileHandler(infolog_file, "w")
        fmt = logging.Formatter('[%(levelname)s:%(asctime)s]:%(message)s')
        infolvl_handler.setFormatter(fmt)
        infolvl_handler.setLevel(logging.INFO)
        logging.root.addHandler(infolvl_handler)
    
        debuglog_file = os.path.join(testcasedir, debuglog_file)
        debuglvl_handler = logging.FileHandler(debuglog_file, "w")
        fmt = logging.Formatter('[%(levelname)s:%(asctime)s]:%(message)s')
        debuglvl_handler.setFormatter(fmt)
        debuglvl_handler.setLevel(logging.DEBUG)
        logging.root.addHandler(debuglvl_handler)
    
    def test_activateproduct(self):
        u'''激活产品（使用不存在的文件名）'''
        def _action_on_trigger_element(_element):
            _element.click()
            
            
        logging.info("Test wrong lic file. Expect the the wrong file can be prompted" 
                      " proper error with ")
        
        driver = self.driver
        
        lic_file_path = 'abcdef123456'
        logging.info("Input the file: " + lic_file_path)
        select_file_btn_elm = driver.find_element(By.XPATH, 
                                  '//*[@id="uploadform"]/div/p[3]/input')
        #select_file_btn_elm.click()
        th = threading.Thread(target = _action_on_trigger_element, args =[
                              select_file_btn_elm])
        th.start()
        time.sleep(1)
        
        # Call WindowFinder Class
        upload_file_dialog_title = u"文件上传"
        enter_str = "{ENTER}"
        win = WindowFinder()
        #win.find_window_wildcard(upload_file_dialog_title)
        win.find_dialog_wildcard(upload_file_dialog_title)
        win.set_foreground()
        result_status = True
        #try:
        logging.debug("Try to sendkeys")
        #win.SendMessage(lic_file_path)
        SendKeys.SendKeys(lic_file_path)
        time.sleep(2)
        SendKeys.SendKeys(enter_str)
        time.sleep(2)
        assert(not th.isAlive())
        #except:
        #    logging.debug("catch in sendkeys exception")
        #    result_status = False
        
        # 检查点
        #　不存在的文件，会提示“ｘｘｘｘ文件不存在”，使用程序期待这样的弹出窗口
        win.expect_the_specific_dialog(win.get_current_dialog())
        time.sleep(2)
        # 有窗口弹出，该“不存在文件名测试”即成功
        self.failUnless(win.get_expect_sec_window())
 
      
    def test_activateproduct_with_wronglicfile(self):
        u'''激活产品（使用存在的文件名,lic文件不匹配）'''
        licfile = r'E:\TEAMSUN\Lic\06052EA_8246-L2D_ivm39.lic'
        self.activate_product_with_licfile(ActivateProduction.LICFILE_NOT_VALID,
                                           licfile)
        
    def test_activateproduct_with_correctlicfile(self):
        u'''激活产品（使用存在的有效lic文件）'''
        licfile = r'E:\TEAMSUN\Lic\060556A_8246-L2D_111.lic'
        self.activate_product_with_licfile(ActivateProduction.LICFILE_VALID,
                                           licfile)
        
    
    def activate_product_with_licfile(self, reg_type, licfile):
        '''
        Use a lic file to activate the product
        
        :licfile: refer to a lic file 
        '''
        def _action_on_trigger_element(_element):
            _element.click()
            
            
        logging.info("Test wrong lic file. Expect the the wrong file can be prompted" 
                      " proper error with ")
        
        driver = self.driver
        
        registerLicUI = RegisterLicUI.RegisterLicUI(driver)
        
        lic_file_path = licfile
        #lic_file_path = 'abcdef123456'
        logging.info("Input the file: " + lic_file_path)
        select_file_btn_elm = registerLicUI.get_select_file_btn_elm()

        select_file_btn_elm.click()
        th = threading.Thread(target = _action_on_trigger_element, args =[
                              select_file_btn_elm])
        th.start()
        time.sleep(1)
        
        # Call WindowFinder Class
        upload_file_dialog_title = u"文件上传"
        enter_str = "{ENTER}"
        win = WindowFinder()
        #win.find_window_wildcard(upload_file_dialog_title)
        win.find_dialog_wildcard(upload_file_dialog_title)
        win.set_foreground()
        
        #try:
        logging.debug("Try to sendkeys")
        #win.SendMessage(lic_file_path)
        time.sleep(1)
        SendKeys.SendKeys(lic_file_path)
        time.sleep(2)
        SendKeys.SendKeys(enter_str)
        time.sleep(2)
        assert(not th.isAlive())
        #except:
        #    logging.debug("catch in sendkeys exception")
        #    result_status = False
        
        # 检查点
        if ActivateProduction.LICFILE_NOT_EXISTED_CASE == reg_type:
            #　不存在的文件，会提示“ｘｘｘｘ文件不存在”，使用程序期待这样的弹出窗口
            win.expect_the_specific_dialog(win.get_current_dialog())
            time.sleep(2)
            # 有窗口弹出，该“不存在文件名测试”即成功, 
            # 文件存在则跳过该检查步骤，到下一检查点
            self.failUnless(win.get_expect_sec_window())
        elif ActivateProduction.LICFILE_NOT_VALID == reg_type:
            #　Licfile文件存在，点击“上传按钮”后，
            # 有返回消息“上传的License文件无效！”返回
            registerLicUI.get_submit_btn().click()
            time.sleep(2)  # 等待时间不能太短
            
            #response_msg_elm = driver.find_element_by_id('msg')
            #import pdb; pdb.set_trace()
            expectmsg = u"上传的License文件无效！".strip()
            respmsg = registerLicUI.get_response_msg_elm() #response_msg_elm.strip() #.encode('utf-8')
            respmsg = unicode(respmsg.strip())
            logging.info("Got the msg is "  + respmsg)
            self.assertEqual(respmsg, expectmsg)
        
        elif ActivateProduction.LICFILE_VALID == reg_type:
            registerLicUI.get_submit_btn().click()
            time.sleep(3)  # 等待时间不能太短
            
            # wait to alert dialog pops up
            
            expectmsg = u'License验证成功,转到登录界面！'
            respmsg = registerLicUI.get_alert_text()
            respmsg = unicode(respmsg.strip())
            logging.info("Step info: " + 
                         "Got the response message, " +
                         respmsg )
            self.assertEqual(expectmsg, respmsg)

        #driver.refresh()
        time.sleep(2)
        #return result_status
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        Basejob.tearDown(self)
        self.assertEqual([], self.verificationErrors)

RESULT_DIR = '..\\results'

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s:%(asctime)s]:%(message)s', 
                        level=logging.DEBUG)
    testsuite = unittest.TestSuite()
    
    testsuite.addTest(ActivateProduction('test_activateproduct'))
    testsuite.addTest(ActivateProduction('test_activateproduct_with_wronglicfile'))
    testsuite.addTest(ActivateProduction('test_activateproduct_with_correctlicfile'))
    
    desc_text = u'''验证“激活产品”
                      1)对不存在的文件的处理
                      2)对错误lic文件的处理
                      3)注册正确的lic文件
                 '''
    
    report_file_name = 'my_file_report.html'
    report_file_name = os.path.join(RESULT_DIR, report_file_name)
    fp = file(report_file_name, 'wb')
    testrunner = HTMLTestRunner.HTMLTestRunner(
                 stream=fp,
                 title = u'PD2.5 Web功能验证',
                 description = desc_text)
    
    testrunner.run(testsuite)
    
    time.sleep(5)

    
    me = 'hanxm@teamsun.com.cn'
    
    #you = ['hanxm@teamsun.com.cn', 'lizhha@teamsun.com.cn']
    you =  ['hanxm@teamsun.com.cn', ]
    msg = MIMEMultipart()
    msg['Subject'] = "Python send email test[Do not reply]"
    msg['From'] = me
    #msg['To'] = you

    
    # add attach file
    # open the report file to send it out as email attachment

    #fp = open(report_file_name, 'r')
    #msg = MIMEText(fp.read(), 'base64', 'gb2312')
    #fp.close()
    #att = MIMEText(open(report_file_name, 'r').read(), 'base64', 'gb2312')
    att = MIMEText(open(report_file_name, 'rb').read(), 'text/html', _charset='gb2312')
    att["Content-Type"] = 'application/octet-stream' 
    str_content_disposition = 'attachment; filename=%s' % report_file_name  
    att["Content-Disposition"] = str_content_disposition  #"report.html"'
    msg.attach(att)
    
    s = smtplib.SMTP()
    s.connect('smtp.teamsun.com.cn')
    s.set_debuglevel(1)
    s.login('hanxm@teamsun.com.cn', 'teamsun2009')
    s.sendmail(me, you, msg.as_string())
    s.quit()