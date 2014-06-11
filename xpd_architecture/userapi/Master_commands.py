# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from userapi.Motor_commands import *
from userapi.Detector_commands import *
import cothread
from cothread.catools import *
from dataapi.config._conf import _conf

def _initpvs(_conf):
    """
    Double checks connection to Instruments"""
    print 'Connecting instruments'
    try:
        for option in _conf.options('PVs'):
            connect(_conf.get('PVs',option))
        print 'Instrument initialization complete'
    except:
        raise Exception('Some of the instruments were not found or connected\
        , namely %s'% (option,))
                

def printf(value):
#    print value, test function
    return value

if __name__ == "__main__":
    _initpvs(_conf)
#    print('Initial positions:')
#    print(where())
