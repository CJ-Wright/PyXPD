# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:46:01 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from xpd_architecture.dataapi.config._conf import *
import cothread
from cothread.catools import *


def initDet(_conf):
    confail={}
    conpass={}
    print 'Connecitng Counters'
    for option in _conf.options('Count PVs'):
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
    print 'Counter initialization complete'
    return confail, conpass

def flux_counts(position=None):
    """
    This function returns the counts from the various flux detectors, including the photodiode.
    :param position: Name of position of flux detector
    :type position:str
    :return:
    :rtype:
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
