'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

from xpd_architecture.userapi.Master_commands import *
from xpd_architecture.userapi.Util_commands import Mix
import matplotlib.pyplot as plt
import time
import numpy as np
import scipy.signal as signal


def ocilgen(ocilator, cycles=None, shots_per_cycle=None,subframes=None, exp_time=None, phase=0):


    totaltime=exp_time*subframes*shots_per_cycle*cycles
    t=np.linspace(0, 1, shots_per_cycle)
    periodt=2*np.pi*cycles*t
    if ocilator in ['sin', 'Sin']:
        ocil=(np.sin(periodt+phase)+1)/2
    elif ocilator in ['Triangle', 'tri']:
        ocil=abs(signal.sawtooth(periodt+phase))
    elif ocilator in ['saw']:
        ocil=(signal.sawtooth(periodt+phase)+1)/2
    elif ocilator in ['square']:
        ocil=(signal.square(periodt+phase)+1)/2
    plt.plot((t*totaltime/60**2), ocilgen)
    plt.ylim(-1.5, 1.5)
    plt.show()
    return ocil
def MED(cycles=None, shots_per_cycle=None, subframes=None, exp_time=None,
        function_to_mod=None,
        ocilator=None, **kwargs):

    totaltime=exp_time*subframes*shots_per_cycle*cycles
    print 'Experiment will take %s hours' % (totaltime/60.**2,)
    totalepoch=totaltime+time.time()

    #generate modulated stimulus datapoints
    if function_to_mod in ['Mix']:
        while time.time()<=totalepoch:
            Mix({'H2':5*ocilgen(ocilator, cycles, shots_per_cycle, subframes, exp_time, phase=0)}, {'O2':5*ocilgen(ocilator, cycles, shots_per_cycle, subframes, exp_time, phase=np.pi)})



MED(cycles=4, shots_per_cycle=250, subframes=5, exp_time=1,ocilator='sin')