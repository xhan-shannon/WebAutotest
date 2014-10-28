# -*- coding: utf-8 -*-
'''
Created on 2014��6��13��

@author: stm
'''

import win32gui
import re
import logging
import win32con
import time

top_hwnd = None

class WindowFinder:
    """Class to find and make focus on a particular Native OS dialog/Window """
    def __init__ (self):
        self._handle = None
        self.expect_sec_window = None
        self.hwnd = None

    def find_window(self, class_name, window_name = None):
        """Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """

        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """Get the focus on the desired open window"""
        logging.debug("set the window foreground")
        if self.hwnd:
            logging.debug("Find the window and set it as foreground")
            win32gui.SetForegroundWindow(self.hwnd)

    def _window_enum_dialog_callback_(self, hwnd, extra):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        #self._handle = None
        matchtext = extra 
        logging.debug("call _window_enum_dialog_callback")
        classname = win32gui.GetClassName(hwnd)
        title_text = win32gui.GetWindowText(hwnd)
        title_text = title_text.decode('gbk').encode('utf-8')
        if classname == '#32770':
            matchtext = matchtext.encode('utf-8')
            logging.debug("msg: " + matchtext)
            logging.debug("Title is: " + title_text)
#             buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
#             buffer_text = win32gui.PyMakeBuffer(buf_size)
#             win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer_text)
#         
#             logging.debug("Buffer_text: " + buffer_text)
#             logging.debug("Buffer_text decode(gbk).encode(utf-8): " + 
#                           buffer_text.decode('gbk').encode('utf-8'))
#             windowText = buffer_text[:buf_size]
# 
#             try:
#                 windowText = windowText.decode('gbk').encode('utf-8') #unicode(windowText, 'utf-8')
#             except:
#                 logging.debug("_window_enum_dialog_callback unicode exception")
#                 pass
# 
#             message = ['Handle:\t' + str(hwnd),
#                    'Class Name:\t' + classname,
#                    'Window Text:\t' + windowText]
#     
#             logging.debug("Print the message: " + str(message))
#                
#             #if re.match(wildcard, windowText) != None:
            
            if (matchtext.strip() == title_text.strip()):
                logging.debug("!!!!BINGO!!!!")
                self.hwnd = hwnd
                return False
            else:
                logging.debug("No matched .....")
                return True
            
    
    def find_dialog_wildcard(self, wildcard):
        ''' Enumerate all the dialog to find the dialog which title matches the title'''              
        
        #extra = (self._handle, wildcard)
        try:
            win32gui.EnumWindows(_window_enum_dialog_callback, wildcard)
        except:
            logging.debug("Got the error:")
            logging.debug("win32gui.EnumWindows with " + str(_window_enum_dialog_callback))
            pass
        
        self.hwnd = top_hwnd

    
    def SendMessage(self, msg):
        '''Send message to the top window'''
        logging.debug("SendMessage "+msg + " to the current top window")
        win32gui.SendMessage(self.hwnd, msg, 0, 0)

    
    def expect_the_specific_dialog(self, _current_dialog):
        '''
        Set the windows white list,
        Then find another 
        :_current_dialog: 
        :return: the new top dialog
        '''
        def _expect_window_dialog_enum_callback(hwnd, extra):
            '''Call back func which checks each open window and matches the name of window using reg ex'''
            #self._handle = None
            matchtext = extra 
            logging.debug("call _window_enum_dialog_callback")
            classname = win32gui.GetClassName(hwnd)
            title_text = win32gui.GetWindowText(hwnd)
            title_text = title_text.decode('gbk').encode('utf-8')
            if classname == '#32770':
                matchtext = matchtext.encode('utf-8')
                logging.debug("msg: " + matchtext)
                logging.debug("Title is: " + title_text)
                 
            if (matchtext.strip() == title_text.strip()):
                logging.debug("!!!!Second window BINGO!!!!")
                if hwnd not in self.white_windows_list:
                    logging.debug("Find the second window at the top")
                    self.expect_sec_window = hwnd
                    return False
                else:
                    logging.debug("Find the window at the top which is not the second")
                    return True
            else:
                logging.debug("No matched .....")
                return True
            
        self.white_windows_list = [_current_dialog, ]
        windowtitle = win32gui.GetWindowText(_current_dialog)
        logging.debug("To find the second window, need match " + windowtitle)
        
        try:
            #win32gui.EnumWindows(_expect_window_dialog_enum_callback, windowtitle)
            win32gui.EnumChildWindows(self.hwnd, _expect_window_dialog_enum_callback, windowtitle)
        except:
            logging.debug("Got the error:")
            logging.debug("win32gui.EnumWindows with " + str(_expect_window_dialog_enum_callback))
        

    
    def get_current_dialog(self):
        '''just return the current top window'''
        return self.hwnd

    
    def get_expect_sec_window(self):
        '''return the expect window hwnd'''                
                           
#         control = win32gui.FindWindowEx(window, 0, 'static', None)
#         buffer = win32gui.PyMakeBuffer(20)
#         length = win32gui.SendMessage(control, win32con.WM_GETTEXT, 20, buffer)
#  
#         result = buffer[:length]
#         print result
#         time.sleep(1)
        return self.expect_sec_window

    
    def get_expect_window_label_text(self, _expect_sec_window):
        '''
        Try to get window label text
        '''
#         label_text = u"文件上传"
#         label_text = label_text.encode('utf-8')
#         return label_text
        label_text = ''
        window = self.expect_sec_window
        
        child_control = None
        last_child = 0
        while True:
            logging.debug("Find the child controls for parent window")
            child_control = win32gui.FindWindowEx(window, last_child, 'static', None)
            if not child_control:
                logging.debug("The child is None")
                break;
            else:
                logging.debug("The child is not None, ")
                buffer = win32gui.PyMakeBuffer(200)
                length = win32gui.SendMessage(child_control, win32con.WM_GETTEXT, 200, buffer)
                result = buffer[:length]
                result = result.decode('gbk').encode('utf-8')
                logging.debug("Got the child text is :" + result)
                last_child = child_control
                label_text = result
            time.sleep(0.5)
            
        def _winfun(hwnd, lparam):
            s = win32gui.GetWindowText(hwnd)
            s = s.decode('gbk').encode('utf-8')
            logging.debug("winfun, child_hwnd: %d   txt: %s" % (hwnd, s))
            return 1

        if window:
            logging.debug("To enumerate all the child windows")
            win32gui.EnumChildWindows(self.expect_sec_window, _winfun, None)
            
        #bufferlength = struct.pack('i', 255)
        #count = win32gui.SendMessage(self.expect_sec_window, win32con.get, 0, 0)
        #for itemIndex in range(count):
        #    value = array.array('c', bufferlength +str().ljust(253))
        #    valueLength = win32gui.SendMessage(self.expect_sec_window, getValueMessage, itemIndex, value)
        #    yield value.tostring()[:valueLength]
            
        
    
        return label_text
    
    
    
    
    
    
    
    
    
    
    
def _window_enum_dialog_callback(hwnd, extra):
    '''Call back func which checks each open window and matches the name of window using reg ex'''
    #self._handle = None
    matchtext = extra 
    matchtext = matchtext.encode('utf-8')
    logging.debug("call _window_enum_dialog_callback")
    classname = win32gui.GetClassName(hwnd)
    title_text = win32gui.GetWindowText(hwnd)
    title_text = title_text.decode('gbk').encode('utf-8')
    if classname == '#32770':
        matchtext = matchtext.encode('utf-8')
        logging.debug("msg: " + matchtext)
        logging.debug("Title is: " + title_text)
         
    if (matchtext.strip() == title_text.strip()):
        logging.debug("!!!!BINGO!!!!")
        top_hwnd = hwnd
        logging.debug("Find the window at the top")
        return False
    else:
        logging.debug("No matched .....")
        return True
