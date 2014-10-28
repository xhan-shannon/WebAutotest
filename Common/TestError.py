# -*- coding: utf-8 -*-
'''
Created on 20141008

@author: stm
'''

class TestError(Exception):
    """The parent of all errors deliberately thrown within the client code."""

    def __str__(self):
        return Exception.__str__(self) #+ _context_message(self)
    

class ElemNotExisted(TestError):
    pass
    