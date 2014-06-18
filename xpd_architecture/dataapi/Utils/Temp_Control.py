'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

from xpd_architecture.dataapi.config._conf import *
from xpd_architecture.userapi._userconf import *
import time
import Decimal


if _userconf.has_section('Temperature System'):
    if _userconf.get('Temperature System', 'Control') in ['Euro', 'Eurotherm']:
        import eurotherm3500
        z='Eurotherm'
        heatcontroller = eurotherm3500.Eurotherm3500(_conf.get(z, 'Port'), _conf.get(z, 'Address'))
        deframp=float(_conf.get(z, 'DefRamp'))
        maxout=float(_conf.get(z,'Max%'))
        res=float(_conf.get(z, 'Res'))


        def temp_ramp(value=None):
            if value is not None:
                heatcontroller.set_sprate_loop1(value)
            return heatcontroller.get_sprate_loop1()


        def current_Temp():
            return heatcontroller.get_pv_loop1()


        def setT(value=None):
            if value is not None:
                heatcontroller.set_sp_loop1(value)
            return heatcontroller.get_sptarget_loop1()

        def res_check(value=None):
            if value is None:
                return float(_conf.get(z, 'Resolution'))
            else:
                return abs(Decimal(value).remainder_near(Decimal(_conf.get(z, 'Resolution'))))<1e-10


    if _userconf.get('Temperature System', 'Control') in ['Cryostream', 'stream', 'cryostream']:
        #stuff needs to go here about the cyrostream interface
        pass

def Temp_set(Start_Temp=None, Stop_Temp=None, Ramp=None, Time=None):
    """
    Sets one section of an overall temperature scheme, starts the section and blocks until complete.

    Parameters
    ----------
    Start_Temp: float
        The starting temperature to use,
            If this None use current temperature as starting temperature
            If this is not the current temperature go to the current temperature before starting run
    Stop_Temp: float
        The final temperature
    Ramp: float
        Ramp rate for the segment in C/min
            If this is None try to calculate ramp from stop and time
            If the calculation fails use default ramp
    Time: float
        Time for segment
            If this is none ramp until stop temperature is met


    Logical concerns
    ----------------
        Check that temperatures are in the instrument resolution
        Not all fields populated, which may be ok
        Potential combos:
                  Start, Stop: go to the start temperature, then got to the stop at default ramp rate
            Start, Stop, Ramp: go to the start temperature, go to the stop taking as much time as the ramp demands
            Start, Stop, Time: go to the start temperature, go to the stop ramp determined by math
            Start, Ramp, Time: go to start temperature, ramp temperature until time runs out

                  Stop, Ramp: from the current temperature go to the stop taking as much time as the ramp demands
                  Stop, Time: from the current temperature go to the stop ramp determined by math
                  Ramp, Time: from the current temperature ramp until the time limit is reached
            Stop, Ramp, Time: Stop, Ramp, check that the time works out:
    """
    for x in [Start_Temp, Stop_Temp]:
        if not res_check(x):
            print 'Temperature settings not in instrument resolution, resolution= %s' % (res_check(),)
    if Start_Temp is None:
        Start_Temp=current_Temp()
    else:
        Temp_set(current_Temp(), Start_Temp)

    if Ramp is None:
        try:
            internal_ramp=(Stop_Temp-Start_Temp)/(Time/60)
        except:
            internal_ramp=deframp

        Ramp=internal_ramp

    if Time is None:
        temp_ramp(Ramp)
        setT(Stop_Temp)
        while current_Temp() != Stop_Temp:
            print 'Heating/Cooling to %s C, currently at %s C' % (Stop_Temp, current_Temp(),)
            time.sleep(.1)
    else:
        starttime=time.time()
        temp_ramp(Ramp)
        setT(Stop_Temp)
        while time.time()<=starttime+Time:
            print 'Heating/Cooling to %s C, currently at %s C' % (Stop_Temp, current_Temp(),)
            time.sleep(.1)