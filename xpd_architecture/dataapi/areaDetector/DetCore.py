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
import os.path


def initDet(_conf):
    print 'Connecitng Dector'
    try:
        for option in _conf.options('PVs'):
            if 'det' in str(_conf.get('PVs',option)):
                connect(_conf.get('PVs',option))
        print 'Detector initialization complete'
    except:
        raise Exception('Some of the detectors were not found or could not connect\
        , namely:\n %s, pv=%s'% (option,_conf.get('PVs',option)))
    print 'Finding offset/gain/bad pixel correction files'
    try:
        for option in _conf.options('Detector files'):
            os.path.isfile(option)
    except:
        raise Exception('Some of the files were not found or could not connect\
        , namely:\n %s, pv=%s'% (option,_conf.get('Detector files',option)))
        
initDet(_conf)

detectorD=dict()

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
    Shutter(0)
    StartAq()
    
    pass

def Shutter(state=None):
    """
    Opens/closes the beamline shutter
    """
    if state==None:
        if _conf.get('PVs','shutter')==1:
            print 'Shutter open'
        else:
            print 'Shutter closed'
    if state in ['open', 'Open', 'Op',1]:
        caput(_conf.get('PVs','shutter'),1)
        Shutter()
    elif state in ['close, Close, Cl',0]:
        caput(_conf.get('PVs','shutter'),0)
        Shutter()


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

def Gain(Frames=None):
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
        else:
            print 'Offset not yet available'
    else:
        caput(detectorD['pv']+'PENumGainFrames',Frames)
        print 'Starting Gain aquesition'
        caput(detectorD['pv']+'PEAcquireOffset',1)
        while caget(detectorD['pv']+'PECurrentGainFrame')!=Frames:
            print 'Collecting frame number '+str(caget(detectorD['pv']+'PECurrentGainFrame'))
        print 'Finished Gain aquesition, Gain now in use'
        caput(detectorD['pv']+'PEUseGain',1)

def load_Offset_and_Gain(Filename=None):
    if Filename==None:
        #GUI LOAD FILE PROMPT
    