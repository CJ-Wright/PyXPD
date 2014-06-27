"""
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved.
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the flow meters/controllers

.. warning:: This module is not fully implemented.  This module is still pending a true EPICS interface, a method to \
to change mass flow calibrations, and other features
"""
__author__ = 'Christopher J. Wright'

from pyXPD.instrumentapi.config._conf import _conf, __initPV
from cothread.catools import *


pv_fail, pv_pass = __initPV(_conf, 'Flow Meter PVs')


def set_flow(flowmeter=None, value=None):
    """
    Sets the flow of a flowmeter

    Parameters
    ----------
    flowmeter: str
        The name of the flowmeter, as found in the configuration file
    value: float
        The new setpoint for that flowmeter

    >>> set_flow('Flow_3', 25)
    """
    caput(pv_pass[flowmeter], value)


def get_flow(flowmeter=None):
    """
    Gets the current flow for a flowmeter

    Parameters
    ----------
    flowmeter: str
        Name of the flowmeter
    """
    return caget(pv_pass[flowmeter])