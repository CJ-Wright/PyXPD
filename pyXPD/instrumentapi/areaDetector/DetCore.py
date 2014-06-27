# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:19:44 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module deals with some of the general detector aspects.  Less general aspects are dealt with in the \
detector specific modules.

.. warning:: There are major issues with this module, until it is tested against the detector, it may be very unreliable

"""

import cothread
from cothread.catools import *
from pyXPD.instrumentapi.config._conf import _conf, __initPV
import numpy as np
import os


pv_fail, pv_pass = __initPV(section='Detector PVs')

__detectorD = dict()
for option in pv_pass.keys():
    __detectorD[option] = pv_pass[option]

#TODO: Make a __initFile function to initialize files
__fileD = dict()
for option in _conf.options('Detector files'):
    __fileD[option] = _conf.get('Detector files', option)


def wave_conv_str(data):
    """
    This function converts between waveforms and strings for EPICS commands

    Parameters
    ----------
    data:
        the waveform or string to be converted

    Returns
    -------
    string or bytes: Human or spec readable translation of the data.

    """
    if type(data) is str:
        return bytearray(data, 'ascii')
    else:
        arr_string = "".join(map(chr, (list(data)))[:-1])
        return arr_string

#TODO: Split up SetFile on a PV basis
def SetFile(dirname=None, filename=None,
            metadata=None, increment=None, auto_save=True, file_format=None):
    """
    Set the path, filename, increment, and file_format in preperation for acuqesition of images

    Parameters
    -----------
    dirname: str
        Path to the directory to be saved in
    filename: str
        Base file name for the image
    increment:
    auto_save: bool
        If true use auto save
    file_format:

    """
    if filename is not None:
        internalfilename, ext = os.path.splitext(filename)
        NDFileName = internalfilename
        wave_conv_str(NDFileName)
        caput(__detectorD['FileName'], wave_conv_str(NDFileName))

    if dirname is not None and os.path.exists(dirname):
        NDFilePath = dirname
        caput(__detectorD['Path'], wave_conv_str(NDFilePath))

    if auto_save == True:
        NDAutoSave = 1
    else:
        NDAutoSave = 0
    caput(__detectorD['AutoS'], NDAutoSave)

    formats = __fileD['SupFiles'].split(',')
    for ff in formats:
        file_formatname, ext = ff.split(':')
        if file_format == file_formatname:
            NDFileFormat = file_format
            caput(__detectorD['Format'], NDFileFormat)
            end = ext
            break
    else:
        caput(__detectorD['Format'], 'TIFF')
        end = '.tif'
    if increment is 'Auto':
        NDAutoIncrement = 1
        caput(__detectorD['AutoI'], NDAutoIncrement)
        NDFileTemplate = "%s%s%4.4d" + end

    elif increment is 'Multi-Auto':
        NDFileNumber = 0
        NDAutoIncrement = 1
        caput(__detectorD['FileNum'], NDFileNumber)
        caput(__detectorD['AutoI'], NDAutoIncrement)
        NDFileTemplate = "%s%s%4.4d" + end

    elif increment is not None:
        if type(increment) is not int:
            print 'Only integer increments allowed'
        else:
            NDFileNumber = increment
            caput(__detectorD['FileNum'], NDFileNumber)
            NDFileTemplate = "%s%s%4.4d" + end
    else:
        NDFileTemplate = "%s%s" + end
    caput(__detectorD['File_Temp'], wave_conv_str(NDFileTemplate))
    return wave_conv_str(caget(__detectorD['FullName']))


def Acquire(state=None, subs=None, Time=None):
    """
    Set image acquisition parameters and start acquiring images

    Parameters
    ----------
    state: {'Start', 'start', 1} or {'Stop', 'stop', 0}
        Start or Stop the detector acquisition
    subs: int
        Number of sub images to sum into one, these are taken to avoid saturating the detector during the exposure
    Time: float
        exposure time per subframe

    Return
    ------
    status;
        Status of the detector

    >>> Acquire('Start', 5, 3)

    >>> Acquire()

    >>> Acquire('Stop')
    """
    if state in ['Start', 'start', 1]:
        AcquireTime(Time)
        Exposures(subs)
        caput(__detectorD['Aq'], 1)
    elif state in ['Stop', 'stop', 0]:
        caput(__detectorD['Aq'], 0)
    print caget(__detectorD['Status'])
    return caget(__detectorD['Status'])


def AcquireTime(Time=None):
    """
    Set the acquire time

    Parameters
    ----------
    Time: float
        exposure time per subframe

    Returns
    -------
    acquire time:
        acquire time set in the detector

    >>> AcquireTime(5)

    >>> AcquireTime()

    """
    print Time
    if Time is not None:
        caput(__detectorD['AcquireTime'], Time)
    else:
        print caget(__detectorD['AcquireTimeRBV'])
        return caget(__detectorD['AcquireTimeRBV'])


#TODO: Double check documentation for NumImages/Exposures
def NumImages(Number=None):
    """
    Set the number of images in the acquisition run

    Parameters
    ----------
    Number: int
        Number of images to acquire

    Returns
    -------
    int:
        Number of images to acquire set in the detector

    >>> NumImages(5)

    >>> NumImages()
    """
    if Number != None and type(Number) is int:
        caput(__detectorD['NumImages'], Number)
    elif type(Number) is not int:
        print 'The number of images to be generated must be an integer %s is not an integer' % (Number,)
    else:
        print('# of Images: ' + caget(__detectorD['NumImagesRBV']))
        return caget(__detectorD['NumImagesRBV'])


def Exposures(exp=None):
    """
    The number of subframes per frame

    Parameters
    ----------
    exp: int
        Number of subframes per frame

    Returns
    -------
    int:
        Number of subrames per frame set in the detector\

    >>> Exposures(5)

    >>> Exposures()
    """
    if exp != None and type(exp) is int:
        caput(__detectorD['NumImages'], exp)
    elif type(exp) is not int:
        print 'The number of images to be generated must be an integer %s is not an integer' % (exp,)
    else:
        print caget(__detectorD['NumExpRBV'])
        return caget(__detectorD['NumExpRBV'])


def Light_Field(subs, Time):
    """
    Takes light field image for future masking use.  NOT IMPLEMENTED
    """
    # turn on source or move flat field generator into position
    Acquire('Start', subs, Time)
    pass


def Dark_Field(pathname=None, filename=None, file_format=None,
               metadata=None, increment=None,
               Dark_subframes=None, Dark_exp_time=None):
    """
    Takes dark field image for subtraction

    Parameters
    ----------
    pathname: str
        Name of file path to directory for depositing file
    filename: str
        Name of file to save image
    file_format: str

    metadata: str

    increment: str or int

    Dark_Subframes: int
        Number of subframes to use in the dark images
    Dark_exp_time: float
        exposure time per dark frame
    """
    SetFile(dirname=pathname, filename=filename + '.dark', file_format=file_format,
            metadata=metadata, increment=increment)

    # print 'Write dark file to:'
    # print caget(__detectorD['File_Temp']+'_RBV')

    Shutter(0)
    Acquire('Start', subs=Dark_subframes, Time=Dark_exp_time)


def Shutter(state=None):
    """
    Opens/closes the beamline shutter

    Parameters
    ----------
    state: {'open', 'Open', 'Op', 1} or {'close, Close, Cl', 0} or None
        Open or close the shutter

    Returns
    -------
    bool:
        shutter state 1=open, 0=closed

    >>> Shutter(1)

    >>> Shutter()

    >>> Shutter(0)

    >>> Shutter()

    """
    if state == None:
        if _conf.get('Util PVs', 'shutter') == 1:
            print 'Shutter open'
            return 1
        else:
            print 'Shutter closed'
            return 0
    if state in ['open', 'Open', 'Op', 1]:
        caput(_conf.get('Util PVs', 'shutter'), 1)
        Shutter()
    elif state in ['close, Close, Cl', 0]:
        caput(_conf.get('Util PVs', 'shutter'), 0)
        Shutter()


        # print SetFile(dirname='/home/xpdlabuser/Spyder_Projects/XPD+_architecture/test',filename='test1',
        # metadata=None, increment=None, save='Auto', file_format='TIFF')
        # print wave_conv_str(caget(__detectorD['File_Temp']+'_RBV'))