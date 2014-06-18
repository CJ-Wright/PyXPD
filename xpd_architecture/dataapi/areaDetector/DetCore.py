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
from xpd_architecture.dataapi.config._conf import _conf, __initPV
import numpy as np
import os


confail,conpass=__initPV(_conf, 'Detector PVs')

__detectorD=dict()
for option in _conf.options('Detector PVs'):
    __detectorD[option]=_conf.get('Detector PVs',option)
__fileD=dict()
for option in _conf.options('Detector files'):
    __fileD[option]=_conf.get('Detector files',option)


def wave_conv_str(data):
    """
    This function converts between waveforms and strings for EPICS commands
    :parameter data: the waveform or string to be converted
    :return string or bytes: Human or spec readable translation of the data.
    """
    if type(data) is str:
        return bytearray(data,'ascii')
    else:
        arr_string="".join(map(chr,(list(data)))[:-1])
        return arr_string


def SetFile(dirname=None,filename=None,
            metadata=None, increment=None, save='Auto', file_format=None):
                
    if filename is not None:
        internalfilename, ext= os.path.splitext(filename)
        NDFileName= internalfilename
        wave_conv_str(NDFileName)
        caput(__detectorD['FileName'], wave_conv_str(NDFileName))

    if dirname is not None and os.path.exists(dirname):
        NDFilePath=dirname
        caput(__detectorD['Path'], wave_conv_str(NDFilePath))

    if save=='Auto':
        NDAutoSave=1
    else:
        NDAutoSave=0
    caput(__detectorD['AutoS'], NDAutoSave)

    formats=__fileD['SupFiles'].split(',')
    for ff in formats:
        file_formatname, ext=ff.split(':')
        if file_format==file_formatname:
            NDFileFormat= file_format
            caput(__detectorD['Format'], NDFileFormat)
            end=ext
            break
    else:
        caput(__detectorD['Format'], 'TIFF')
        end='.tif'
    if increment is 'Auto':
        NDAutoIncrement= 1
        caput(__detectorD['AutoI'], NDAutoIncrement)
        NDFileTemplate="%s%s%4.4d"+end

    elif increment is 'Multi-Auto':
        NDFileNumber=0
        NDAutoIncrement=1
        caput(__detectorD['FileNum'], NDFileNumber)
        caput(__detectorD['AutoI'], NDAutoIncrement)
        NDFileTemplate="%s%s%4.4d"+end

    elif increment is not None:
        if type(increment) is not int:
            print 'Only integer increments allowed'
        else:
            NDFileNumber=increment
            caput(__detectorD['FileNum'], NDFileNumber)
            NDFileTemplate="%s%s%4.4d"+end
    else:
        NDFileTemplate="%s%s"+end
    caput(__detectorD['File_Temp'],wave_conv_str(NDFileTemplate))
    return wave_conv_str(caget(__detectorD['FullName']))


def Acquire(state=None,subs=None,Time=None):
    AcquireTime(Time)
    Exposures(subs)
    if state in ['Start','start', 1]:
        caput(__detectorD['Aq'], 1)
    elif state in ['Stop','stop', 0]:
        caput(__detectorD['Aq'], 0)
    print caget(__detectorD['Status'])
    return caget(__detectorD['Status'])


def AcquireTime(Time=None):
    print Time
    if Time!=None:
        caput(__detectorD['AcquireTime'],Time)
    else:
        print caget(__detectorD['AcquireTimeRBV'])
        return caget(__detectorD['AcquireTimeRBV'])


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
    
    # print 'Write dark file to:'
    # print caget(__detectorD['File_Temp']+'_RBV')
    
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


# print SetFile(dirname='/home/xpdlabuser/Spyder_Projects/XPD+_architecture/test',filename='test1',
#             metadata=None, increment=None, save='Auto', file_format='TIFF')
# print wave_conv_str(caget(__detectorD['File_Temp']+'_RBV'))