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
import os


def initDet(_conf):
    confail={}
    conpass={}
    print 'Connecitng Dector'
    for option in _conf.options('Detector PVs'):
        try:
            connect(_conf.get('Detector PVs',option), timeout=0)
            print 'PV passed:', option
            conpass[option]=_conf.get('Detector PVs',option)
        except:
            try:
                getv=caget(_conf.get('Detector PVs',option))
                print 'PV get passed:', option, getv
            except:
                print 'PV failed:', option            
                confail[option]=_conf.get('Detector PVs',option)
                pass
    if confail=={}:
        print 'Detector initialization complete'
    else:
        print 'Some PVs did not load, see confail'
    return confail, conpass

        
confail,conpass=initDet(_conf)

_detectorD=dict()
for option in _conf.options('Detector PVs'):
    _detectorD[option]=_conf.get('Detector PVs',option)

#XXX:This function may not work on PE detectors 'File (None of the file parameters in NDFile)'
def SetFile(dirname=None,filename=None, file_format=None,
            metadata=None, increment=None):
                
    if filename is not None:
        internalfilename, ext= os.path.splitext(filename)
        
        #File Numbering Logic block
        if increment is 'Auto':
            internalfilename=internalfilename+'(Meta'+metadata+')'
#            caput(detectorD['pv']+'FileNumber',0)
            caput(_detectorD['autoi'],1)
        elif increment is not None:
            internalfilename=internalfilename+'(Meta'+metadata+')'+str(increment)
        else:
            internalfilename=internalfilename+'(Meta'+metadata+')'
        
        if os.path.exists(dirname) is False:
            print 'The directory %s does not exist, would you like to make it?'
            os.mkdir(dirname)
#XXX:Need to set file format
        internalpath=os.path.join(dirname, internalfilename)
        if os.path.exists(internalpath) is True:
            print 'File already exists, please choose another file'
        else:
    #        path,destfile=os.path.split(internalpath)
            if increment is 'Auto':
                caput(_detectorD['file_temp'],internalpath+'_%4.4d'+file_format)
            else:
                caput(_detectorD['file_temp'],internalpath+file_format)
    
def Acquire(state=None,subs=None,Time=None):
    AcquireTime(Time)
    Exposures(subs)
    if state in ['Start','start',1]:
        caput(detectorD['aq'],1)
    elif state in ['Stop','stop',0]:
        caput(detectorD['aq'],0)
    print caget(detectorD['status'])
    return caget(detectorD['status'])
def AcquireTime(Time=None):
    if Time!=None:
        caput(_detectorD['acquiretime'],Time)
    else:
        print caget(_detectorD['acquiretimerbv'])
        return caget(_detectorD['acquiretimerbv'])

def NumImages(Number=None):
    if Number!=None and type(Number) is int:
        caput(_detectorD['NumImages'],Number)
    elif type(Number) is not int:
        print 'The number of images to be generated must be an integer %s is not an integer' % (Number,)
    else:
        print('# of Images: '+caget(_detectorD['NumImagesRBV']))
        return caget(_detectorD['NumImagesRBV'])

def Exposures(exp=None):
    if exp is not None:
        caput(_detectorD['NumExp'],exp)
    else:
        print caget(_detectorD['NumExpRBV'])
        return caget(_detectorD['NumExpRBV'])
def Light_Field():
    """
    Takes light field image for future masking use.
    """
    #turn on source
    Acquire('Start')
    pass

def Dark_Field(dirname=None,filename=None, file_format=None,
            metadata=None, increment=None,Dark_subframes=None, Dark_exp_time=None):
    """
    Takes dark field image for subtraction
    """
    SetFile(dirname=pathname,filename=filename+'.dark', file_format=file_format,
            metadata=Metadata, increment=None)
    
    print 'Write dark file to:'
    print caget(detectorD['pv']+'FileTemplate_RBV')
    
    Shutter(0)
    
    Acquire('Start', Dark_exp_time)
    
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


