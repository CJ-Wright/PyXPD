"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""
from pyXPD.instrumentapi.motion.motors.status import *
from pyXPD.instrumentapi.areaDetector.DetCore import *
import cothread
from cothread.catools import *
from pyXPD.instrumentapi.config._conf import _conf

"""Motor Commands"""


def where(motor=None):
    """
    Returns:
        motor coordinates
    """
    if motor == 'all':
        print motorD
    if motor in motorD.keys():
        posd = dict()
        posd[motor] = caget(_conf.get('Motor PVs', motor))
        print posd
    else:
        posd = dict()
        for option in _conf.options('Motor PVs'):
            if 'motor' in str(_conf.get('Motor PVs', option)):
                posd[str(option)] = caget(_conf.get('Motor PVs', option))
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
    A : ndarray
        array of motor positions and function outputs
    Example
    -------
    ascan('samx',-1, 1, .5,printf, 5)
    """

    x = None
    y = None
    print 'start move'
    # Use kwargs to change pv settings? i.e. motor speed?
    for entry in np.arange(start, finish + step, step):
        move(alias, entry, wait=True)
        if x == None:
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
    Example
    -------
    rscan(printf, 5, step=.1, finish=5, start=-5, alias='samx')
    """
    A = None
    for entry in np.arange(float(position(alias)) + start, float(position(alias)) + finish + step, step):
        move(alias, entry, wait=True)
        func(*args)
        if A == None:
            print 'starting data aquesition'
            A = [position(alias), func(*args)]
        else:
            A = np.vstack((A, [position(alias), func(*args)]))
    return A


def gscan(func, *args, **kwargs):
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
    Example
    -------
    gscan(printf,5,ax1={'alias':'samx','start':-1,'finish':1,'step':.5,'movetype':'ABS'},ax2={'alias':'samy','start':-1,'finish':1,'step':.5,'movetype':'ABS'})
    """
    out = dict()
    for key in sorted(kwargs.keys()):
        motormovedict = kwargs[key]
        print motormovedict['alias']
        if motormovedict['movetype'] == 'ABS':
            A = ascan(func, *args, **motormovedict)
        elif motormovedict['movetype'] == 'REL':
            A = rscan(func, *args, **motormovedict)
        else:
            raise Exception('Movetype not correctly specified')
        out[motormovedict['alias']] = A
    return out


def stop(alias):
    """
    Stop selected process, or all processies, NOT IMPLEMENTED
    """


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
    
    Example
    -------
    mesh(printf,-1,serpentmove=True, ax1={'movetype': 'ABS', 'alias': 'samy', 'step': 0.5, 'finish': 1, 'start': -1},ax2={'movetype': 'ABS', 'alias': 'samx', 'step': 0.5, 'finish': 1, 'start': -1})
    """
    # print 'n\n\n'
    # print kwargs['serpentmove']
    A = None
    B = None
    # kwargs['ax1']=ax1
    # kwargs['ax2']=ax2
    if kwargs.has_key('serpentmove') == False:
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
    if kwargs['serpentmove'] == False:
        print 'start move'
        for entry in ax1graphax:
            move(ax1['alias'], entry, wait=True)
            for entry in ax2graphax:
                move(ax2['alias'], entry, wait=True)
                if A == None:
                    A = [position(ax2['alias']), func(*args)]
                else:
                    A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            if B == None:
                B = A[:, 1]
                A = None
            else:
                B = np.column_stack((B, A[:, 1]))
                A = None
    else:
        print 'start move'
        i = 0
        for entry in ax1graphax:
            move(ax1['alias'], entry, wait=True)
            if i % 2 == 0:
                for entry in ax2graphax:
                    move(ax2['alias'], entry, wait=True)
                    if A == None:
                        A = [position(ax2['alias']), func(*args)]
                    else:
                        A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            else:
                for entry in -ax2graphax:
                    move(ax2['alias'], entry, wait=True)
                    if A == None:
                        A = [position(ax2['alias']), func(*args)]
                    else:
                        A = np.vstack((A, [position(ax2['alias']), func(*args)]))
            if B == None:
                B = A[:, 1]
                A = None
            else:
                B = np.column_stack((B, A[:, 1]))
                A = None
            i += 1
    return B, ax1graphax, ax2graphax
               
