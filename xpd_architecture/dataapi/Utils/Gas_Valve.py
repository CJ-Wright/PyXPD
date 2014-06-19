'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'


from xpd_architecture.dataapi.config._conf import _conf, __initPV
import cothread
from cothread.catools import *

confail, conpass= __initPV(section='Gas Valve PVs')

def loadGasConfig(configuration=None,config=None):
    """

    :param _conf: configuration file to load the gas names from
    :type _conf: safeconfig instance
    :param configuration: section of configuration file to use, allows user to use alternate gas
     configuration, which is preset in the configuration file
    :type configuration: string
    :return: dictionary of valve assignments {gas name: valve number}
    :rtype: dict
    """
    if config is None:
        config=_conf
    if configuration is None:
        configuration='Default Gas Assignments'
    valve_assignments=dict()
    for option in config.options(configuration):
        # print option, config.get(configuration, option)
        valve_assignments[option] = dict(Valve=config.get(configuration, option).split(':')[0],
                                        Pos=int(config.get(configuration, option).split(':')[1]))
    return valve_assignments

valve_asg=loadGasConfig()


def flowname_from_gas(GasName):
    valvename=valve_asg[Gas_Name].split(':')[0]
    valvenumber=valvename.split('_')[1]
    return 'Flow_'+str(valvenumber)

def gas_position(Valve=None, Pos=None):
    """

    :param Valve: Valve to use
    :type Valve: str
    :param new_position: new Valve position
    :type new_position: int
    :return:
    :rtype:
    """
    # print Valve, Pos

    if Pos is None and Valve is None:
        if valve_asg.has_key('Valve_2'):
            if str(caget(conpass['Valve_1'])) is not valve_asg['Valve_2']['Pos']:
                return 'Valve_1', int(caget(conpass['Valve_1']))
            else:
                return 'Valve_2', int(caget(conpass['Valve_2']))
        else:
            return 'Valve_1', int(caget(conpass['Valve_1']))

    elif Valve is None:
        Valve='Valve_1'

    if Valve=='Valve_2':
        caput(conpass['Valve_1'], valve_asg['Valve_2']['Pos'])

    if type(Pos) is int:
        caput(conpass[Valve], Pos)
        return gas_position()
    else:
        print 'Valve position must be integer'


