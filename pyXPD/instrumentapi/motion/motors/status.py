"""
Created on Wed Jun  4 15:19:44 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved.
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the basic motor motions and valuables
"""
__author__ = 'Christopher J. Wright'

from cothread.catools import *
from decimal import *
from pyXPD.instrumentapi.config._conf import _conf, __initPV


# this is used later on for the determination if moves are in resolution
getcontext().prec = 8

# read configuration file motor section, and test their connection
pv_fail, pv_pass = __initPV(section='Motor PVs')

# create motor dictionary, which will hold information about the motors
motorD = dict()
# loop loads up the pv information for the pvs that pass the connection test
for option in pv_pass:
    pv = _conf.get('Motor PVs', option)
    motorD[option] = {'pv': pv, 'low': caget(pv + '.LLM'), 'high': caget(pv + '.HLM'), 'EGU': caget(pv + '.EGU'),
                      'res': caget(pv + '.MRES')}


def move(alias=None, value=None, wait=False):
    """
    Provides movement interface with the motor PVs, while checking that the endpoint is within the bounds of the soft \
    limits and the resolution of the motors.  The positions are absolute with respect to the motor's internal axis.

    Parameters
    ----------
    alias: str
        The name of the motor to be moved, which is translated via the `motorD` into a PV name
    value: float
        Ending motor position (absolute), which should be in the motor resolution, in the motors axis
    wait: bool, optional
        Whether or not to bind the thread while waiting for the motor move to stop

    Returns
    -------
    None

    Raises
    ------
    Precision error
        If the endpoint is specified with more resolution than the motor allows

    This function will move the motor to -1.5 mm and bind the thread in the process

    >>> move('samx', -1.5, wait=True)

    This will fail, the resolution of the motors is too low
    >>> move('samx', .00000001, wait=False)
    Traceback (most recent call last):
    Exception: Move specified with more precision than instrument allows

    >>> move('samx', 10000000, wait=False)
    Traceback (most recent call last):
    Exception: Out of Bounds, move beyond the soft limit
     """
    # load motor specific parameters from the motor dictionary
    motor = motorD[alias]
    # check final position within limits
    if motor['low'] <= value <= motor['high']:
        # check is move is within motor resolution,
        if abs(Decimal(value).remainder_near(Decimal(motor['res']))) < 1e-10:
            # Start move
            caput(motor['pv'], value, wait=wait, timeout=None)
        else:
            raise Exception('Move specified with more precision than instrument allows')
    else:
        raise Exception('Out of Bounds, move beyond the soft limit')


def rmove(alias=None, value=None, wait=False):
    """
    Provides movement interface with the motor PVs, while checking that the endpoint is within the bounds of the soft \
    limits and the resolution of the motors.  The positions are relative to the motors current positions

    Parameters
    ----------
    alias: str
        The name of the motor to be moved, which is translated via the `motorD` into a PV name
    value: float
        Ending motor position, which should be in the motor resolution
    wait: bool, optional
        Whether or not to bind the thread while waiting for the motor move to stop

    Returns
    -------
    None

    Raises
    ------
    Precision error
        If the endpoint is specified with more resolution than the motor allows

    This function will move the motor to -1.5 mm from the current position and bind the thread in the process

    >>> rmove('samx', -1.5, wait=True)

    This will fail, the resolution of the motors is too low
    >>> rmove('samx', .00000001, wait=False)
    Traceback (most recent call last):
    Exception: Move specified with more precision than instrument allows

    >>> rmove('samx', 10000000, wait=False)
    Traceback (most recent call last):
    Exception: Out of Bounds, move beyond the soft limit
     """
    absvalue = value + position(alias)
    move(alias, absvalue, wait=wait)


def position(alias=None):
    """
    Get the position of a given motor or print all the motor positions

    Parameters
    ----------
    alias: str or None
        Motor name

    Returns
    -------
    float
        The position of the motor if alias given, else None

    >>> move('samx', .5)

    >>> move('samy', .3)

    >>> a=position('samx')

    >>> print(a)
    0.5

    >>> position()
    Current positions for the motors are:
    <BLANKLINE>
    Motor: samy, Position: 0.3
    Motor: samx, Position: 0.5
    """
    if alias is None:
        print('Current positions for the motors are:\n')
        for key in motorD.keys():
            print 'Motor: %s, Position: %s' % (key, position(key))
    else:
        motor = motorD[alias]
        pos = caget(motor['pv'] + '.DRBV')
        return float(pos)


def resolution(alias=None):
    """
    Get the resolution of a given motor, list of motors, or all the motors

    Parameters
    ----------
    alias: None, str, or list of str
        If None print all the resolutions and their motor names
        If str print the resolution for that motor
        If list print all the resolutions for the motors in the list

    Return
    ------
    float or dictionary
        If `alias` was a single motor then the resolution for that motor
        If `alias` was a list of motors then a dictionary of motor names and their associated resolutions

    >>> a=resolution('samx')
    0.01
    >>> print(a)
    0.01

    This only prints all the resolutions

    >>> resolution()
    Current resolutions for the motors are:
    <BLANKLINE>
    Motor: samy, Resolution: 0.01
    Motor: samx, Resolution: 0.01

    >>> resolution(['samx', 'samy'])
    Motor: samx, Resolution: 0.01
    Motor: samy, Resolution: 0.01
    {'samy': 0.01, 'samx': 0.01}

    This returns the dictionary
    """
    if alias is None:
        print('Current resolutions for the motors are:\n')
        for key in motorD.keys():
            print 'Motor: %s, Resolution: %s' % (key, motorD[key]['res'])
    elif type(alias) is str:
        print motorD[alias]['res']
        return motorD[alias]['res']
    elif type(alias) is list:
        resdict = {}
        for element in alias:
            print 'Motor: %s, Resolution: %s' % (element, motorD[element]['res'])
            resdict[element] = motorD[element]['res']
        return resdict


def multi_move(movedict=None):
    """
    This function moves multiple motors simultaneously

    Parameters
    ----------
    movedict: dict
        `movedict` contains all the parameters for the move in {'motor name': new_position}

    Returns
    -------
    None


    >>> multi_move({'samx':10, 'samy':-10})

    """
    multiD = {}
    for key, value in movedict.items():
        motor = motorD[key]
        if motor['low'] <= value <= motor['high']:
            if abs(Decimal(value).remainder_near(Decimal(motor['res']))) < 1e-10:
                multiD[motor['pv']] = value
            else:
                raise Exception('Move specified with more precision than instrument allows')
        else:
            raise Exception('Out of Bounds, the soft limit has been reached')
    for key, value in multiD.items():
        caput(key, value, wait=False)
