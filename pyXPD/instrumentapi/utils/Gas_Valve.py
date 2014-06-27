"""
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved.
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the gas switching valve and the flowmeters effectively aliasing the switching valve positions and \
flowmeters to the gases connected.

.. warning:: This module is somewhat based on a certain geometry for the gas flow.  This geometry has the flow meters \
attached to the switching valve.  This does not impact the switching valve functions, but is needed for the flow meter \
gas based aliasing.

.. note:: Some of the gas handling is based on the assumption that there are two gas valves, which are chained one \
into another at position 5 on Valve_1.  The module may handle parallel switching valves, however this has not been \
simulated/tested.
"""
__author__ = 'Christopher J. Wright'

from pyXPD.instrumentapi.config._conf import _conf, __initPV
from pyXPD.userapi._userconf import _userconf
from cothread.catools import *

pv_fail, pv_pass = __initPV(section='Gas Valve PVs')


def loadGasConfig(configuration=None, config=None):
    """
    This loads the gas config from either the user configuration, or the default beamline config

    Parameters
    ----------
    _conf: safeconfig instance
        configuration file to load the gas names from
    configuration: str
        section of configuration file to use, allows user to use alternate gas \configuration, which is \preset in the \
        configuration file

    Returns
    --------
    dictionary:
        dictionary of valve assignments {gas name: valve number}

    >>> loadGasConfig(config=_userconf, configuration='Example User Gas Assignments')
    {'F2': {'Valve': 'Valve_1', 'Pos': 0}, 'FOOF': {'Valve': 'Valve_1', 'Pos': 2}, 'SUPER AWESOME GAS': {'Valve': 'Valve_2', 'Pos': 2}}
    """
    if config is None:
        config = _conf
    if configuration is None:
        configuration = 'Default Gas Assignments'
    valve_assignments = dict()
    for option in config.options(configuration):
        # print option, config.get(configuration, option)
        valve_assignments[option] = dict(Valve=config.get(configuration, option).split(':')[0],
                                         Pos=int(config.get(configuration, option).split(':')[1]))
    return valve_assignments


valve_asg = loadGasConfig()


def flow_name_from_gas(Gas_Name):
    """
    Generate the name of the flowmeter from the gas name

    Parameters
    ----------
    Gas_Name: str
        Name of the gas, as it appears in the userconfig file

    Returns
    -------
    str:
        Name of the Flow meter

    >>> flow_name_from_gas('H2')
    'Flow_1'
    """
    valvename = valve_asg[Gas_Name]['Valve']
    valvenumber = valvename.split('_')[1]
    return 'Flow_' + str(valvenumber)


def gas_position(Valve=None, Pos=None):
    """
    Gets the switching gas valve position, or if the arguments are not None, changes the position

    Parameters
    ----------
    Valve: str
        Valve to use
    Pos: int
        new Valve position

    Returns
    -------

    Change the Valve_1 [default valve] position
    >>> gas_position(Pos=1)
    ('Valve_1', 1)

    Get the gas valve name and position
    >>> gas_position()
    ('Valve_1', 1)

    Change the valves to pass the Valve_2 gas through Valve_1, and change the Valve_2 position
    >>> gas_position(Valve='Valve_2', Pos=2)
    ('Valve_2', 2)

    Get the gas valve name and position
    >>> gas_position()
    ('Valve_2', 2)
    """

    # If no parameters are passed in report the position
    if Pos is None and Valve is None:
        if 'Valve_2' in valve_asg.keys():
            if int(caget(pv_pass['Valve_1'])) is not int(valve_asg['Valve_2']['Pos']):
                return 'Valve_1', int(caget(pv_pass['Valve_1']))
            else:
                return 'Valve_2', int(caget(pv_pass['Valve_2']))
        else:
            return 'Valve_1', int(caget(pv_pass['Valve_1']))
    #If no valve parameter is passed in, but the position parameter is use the default valve
    elif Valve is None:
        Valve = 'Valve_1'
    #If the valve is Valve_2 switch the Valve_1 into position to use the Valve_2
    if Valve == 'Valve_2':
        caput(pv_pass['Valve_1'], valve_asg['Valve_2']['Pos'])
    #If the position is an integer change the position to asked for position
    if type(Pos) is int:
        caput(pv_pass[Valve], Pos)
        return gas_position()
    else:
        print 'Valve position must be integer'


