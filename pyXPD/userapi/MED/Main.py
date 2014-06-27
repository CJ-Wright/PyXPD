"""
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved.
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This module handles the main modulation enhanced diffraction (MED) system
"""
__author__ = 'Christopher J. Wright'

# from pyXPD.userapi.Master_commands import *
# from pyXPD.userapi.Util_commands import Mix
import matplotlib.pyplot as plt
import time
import numpy as np
import scipy.signal as signal

plt.ioff()


def ocilator_gen(functype, cycles, period, phase, resolution):
    """
    Generates an oscillating function for MED experiments
    Parameters
    ----------
    functype: str
        String which determines type of ocilator to use
    cycles: int
        Number of cycles for the total run
    period: float
        Period between peaks in seconds
    phase: float
        Additional phase to add in pi, i.e. 1
    resolution: float
        Maximum time resolution of the data in data points per second
    """

    t = np.linspace(0, cycles * period, cycles * period * resolution)
    phase = phase * np.pi
    internal = 2 * np.pi / period * t + phase

    if functype in ['sin', 'Sin']:
        ocil = np.sin(internal)
    elif functype in ['Triangle', 'tri']:
        ocil = 2 * abs(signal.sawtooth(internal)) - 1
    elif functype in ['saw']:
        ocil = signal.sawtooth(internal)
    elif functype in ['square']:
        ocil = signal.square(internal)
    plt.plot(t, ocil, 'o')
    plt.ylim(-1.5, 1.5)
    plt.show()
    return ocil


def MED(cycles=None, period=None,
        shots_per_cycle=None, subframes=None, exp_time=None,
        function_to_mod=None,
        oscillator=None, **kwargs):
    # need to check that the period and the shots_per_cycle work out
    totaltime = exp_time * subframes * shots_per_cycle * cycles
    print 'Experiment will take %s hours' % (totaltime / 60. ** 2,)
    totalepoch = totaltime + time.time()

    ocil1 = ocilator_gen(oscillator, cycles, period, 0)
    ocil2 = ocilator_gen(oscillator, cycles, period, 1)

    variableD = dict()
    for key in kwargs.keys():
        if key not in ['Constant', 'Const']:
            variableD[key] = kwargs[key]
            variableD[key]['amplitude'] = kwargs[key]['max'] - kwargs[key]['min']
            variableD[key]['offset'] = kwargs[key]['min']

            # generate modulated stimulus datapoints
            # if function_to_mod in ['Mix']:
            # gasD=dict()
            # for key in variableD.keys():
            # gasD[variableD[key]['Gas_Name']]=
            # Mix(dictionary=None, total_flow=None, equilibration=False)
            #
            #
            # while time.time()<=totalepoch:
            # Mix({'H2': 5*ocil1[time.time()]}, {'O2': 5*ocil2[time.time()]})


# MED(cycles=4, shots_per_cycle=250, subframes=5, exp_time=1,ocilator='sin')
ocilator_gen('square', 10, 60, 0, 1)