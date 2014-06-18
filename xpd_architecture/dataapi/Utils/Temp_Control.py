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
    Logical concerns:
        Check that temperatures are in the instrument resolution
        Not all fields populated, which may be ok
        Potential combos
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
            internal_ramp=(Stop_Temp-Start_Temp)/(Time)
        except:
            internal_ramp=deframp

        Ramp=internal_ramp

    if Time is None:
        temp_ramp(Ramp)
        setT(Stop_Temp)
        while current_Temp() != Stop_Temp:
            print 'Heating/Cooling to %s C, currently at %s C' % (Stop_Temp, current_Temp(),)
            time.sleep(.1)













    if Start_Temp is None:
        Start_Temp=current_Temp()
    internal_ramp=(Stop_Temp-Start_Temp)/(Time)
    if Ramp is None:
        Ramp=internal_ramp
    if internal_ramp != Ramp:
        print 'The set ramp rate does not match the internal ramp rate, using internal ramp rate'
        Ramp=internal_ramp
    if current_Temp() != Start_Temp:
        print 'Not at starting temperature, moving to start temperature before program start'
        Temp_set(current_Temp(), Start_Temp, Ramp=deframp)

    #core
    temp_ramp(Ramp)
    set(Stop_Temp)
    while current_Temp() != Stop_Temp:
        sleep(.1)
