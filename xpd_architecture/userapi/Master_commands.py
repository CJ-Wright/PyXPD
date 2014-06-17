# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from xpd_architecture.userapi import *
import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf, __initPV


def printf(value):
#    print value, test function
    return value

if __name__ == "__main__":
    __initPV(_conf)
#    print('Initial positions:')
#    print(where())
