# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from userapi import *
import cothread
from cothread.catools import *
from dataapi.config._conf import _conf

##TODO:Rename _initDet to _initPVs and put in every dataapi module that uses PVs
def printf(value):
#    print value, test function
    return value

if __name__ == "__main__":
    _initpvs(_conf)
#    print('Initial positions:')
#    print(where())
