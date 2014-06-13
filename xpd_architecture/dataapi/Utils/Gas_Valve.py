'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'


from xpd_architecture.dataapi.config._conf import *
import cothread
from cothread.catools import *

confail, conpass= _initDet(section='Gas Valve PVs')

def loadGasConfig(configuration=None,_conf=None):
    """

    :param _conf: configuration file to load the gas names from
    :type _conf: safeconfig instance
    :param configuration: section of configuration file to use, allows user to use alternate gas
     configuration, which is preset in the configuration file
    :type configuration: string
    :return: dictionary of valve assignments {gas name: valve number}
    :rtype: dict
    """
    if _conf is None:
        _conf=_conf
    if configuration is None:
        configuration='Default Gas Assignments'
    valve_assignments=dict()
    for option in _conf.options(configuration):
        valve_assignments[option]=_conf.get(configuration, option)
    return valve_assignments
valve_asg=loadGasConfig()

def gas_position(valve=None, new_position=None):
    """

    :param valve: valve to use
    :type valve: str
    :param new_position: new valve position
    :type new_position: int
    :return:
    :rtype:
    """
    if valve is None:
        valve='Valve_1'
    if new_position is None:
        return caget(conpass[valve])
    elif new_position is int:
        caput(conpass[valve], new_position)
        return gas_position(valve)
    else:
        print 'Valve position must be integer'


