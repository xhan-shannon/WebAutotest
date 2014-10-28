# -*- coding: utf-8 -*-
'''
Created on 2014年7月1日
@author: stm
'''
import ConfigParser
import logging
import os
import time
import unittest

from Common.Connect import PD_Connection
from Common.Utils import PD_DebugLog
from Common.Messages import Messages


class ConfigFileError(Exception):
    
    def __str__(self):
        return Exception.__str__(self) #+ _context_message(self)



class Basejob(unittest.TestCase):
    '''
    Base job class for all the test cases
    It implemnets the setup and teardown function.
    All other cases need extend from it.
    '''
    RESULT_DIR = os.path.join(os.environ['AUTODIR'], 'results')
    TESTCASE_DIR = os.path.join(os.environ['AUTODIR'], 'tests')
    
    def __init__(self, methodName, need_config=True):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.need_config = need_config
        
    def setUp(self):
        '''
        Base job case need do setup stuff:
        1. Read config from base configuration file
             tests-shared.cfg
             <tests-case>.cfg
        2. Set the debug and info log files in the result directory
        3. Start the PD web browser connection
             
        '''
        self.shared_config = ConfigParser.ConfigParser()
        self.shared_config_file = os.path.join(Basejob.TESTCASE_DIR, 'cfg', 'tests-shared.cfg')
        PD_DebugLog.info_print("The shared_config is " + self.shared_config_file)
        if self.shared_config_file and os.path.exists(self.shared_config_file):
            self.shared_config.read(self.shared_config_file)
        else:
            raise ConfigFileError('%s not found' % (self.shared_config_file))
        
        
        if self.need_config:
            self.config = ConfigParser.ConfigParser()
            self.config_file = 'cfg\\' + self.__class__.__name__ + '.cfg'
            logging.debug("The self.config_file is " + self.config_file)
            self.config_file = os.path.join(Basejob.TESTCASE_DIR, self.config_file)
            logging.debug("The self.config_file is " + self.config_file)
            if self.config_file and os.path.exists(self.config_file):
                self.config.read(self.config_file)
            else:
                raise ConfigFileError('%s not found' % (self.config_file))
                    
        logging.debug("Set up the log system")
        logfile_prefix = self._testMethodName
        logging.debug("Testcase name is " + logfile_prefix)
        testcasedir = os.path.join(Basejob.RESULT_DIR, logfile_prefix)
        self.testcasedir = testcasedir
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

        url_addr = self.shared_config.get('DEFAULT', 'url')
        url_port = self.shared_config.get('DEFAULT', 'port')
        self.pd_conn = PD_Connection(url_addr, url_port)
        self.driver = self.pd_client_browser = self.pd_conn.start()
        #self.driver = self.pd_client_browser = pd_conn.start_htmlunit()

    def testName(self):
        pass


    def pd_login(self, username=None, password=None):
        '''
        Use default configurations in shared_config file to login PD
        '''
        if not username:
            username = self.shared_config.get('DEFAULT', 'pd_login_username')
            
        if not password:
            password = self.shared_config.get('DEFAULT', 'pd_login_password')
            
        PD_DebugLog.stepinfo(Messages.LOGIN_POWERDIRECTOR)
        self.pd_client_browser = self.pd_conn.pd_login(self.driver, 
                                                username,
                                                password)
        self.driver = self.pd_client_browser
        
        return self.driver
        
            
            
    def tearDown(self):
        '''
        Do the stuff when case is finished.
        The most cases of the this function is to close the browser.
        '''
        logging.debug("Basejob tearDown to close current page")
        if self.driver:
            time.sleep(1)
            self.driver.quit()
