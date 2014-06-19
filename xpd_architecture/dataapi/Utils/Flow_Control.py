'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

from xpd_architecture.dataapi.config._conf import *
from cothread.catools import *

confail, conpass= __initPV(_conf, 'Flow Meters')

def set_flow(flowmeter=None, value=None):
    caput(_conf.get('Flow Meter PVs', flowmeter),value)

def get_flow(flowmeter=None):
    return _conf.get('Flow Meter PVs', flowmeter)