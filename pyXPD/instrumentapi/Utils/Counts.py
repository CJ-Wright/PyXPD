# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:46:01 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the counts from point detectors like photodiodes
"""
from cothread.catools import *

from pyXPD.instrumentapi.config._conf import __initPV


pv_fail, pv_pass = __initPV(section='Count PVs')


def flux_counts(position=None):
    """
    This function returns the counts from the various flux detectors, including the photodiode.

    Parameters
    ----------
    position: str
        Name of position of flux detector
    Return
    -----
    countD: dict
    Dictionary of positions and their counts
    x: float
    The counts at the specified position

    >>> flux_counts('PhotoD')
    0.0
    0.0

    >>> flux_counts()
    PhotoD: 0.0
    {'PhotoD': 0.0}
    """
    if position is None:
        countD = dict()
        for pv in pv_pass:
            countD[pv] = caget(pv_pass[pv])
            print pv + ': ' + str(countD[pv])
        return countD
    else:
        x = caget(pv_pass[position])
        print x
        return x
