# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 11:39:58 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf, __initPV
import numpy as np
import os


confail, conpass=__initPV(section='PE PVs')

#TODO: make file initiator for detector corrections

print 'Finding offset/gain/bad pixel correction files'
try:
    for option in _conf.options('PE files'):
        os.path.isfile(option)
except:
    raise Exception('Some of the files were not found or could not connect\
    , namely:\n %s, pv=%s'% (option,_conf.get('Detector files', option)))

__PED=dict()
for option in _conf.options('Detector PVs'):
    __PED[option]=_conf.get('Detector PVs',option)
def Offset(Frames=None):
    """
    Reports on the status of the internal offset correction and aquires offset correction
    
    Parameters
    ----------
    Frames: int
        Number of frames to aquire for the offset correction
    
    """
    if Frames==None:
        if caget(__PED['OffAvail'])==1:
            print 'Offset Available'
        else:
            print 'Offset not yet available'
    else:
        caput(__PED['NumOffset'],Frames)
        print 'Starting offset acquisition'
        caput(__PED['AqOff'], 1)
        while caget(__PED['OffsetFrame']) != Frames:
            print 'Collecting frame number '+str(caget(__PED['OffsetFrame']))
        print 'Finished offset acquisition, offset now in use'
        caput(__PED['UseOff'], 1)

def Gain(Use=False, Frames=None):
    """
    Reports on the status of the internal offset correction and aquires offset correction
    
    Parameters
    ----------
    Frames: int
        Number of frames to aquire for the offset correction
    
    """
    if Frames==None:
        if caget(__PED['GainAvail'])==1:
            print 'Gain Available'
            if Use is True:
                print 'Gain now in use'
                caput(__PED['UseGain'],1)
        else:
            print 'Gain not yet available'
        return caget(__PED['GainAvail'])
    else:
        caput(__PED['AqGain'], 1)
        while caget(__PED['GainFrame']) != Frames:
            print 'Collecting frame number '+str(caget(__PED['GainFrame']))
        print 'Finished Gain aquesition, Gain now in use'
        caput(__PED['UseGain'],1)

def load_Offset(Filename=None):
    pass
def load_Gain(Filename=None):
    return Filename    
    pass