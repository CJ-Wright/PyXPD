"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the user scans for the motors
"""
from pyXPD.instrumentapi.motion.motors.status import *
import pyXPD.instrumentapi.motion.motors.status as status
from pyXPD.instrumentapi.areaDetector.DetCore import *
from pyXPD.userapi.Master_commands import printf
from cothread.catools import *
from pyXPD.instrumentapi.config._conf import _conf
import numpy as np

"""Motor Commands"""


def where(motor=None):
    """
    Get information on the motors

    Parameters
    ----------
    motor: str
        Motor alias

    Returns:
    -------
        motor coordinates

    >>> where('samx')

    >>> where()
    """
    if motor == 'all':
        print motorD
    if motor in motorD.keys():
        posd = dict()
        posd[motor] = caget(status.pv_pass[motor])
        print posd
    else:
        posd = dict()
        for option in status.pv_pass.keys():
            posd[str(option)] = caget(status.pv_pass[option])
            print posd
        return posd


def ascan(alias, start, finish, step, func, *args, **kwargs):
    """
    Scan from one position to another, performing a function at each step
    
    Parameters
    ----------
    alias : string
        Name of direction e.g. x, y, phi, etc.
    start : float
        Starting position for scan, absolute
    finish : float
        Ending position for scan, absolute
    step : float
        Step size betwfunceen function calls
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments

    Returns
    -------
    x, y : arrays
        array of motor positions and function outputs


    >>> ascan('samx', -1, 1, .5, printf, 5)
    start move
    starting data acquisition
    ([-1.0, -0.5, 0.0, 0.5, 1.0], [5, 5, 5, 5, 5])
    """

    x = None
    y = None
    print 'start move'
    # Use kwargs to change pv settings? i.e. motor speed?
    for entry in np.arange(start, finish + step, step):
        move(alias, entry, wait=True)
        if x is None:
            print 'starting data aquesition'
            x = [position(alias)]
            y = [func(*args)]
        else:
            x.append(position(alias))
            y.append(func(*args))
    return x, y


def rscan(alias, start, finish, step, func, *args, **kwargs):
    """
    Scan from one position to another, performing a function at each step
    
    Parameters
    ----------
    alias : string
        Name of direction e.g. x, y, phi, etc.
    start : float
        Starting position for scan, relative
    finish : float
        Ending position for scan, relative
    step : float
        Step size between function calls
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments

    Returns
    -------
    A : ndarray
        array of motor positions and function outputs

    >>> rscan('samx', -1, 1, .5, printf, 5)
    starting data aquesition
    ([0.0, 0.5, 1.0, 1.5, 2.0], [5, 5, 5, 5, 5])
    """
    x = None
    y = None
    for entry in np.arange(float(position(alias)) + start, float(position(alias)) + finish + step, step):
        move(alias, entry, wait=True)
        if x is None:
            print 'starting data acquisition'
            x = [position(alias)]
            y = [func(*args)]
        else:
            x.append(position(alias))
            y.append(func(*args))
    return x, y


# TODO: Need new gscan output if any
def gscan(list_of_moves, func, *args, **kwargs):
    """
    Most general scan, each row is a new direction with start stop and step functions
    
    Parameters
    ----------
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments
    **kwargs:
        Keyword arguments for the scan

    Returns
    -------
    A : ndarray
        array of motor positions and function outputs

    >>> gscan([{'alias':'samx','start':-1,'finish':1,'step':.5, 'movetype':'ABS'},{'alias':'samy','start':-1,'finish':1,'step':.5,'movetype':'ABS'}],printf, 5,)
    samx
    start move
    starting data aquesition
    samy
    start move
    starting data aquesition
    {'samy': ([-1.0, -0.5, 0.0, 0.5, 1.0], [5, 5, 5, 5, 5]), 'samx': ([-1.0, -0.5, 0.0, 0.5, 1.0], [5, 5, 5, 5, 5])}
    """
    out = dict()
    for element in list_of_moves:
        motormovedict = element
        print motormovedict['alias']
        if motormovedict['movetype'] == 'ABS':
            A = ascan(motormovedict['alias'], motormovedict['start'], motormovedict['finish'], motormovedict['step'],
                      func, *args)
        elif motormovedict['movetype'] == 'REL':
            A = rscan(motormovedict['alias'], motormovedict['start'], motormovedict['finish'], motormovedict['step'],
                      func, *args)
        else:
            raise Exception('Movetype not correctly specified')
        out[motormovedict['alias']] = A
    return out


def stop(alias):
    """
    Stop selected process, or all processes, NOT IMPLEMENTED
    """
    pass


# TODO: these are called with wait functions
def mesh(ax1, ax2, func, *args, **kwargs):
    """
    Performs function on each position within the 2 coordinates, creating a matrix
    of data points.
    
    Parameters
    ----------
    ax1: Dictionary
        This dictionary contains all the information about your scan in the first \
        direction. ie ax1={'movetype': 'ABS', 'alias': 'samy', 'step': 0.5, 'finish': 1, 'start': -1}
    ax2: Dictionary
        This dictionary contains all the information about your scan in the first \
        direction. ie ax2={'movetype': 'ABS', 'alias': 'samx', 'step': 0.5, 'finish': 1, 'start': -1}
    func: function
        This function is called at every point within the bounds of the surface
    *args:
        Function arguments
    **kwargs:
        Keyword arguments for the motormove
        
    
    Returns
    -------
    B: 2D array
        This array hold all the data returned by the function
    ax1graphax: 1D array
        This array holds all the points tested in the ax1 direction
    ax2graphax: 1D array
        This array holds all the points tested in the ax2 direction

    >>> mesh({'movetype': 'ABS', 'alias': 'samy', 'step': 0.5, 'finish': 1, 'start': -1},{'movetype': 'ABS', 'alias': 'samx', 'step': 0.5, 'finish': 1, 'start': -1},printf,-1,serpentmove=True)
    start move
    (array([[-1., -1., -1., -1., -1.],
           [-1., -1., -1., -1., -1.],
           [-1., -1., -1., -1., -1.],
           [-1., -1., -1., -1., -1.],
           [-1., -1., -1., -1., -1.]]), array([-1. , -0.5,  0. ,  0.5,  1. ]), array([-1. , -0.5,  0. ,  0.5,  1. ]))


    """
    # print 'n\n\n'
    # print kwargs['serpentmove']
    A = None
    B = None
    # kwargs['ax1']=ax1
    # kwargs['ax2']=ax2
    if not kwargs.has_key('serpentmove'):
        kwargs['serpentmove'] = True
    # TODO: Compress these if functions down to a single if and else
    if ax1['movetype'] == 'REL':
        ax1graphax = np.arange(float(position(ax1['alias'])) + ax1['start'],
                               float(position(ax1['alias'])) + ax1['finish'] + ax1['step'], ax1['step'])
    if ax2['movetype'] == 'REL':
        ax2graphax = np.arange(float(position(ax2['alias'])) + ax2['start'],
                               float(position(ax2['alias'])) + ax2['finish'] + ax2['step'], ax2['step'])
    if ax1['movetype'] == 'ABS':
        ax1graphax = np.arange(ax1['start'], ax1['finish'] + ax1['step'], ax1['step'])
    if ax2['movetype'] == 'ABS':
        ax2graphax = np.arange(ax2['start'], ax2['finish'] + ax2['step'], ax2['step'])
    if not kwargs['serpentmove']:
        print 'start move'
        for entry1 in ax1graphax:
            move(ax1['alias'], entry1, wait=True)
            for entry2 in ax2graphax:
                move(ax2['alias'], entry2, wait=True)
                if A is None:
                    A = [position(ax2['alias']), func(*args)]
                else:
                    A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            if B is None:
                B = A[:, 1]
                A = None
            else:
                B = np.column_stack((B, A[:, 1]))
                A = None
    else:
        print 'start move'
        i = 0
        for entry1 in ax1graphax:
            move(ax1['alias'], entry1, wait=True)
            if i % 2 == 0:
                for entry2 in ax2graphax:
                    move(ax2['alias'], entry2, wait=True)
                    if A is None:
                        A = [position(ax2['alias']), func(*args)]
                    else:
                        A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            else:
                for entry2 in -ax2graphax:
                    move(ax2['alias'], entry2, wait=True)
                    if A is None:
                        A = [position(ax2['alias']), func(*args)]
                    else:
                        A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            if B is None:
                B = A[:, 1]
                A = None
            else:
                B = np.column_stack((B, A[:, 1]))
                A = None
            i += 1
    return B, ax1graphax, ax2graphax
               
