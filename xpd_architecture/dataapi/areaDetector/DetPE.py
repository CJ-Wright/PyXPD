# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 11:39:58 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf
import numpy as np
import os

def initDet(_conf):
    confail={}
    conpass={}
    print 'Connecitng Dector'
    for option in _conf.options('PE PVs'):
        try:
            connect(_conf.get('PE PVs',option), timeout=1)
            print 'PV passed:', option
            conpass[option]=_conf.get('PE PVs',option)
        except:
            print 'PV failed:', option
            confail[option]=_conf.get('PE PVs',option)
            pass
#            raise Exception('Some of the detectors were not found or could not connect, \
#            namely:\n %s, pv=%s'% (option,_conf.get('Detector PVs',option)))
#    print 'failed: \n', confail
#    print '\n\n'
#    print 'passed: \n', conpass
    print 'Detector initialization complete'
    return confail, conpass
    
    print 'Finding offset/gain/bad pixel correction files'
    try:
        for option in _conf.options('PE files'):
            os.path.isfile(option)
    except:
        raise Exception('Some of the files were not found or could not connect\
        , namely:\n %s, pv=%s'% (option,_conf.get('Detector files',option)))

confail,conpass=initDet(_conf)

def Offset(Frames=None):
    """
    Reports on the status of the internal offset correction and aquires offset correction
    
    Parameters
    ----------
    Frames: int
        Number of frames to aquire for the offset correction
    
    """
    if Frames==None:
        if caget(detectorD['pv']+'PEOffsetAvailable')==1:
            print 'Offset Available'
        else:
            print 'Offset not yet available'
    else:
        caput(detectorD['pv']+'PENumOffsetFrames',Frames)
        print 'Starting offset aquesition'
        caput(detectorD['pv']+'PEAcquireOffset',1)
        while caget(detectorD['pv']+'PECurrentOffsetFrame')!=Frames:
            print 'Collecting frame number '+str(caget(detectorD['pv']+'PECurrentOffsetFrame'))
        print 'Finished offset aquesition, offset now in use'
        caput(detectorD['pv']+'PEUseOffset',1)

def Gain(Use=False, Frames=None):
    """
    Reports on the status of the internal offset correction and aquires offset correction
    
    Parameters
    ----------
    Frames: int
        Number of frames to aquire for the offset correction
    
    """
    if Frames==None:
        if caget(detectorD['pv']+'PEGainAvailable')==1:
            print 'Gain Available'
            if Use is True:
                print 'Gain now in use'
                caput(detectorD['pv']+'PEUseGain',1)
        else:
            print 'Gain not yet available'
        return caget(detectorD['pv']+'PEGainAvailable')
    else:
        caput(detectorD['pv']+'PENumGainFrames',Frames)
        print 'Starting Gain acquesition'
        caput(detectorD['pv']+'PEAcquireGain',1)
        while caget(detectorD['pv']+'PECurrentGainFrame')!=Frames:
            print 'Collecting frame number '+str(caget(detectorD['pv']+'PECurrentGainFrame'))
        print 'Finished Gain aquesition, Gain now in use'
        caput(detectorD['pv']+'PEUseGain',1)

def load_Offset(Filename=None):
    pass
def load_Gain(Filename=None):
    return Filename    
    pass