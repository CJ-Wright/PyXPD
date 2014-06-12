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
from xpd_architecture.dataapi.config._conf import _conf
import numpy as np
import os


def initDet(_conf):
    """

    :param _conf: config parser instance
        configuration file for XPD beamline
    :return: confail: PVs that failed to be connected
    :return conpass: PVs that passed connection test
    """
    confail={}
    conpass={}
    print 'Connecitng Dector'
    for option in _conf.options('Detector PVs'):
        try:
            connect(_conf.get('Detector PVs',option), timeout=1)
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

__detectorD=dict()
for option in _conf.options('Detector PVs'):
    __detectorD[option]=_conf.get('Detector PVs',option)


def wave_conv_str(data):
    """
    This function converts between waveforms and strings for EPICS commands
    :parameter data: the waveform or string to be converted
    :return string or bytes: Human or spec readable translation of the data.
    """
    if type(data) is str:
        return (data,'ascii')
    else:
        arr_bytes = bytes(list(data))
        arr_string = arr_bytes.decode('utf-8')
        return arr_string

#ToDO:This function may not work on PE detectors 'File (None of the file parameters in NDFile)'
#TODO: Rewrite this function to work with file template,
# TODO:pass variables into appropriate NDFile PVs and the template into template


def SetFile(dirname=None,filename=None, file_format=None,
            metadata=None, increment=None):
                
    if filename is not None:
        internalfilename, ext= os.path.splitext(filename)
        
        #File Numbering Logic block
        if increment is 'Auto':
            internalfilename=internalfilename+'(Meta'+metadata+')'
            caput(__detectorD['FileNum']+'FileNumber', 0)
            caput(__detectorD['autoi'], 1)
        elif increment is not None:
            internalfilename=internalfilename+'(Meta'+metadata+')'+str(increment)
        else:
            internalfilename=internalfilename+'(Meta'+metadata+')'
        
        if os.path.exists(dirname) is False:
            print 'The directory %s does not exist, would you like to make it?'
            if raw_input('make directory? y/[n]') is 'y':
                os.mkdir(dirname)
            #ToDO:Need to set file format
        internalpath=os.path.join(dirname, internalfilename)
        if os.path.exists(internalpath) is True:
            print 'File already exists, please choose another file'
        else:
    #        path,destfile=os.path.split(internalpath)
            if increment is 'Auto':
                caput(__detectorD['file_temp'],wave_conv_str(internalpath+'_%4.4d'+file_format))
            else:
                caput(__detectorD['file_temp'],internalpath+file_format)


def Acquire(state=None,subs=None,Time=None):
    AcquireTime(Time)
    Exposures(subs)
    if state in ['Start','start', 1]:
        caput(__detectorD['aq'], 1)
    elif state in ['Stop','stop', 0]:
        caput(__detectorD['aq'], 0)
    print caget(__detectorD['status'])
    return caget(__detectorD['status'])


def AcquireTime(Time=None):
    if Time!=None:
        caput(__detectorD['acquiretime'],Time)
    else:
        print caget(__detectorD['acquiretimerbv'])
        return caget(__detectorD['acquiretimerbv'])


def NumImages(Number=None):
    if Number!=None and type(Number) is int:
        caput(__detectorD['NumImages'],Number)
    elif type(Number) is not int:
        print 'The number of images to be generated must be an integer %s is not an integer' % (Number,)
    else:
        print('# of Images: '+caget(__detectorD['NumImagesRBV']))
        return caget(__detectorD['NumImagesRBV'])


def Exposures(exp=None):
    if exp is not None:
        caput(__detectorD['NumExp'],exp)
    else:
        print caget(__detectorD['NumExpRBV'])
        return caget(__detectorD['NumExpRBV'])


def Light_Field():
    """
    Takes light field image for future masking use.
    """
    #turn on source
    Acquire('Start')
    pass


def Dark_Field(pathname=None,filename=None, file_format=None,
            metadata=None, increment=None,
            Dark_subframes=None, Dark_exp_time=None):
    """
    Takes dark field image for subtraction
    :parameter pathname: Name of file path to directory for depositing file
    :parameter filename: Name of file to save image
    :parameter file_format
    """
    SetFile(dirname=pathname,filename=filename+'.dark', file_format=file_format,
            metadata=metadata, increment=increment)
    
    print 'Write dark file to:'
    print caget(__detectorD['pv']+'FileTemplate_RBV')
    
    Shutter(0)
    Acquire('Start', subs=Dark_subframes, Time=Dark_exp_time)


def Shutter(state=None):
    """
    Opens/closes the beamline shutter
    """
    if state==None:
        if _conf.get('Util PVs','shutter')==1:
            print 'Shutter open'
            return 1
        else:
            print 'Shutter closed'
            return 0
    if state in ['open', 'Open', 'Op',1]:
        caput(_conf.get('Util PVs','shutter'),1)
        Shutter()
    elif state in ['close, Close, Cl',0]:
        caput(_conf.get('Util PVs','shutter'),0)
        Shutter()


