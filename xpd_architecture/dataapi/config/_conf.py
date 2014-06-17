# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:55:39 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

from cothread.catools import *

def __loadConfig():
    import os.path
    import ConfigParser
    cf=ConfigParser.SafeConfigParser()
    cf.optionxform=str
    cf.read([
        '/etc/XPD.conf',
        os.path.expanduser('~/XPD.conf'),
        'XPD.conf',
        '/home/xpdlabuser/Spyder_Projects/XPD+_architecture/xpd_architecture/dataapi/config/XPD.conf'
    ])
    return cf
    
_conf=__loadConfig()


def __initPV(_conf=_conf, section=None):
    confail={}
    conpass={}
    print 'Connecitng '+ section
    for option in _conf.options(section):
        try:
            connect(_conf.get(section, option), timeout=1)
            print 'PV passed:', option
            conpass[option]=_conf.get(section, option)
        except:
            print 'PV failed:', option
            confail[option]=_conf.get(section ,option)
            pass
#            raise Exception('Some of the detectors were not found or could not connect, \
#            namely:\n %s, pv=%s'% (option,_conf.get('Detector PVs',option)))
#    print 'failed: \n', confail
#    print '\n\n'
#    print 'passed: \n', conpass
    print section+' connection complete'
    return confail, conpass