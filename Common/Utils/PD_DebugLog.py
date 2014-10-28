#!/usr/bin/python
# -*-coding: utf-8 -*-
'''
Created on 

@author: stm
'''
import logging
from Common.Messages import Messages


PD_DEBUG_LOG = True

DEBUG_LOG_PRINT = True

PD_LOG_LEVEL_DEBUG, PD_LOG_LEVEL_INFO, PD_LOG_LEVEL_WARNING = range(3)

PD_LOG_LEVEL = PD_LOG_LEVEL_INFO

def init_log():
    logging.basicConfig(format='[%(pathname)s: %(lineno)d: %(levelname)s:%(asctime)s]:%(message)s', 
                        level=logging.DEBUG)


def pd_log(loglevel, details):
    pass


def stepinfo(info):
    logging.info(Messages.STEP_INFO + info)    # "Step info: " 

    
def debug_print(msg):
    logging.debug("| " + msg)


def info_print(msg):
    logging.info("| " + msg)