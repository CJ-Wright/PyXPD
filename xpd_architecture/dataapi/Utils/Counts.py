# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:46:01 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from xpd_architecture.dataapi.config._conf import _conf, __initPV
import cothread
from cothread.catools import *


confail, conpass=__initPV(section='Count PVs')

def flux_counts(position=None):
    """
    This function returns the counts from the various flux detectors, including the photodiode.
    :param position: Name of position of flux detector
    :type position:str
    :return: countD: Dictionary of positions and their counts
    :rtype: dict
    :return x: the counts at the specified position
    :rtype x: float
    """
    if position is None:
        countD=dict()
        for option in _conf.options('Count PVs'):
            countD[option]=caget(_conf.get('Count PVs', option))
            print option+': '+str(countD[option])
        return countD
    else:
        x=caget(_conf.get('Count PVs', position))
        print x
        return x
