# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 08:59:45 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

Design Notes:
    Three major functions CaptureSingle, CaptureMulti, CaptureCont
    Each function must contain fields for:
        Filename
        Filename incrementor
        Metadata to put into the filename
        Exposiure time
        Subframes
        Frames for Multi
        Some field for dark field acquisition pattern
        Gain/offset correction information:
            Use
            Filename to use or aquire new
            
"""
from xpd_architecture.dataapi.motion.motors.status import *
from xpd_architecture.dataapi.areaDetector.DetCore import *
from xpd_architecture.dataapi.areaDetector.DetPE import *
import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf


"""Detector Commands"""


def prep_experiment(inputgain={'Use': True, 'State': 'Default', 'OldFile':True}):
    """
    This function prepares the detector for an experiment, by checking the various detector based corrections and \
    retakeing any if nessisary.  This also checks for available x-rays
    :param inputgain:
    :return:
    """
    # Confirm X-rays
    #Tune Mono?

    #load Gain file, if old take another gain file
    if inputgain['Use'] is not False:
        Gainfile = load_Gain(_conf.get('Single Default', 'Gain File'))
        st = os.stat(Gainfile)
        age = st.st_mtime

        if age < _conf.get('Single Default', 'Gain_age') or inputgain['State'] is 'New' or Gain() is 0:
            print 'Taking new gain measurement'
            Gain(False, Frames=10)
            Gain(Use=True)
    else:
        Gain(False)


    # Take Gain images, using default settings, or other
    #OR Load Gain
    #Check Offset age
    #Take Offset images, using default settings or other
    #OR Load Gain
    #Check Bad Pixel age
    #Take new Bad Pixel stuff???
    #Load Gain
    return True


def CaptureSingle(pathname=None, filename=None, subframes=None, exp_time=None, **kwargs):
    """
    Captures an x-ray image creating a single file out of subframes with set \
    integration times
    
    CaptureSingle(pathname=None,filename=None, increment=None, file_format=None,
                  subframes=None, exp_time=None,
                  Dark_subframes=None, Dark_exp_time=None Dark_pattern=None,
                  Metadata=None,
                  Prep_bypass=False
                  Gain=None,
                  Offset=None,
                  Bad_pixel=None,
                  Automatic=False)
                  
    
    Parameters
    ----------
    filename: string
        Name of a file to save to
    subframes: int
        Number of subframes to use to write the main image
    seconds_per_subframe: float
        Number of seconds of integration time for each subframe
    Automatic: bool
        If True then uses statistical analysis to create an integration time and \
        number of subframes to make the output file statisticly signifigant out to \
        a Q(A^-1) specified by the user
    
    Returns
    -------
    A: 2D array
        Numpy array which represents the image pixels
    """
    if kwargs['Prep_bypass'] is False:
        prep_experiment(kwargs['Gain'], kwargs['Offset'], kwargs['Bad_pixel'])
    for element in ['Dark_subframes', 'Dark_exp_time', 'Dark_pattern']:
        if kwargs.has_key(element) is None:
            kwargs[element] = _conf.get('Single Default', element)

        # Dark Image Block
        if kwargs['Dark_pattern'] is 'Before' or 'Split':
            print 'Start Dark Image'
            if kwargs['Dark_pattern'] is 'Split':
                kwargs['Dark_subframes'] = np.ceil(kwargs['Dark_subframes'] / 2)
            Dark_Field(pathname, filename,
                       kwargs['file_format'], kwargs['metadata'], kwargs['increment'],
                       kwargs['Dark_subframes'], kwargs['Dark_exp_time'])
        Shutter(1)
        Acquire('Start', subframes, Time=exp_time)
        if kwargs['Dark_pattern'] is 'After' or 'Split':
            print 'Start Dark Image'
            Dark_Field(pathname, filename,
                       kwargs['file_format'], kwargs['metadata'], kwargs['increment'],
                       kwargs['Dark_subframes'], kwargs['Dark_exp_time'])


def CaptureMulti(base_filename, filename_iterator, subframes, seconds_per_subframe, offset=None, Automatic=False,
                 **kwargs):
    """
    Captures an x-ray image creating many files out of subframes with set \
    integration times
    
    Parameters
    ----------
    base_filename: string
        Name of a file to save to
    filename_iterator: number or list
        
    subframes: int
        Number of subframes to use to write the main image
    seconds_per_subframe: float
        Number of seconds of integration time for each subframe
    Automatic: bool
        If True then uses statistical analysis to create an integration time and \
        number of subframes to make the output file statisticly signifigant out to \
        a Q(A^-1) specified by the user
    
    Returns
    -------
    A: 3D array
        Numpy array which represents the images
    """
    # check that shutter is open
    #take darkfield image? or do this inside the core?
    pass
