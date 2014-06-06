# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:19:44 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

"""
This module deals with some of the general detector aspects.
Less general aspects are dealt with in the detector specific modules
"""
import cothread
from cothread.catools import *
from dataapi.config._conf import _conf
import numpy as np


def initDet(_conf):
    print 'Connecitng Dector'
    try:
        caput()
        for option in _conf.options('PVs'):
            if 'det' in str(_conf.get('PVs',option)):
                connect(_conf.get('PVs',option))
        print 'Detector initialization complete'
    except:
        raise Exception('Some of the detectors were not found or could not connect\
        , namely:\n %s, pv=%s'% (option,_conf.get('PVs',option)))
initDet(_conf)



def StartAq():
    caput()


def Light_Field():
    """
    Takes light field image for future masking use.
    """
    pass

def Dark_Field():
    """
    Takes dark field image for subtraction
    """
    pass

def Shutter():
    """
    Opens/closes the beamline shutter
    """
    pass