'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

from xpd_architecture.dataapi.Utils.Gas_Valve import *
from xpd_architecture.dataapi.Utils.Counts import *
from xpd_architecture.dataapi.Utils.Temp_Control import *
from xpd_architecture.dataapi.Utils.Flow_Control import *
import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf
import time
from collections import OrderedDict

def Gas(new_gas=None):
    """
    Returns the current gas name, or sets the new gas
    :param new_gas: New Gas name
    :type new_gas: str
    :return: Gas name
    :rtype: str
    """
    if new_gas is None:
        cur_pos=gas_position()
        # print cur_pos
        # print valve_asg
        for key, valvepos in valve_asg.iteritems():
            # print 'key', key
            # print 'valvedict', valvepos
            # print 'curpos', cur_pos
            # print valvepos['Valve'], cur_pos[0], valvepos['Pos'], cur_pos[1]
            # print valvepos['Valve']==cur_pos[0], valvepos['Pos']==str(cur_pos[1])
            if valvepos['Valve']==cur_pos[0] and valvepos['Pos']==int(cur_pos[1]):
                # print key
                return key
    elif valve_asg.has_key(new_gas):
        # print valve_asg[new_gas]
        gas_position(**valve_asg[new_gas])
        return Gas()
    else:
        print '%s is not a recognised gas, please change gas configuration.' % (new_gas,)


def TempProg(orderedD=None):
    """
    Sets and starts the temperature program
    Parameters
    ----------
    orderedD: ordered dictionary
        This dictionary contains the segements of the program in order.  Each sub-directory is a new segment
        i.e. {0:{Start:25, Stop:75, Time: 20},1:{Start:75, Stop:350, Ramp: 35}}
    Subparameters
    -------------
    Start: float, optional
        Starting temperature of segment
    Stop: float
        Ending temperature of segment
    Ramp: float, optional
        the rate of temperature change
    Time: float, optional
        Duration of program segment
    """
    #Expecting entries to contain Start Temp, Stop Temp, Ramp Rate,and Time for each segment
    for key in orderedD.keys():
        Temp_set(**orderedD[key])

def Mix(dictionary=None, total_flow=None, equilibrate=False):
    """
    Mixes gases together for use in flow cell

    Parameters
    ----------
    dictionary: dictionary
        This contains the information of about the gases ie. dictionary={H2:5,O2:10}
        The values are either in flow units or in percent if total_flow is used
    total_flow: float
        If total_flow is used the values in the dictionary are interpreted as percents of the total flow
    equilibrate: bool
        If equilibrate is true the program will wait a max of 45 seconds for the input gas flow to equal the exhaust flow
    """
    #absolute flow control
    if total_flow is None:
        total=0
        for key in dictionary.keys():
            Gas(key)
            Flow(key, dictionary[key])
            total+=dictionary[key]
    #relative flow control
    else:
        for key in dictionary.keys():
            Gas(key)
            Flow(key, dictionary[key]*total_flow)
        total=total_flow
    #wait for equilibration
    if equilibrate==True:
        for i in range(0,15):
            if Flow('EX')==total:
                break
            else:
                print "Pressure not equalized, waiting 3 seconds"
                time.sleep(3)
                i+=1


def Flow(Gas_Name=None, Value=None):
    if Gas_Name is None:
        for option in _conf.options('Flow Meter PVs'):
            print 'Flow at Meter %s is %s' % (option, get_flow(option), )
    elif Value is None:
        print 'Flow for %s is %s' % (Gas_Name, get_flow(flowname_from_gas(Gas_Name))) # need to get flow from gas name
    else:
        #Find flow meter associated with Gas
        set_flow(flowname_from_gas(Gas_Name),Value)
