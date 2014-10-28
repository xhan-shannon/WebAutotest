# -*- coding: utf-8 -*-
'''
Created on 2014年7月1日

@author: stm
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
import sys
import smtplib
import time
import unittest


autotest_client_dir = os.path.dirname(sys.argv[0]) # os.path.join("..","")
os.environ['AUTODIR'] = os.path.abspath(os.path.join(autotest_client_dir, ".."))


sys.path.append(os.environ['AUTODIR'])
from Common import HTMLTestRunner
from Common.Utils import PD_DebugLog

test_case_dir = os.path.join(os.environ['AUTODIR'], "tests")
sys.path.append(test_case_dir)

from ActivateProduction import ActivateProduction
from RegisterPlatform import RegisterPlatform
from UploadISO import UploadISO
from RegisterISO import RegisterISO
from RegisterIMG import RegisterIMG
from CreateVM import CreateVM
from DestroyVM import DestroyVM
from PowerdownVM import PowerdownVM
from BootVM import BootVM
from RebootVM import RebootVM
from PingVM import PingVM
from RegisterVMIP import RegisterVMIP



RESULT_DIR = os.path.join(os.environ["AUTODIR"], 'results')

if __name__ == "__main__":
    #logging.basicConfig(format='[%(pathname)s: %(lineno)d: %(levelname)s:%(asctime)s]:%(message)s', 
    #                    level=logging.DEBUG)
    
    logging.basicConfig(format='[%(levelname)s:%(asctime)s]:%(message)s', 
                        level=logging.DEBUG)
    
    auto_cur_dir = os.path.dirname(sys.argv[0])
    PD_DebugLog.info_print("The current dir is: " + auto_cur_dir)
    os.environ['AUTODIR'] = os.path.abspath(os.path.join(auto_cur_dir, ".."))
    testsuite = unittest.TestSuite()
    
    #testsuite.addTest(ActivateProduction('test_activateproduct'))
    #testsuite.addTest(ActivateProduction('test_activateproduct_with_wronglicfile'))
    #testsuite.addTest(ActivateProduction('test_activateproduct_with_correctlicfile'))
    
    #testsuite.addTest(RegisterPlatform('test_Register_Platform'))
    #testsuite.addTest(RegisterPlatform('test_Register_Platform_Check'))
    
    # UploadISO 上传镜像
    #testsuite.addTest(UploadISO('test_upload_iso'))
    
    # RegisterISO 注册镜像
    #testsuite.addTest(RegisterIMG('test_register_image'))
    
    # Create VM 创建虚拟机
    #testsuite.addTest(CreateVM('test_create_vm_from_image', True))
    
    
    # Boot VM 启动虚拟机
    #testsuite.addTest(BootVM('test_boot_vm_normally'))
    
    # Register IP for VM
    #testsuite.addTest(RegisterVMIP('test_register_vm_ip_normally')) 
    # Ping VM 
    #testsuite.addTest(PingVM('test_ping_vm_normally'))
    
    # Reboot VM 重启虚拟机
    #testsuite.addTest(RebootVM('test_reboot_vm_normally'))
    
    # Powerdown VM 断电虚拟机
    #testsuite.addTest(PowerdownVM('test_powerdown_vm_normally'))
    
    # Destroy VM 删除虚拟机
    testsuite.addTest(DestroyVM('test_destroy_vm_normally'))
    
    desc_text = u'''PD2.5 基本功能验证 包括 \n\r
                    “激活产品”，“注册平台”，“注册镜像”，“创建虚机”， “删除虚机”
                 '''
    
    report_file_name = 'PD2.5_WebAutotest_results.html'
    report_file_name = os.path.join(RESULT_DIR, report_file_name)
    fp = file(report_file_name, 'wb')
    
    testrunner = HTMLTestRunner.HTMLTestRunner(
                 stream=fp,
                 title = u'PD2.5 Web功能验证',
                 description = desc_text)
    
    testrunner.run(testsuite)
    
#     time.sleep(5)
# 
#     
#     me = 'hanxm@teamsun.com.cn'
#     
#     #you = ['hanxm@teamsun.com.cn', 'lizhha@teamsun.com.cn']
#     you =  ['hanxm@teamsun.com.cn', ]
#     msg = MIMEMultipart()
#     msg['Subject'] = "Python send email test[Do not reply]"
#     msg['From'] = me
#     #msg['To'] = you
# 
#     
#     # add attach file
#     # open the report file to send it out as email attachment
# 
#     #fp = open(report_file_name, 'r')
#     #msg = MIMEText(fp.read(), 'base64', 'gb2312')
#     #fp.close()
#     #att = MIMEText(open(report_file_name, 'r').read(), 'base64', 'gb2312')
#     att = MIMEText(open(report_file_name, 'rb').read(), 'text/html', _charset='gb2312')
#     att["Content-Type"] = 'application/octet-stream' 
#     str_content_disposition = 'attachment; filename=%s' % report_file_name  
#     att["Content-Disposition"] = str_content_disposition  #"report.html"'
#     msg.attach(att)
#     
#     s = smtplib.SMTP()
#     s.connect('smtp.teamsun.com.cn')
#     s.set_debuglevel(1)
#     s.login('hanxm@teamsun.com.cn', 'teamsun2009')
#     #s.sendmail(me, you, msg.as_string())
