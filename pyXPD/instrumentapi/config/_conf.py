# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:55:39 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module loads the beamline configuration file so it can be accessed by other modules
"""

from cothread.catools import *

def __loadConfig():
    """
    Load the configuration file, looking a few possible sources for XPD.conf
    """
    import os.path
    import ConfigParser
    cf=ConfigParser.SafeConfigParser()
    cf.optionxform=str
    cf.read([
        '/etc/XPD.conf',
        os.path.expanduser('~/XPD.conf'),
        'XPD.conf',
        '/home/xpdlabuser/Spyder_Projects/XPD+_architecture/pyXPD/instrumentapi/config/XPD.conf'
    ])
    return cf
    
_conf=__loadConfig()


def __initPV(_conf=_conf, section=None):
    """
    Load the PVs and check their connections, this is used in other modules as the first step

    Parameters
    ----------
    _conf: configParser instance
        This is the configuration file which holds all the PVs to be tested
    section: str
        Name of the section in the configuration file

    Returns
    -------
    pv_fail, pv_pass: dict
        Dictionaries of the PVs that failed and passed the connection test, respectively
    """
    pv_fail={}
    pv_pass={}
    print 'Connecitng '+ section
    for option in _conf.options(section):
        try:
            connect(_conf.get(section, option), timeout=1)
            print 'PV passed:', option
            pv_pass[option]=_conf.get(section, option)
        except:
            print 'PV failed:', option
            pv_fail[option]=_conf.get(section ,option)
            pass
    print section+' connection complete'
    return pv_fail, pv_pass