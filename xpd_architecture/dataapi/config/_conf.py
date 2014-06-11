# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:55:39 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

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