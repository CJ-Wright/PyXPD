__author__ = 'arkilic'
import cothread
from cothread.catools import *
from dataapi.config._conf import _conf
import numpy as np
from decimal import *

getcontext().prec=8
#read configuration file motor section
def initmotors(_conf):
    print 'Connecitng motors'
    try:
        for option in _conf.options('PVs'):
            if 'motor' in str(_conf.get('PVs',option)):
                connect(_conf.get('PVs',option))
        print 'Motor initialization complete'
    except:
        raise Exception('Some of the motors were not found or could not connect\
        , namely:\n %s, pv=%s'% (option,_conf.get('PVs',option)))
initmotors(_conf)

motorD=dict()
for option in _conf.options('PVs'):
    if 'motor' in str(_conf.get('PVs',option)):
        pv=_conf.get('PVs',option)
        motorD[option]={'pv':pv,'low':caget(pv+'.LLM'),'high':caget(pv+'.HLM'),'EGU':caget(pv+'.EGU'),'res':caget(pv+'.MRES')}

def trans(alias):
    return _conf.get('PVs',alias)
    
def move(alias,value,wait=False, printop=False):
    #check final position within limits
    motor=motorD[alias]
    if motor['low']<= value <=motor['high']:
        #check is move is within motor resolution,
        if abs(Decimal(value).remainder_near(Decimal(motor['res'])))<1e-10:
            caput(motor['pv'],value,wait=wait, timeout=None)
        else:
            raise Exception('Move specified with more precision than instrument allows')
    else:
        raise Exception('Out of Bounds, the soft limit has been reached')
    

def position(alias, **kwargs):
    if kwargs=={}:
        motor=motorD[alias]
        pos=caget(motor['pv']+'.DRBV') 
        return float(pos)
        #other posibilities
def resolution(**kwargs):
    if kwargs=={}:
        print('Current resolutions for the motors are:\n')
        for element in motorD:
            print 'Motor: %s, Resolution: %s' % (element, element['res'])
    else:
        for key in kwargs.keys():
            print motorD[key]['res']
            
            
        