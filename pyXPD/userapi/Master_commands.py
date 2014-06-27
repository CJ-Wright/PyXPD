# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:00:35 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright

This is the master module for the userapi, it loads all the other userapis which should be loaded at the begining of a \
control ipython session
"""
from pyXPD.userapi import *
import cothread
from cothread.catools import *
from pyXPD.instrumentapi.config._conf import _conf, __initPV
import inspect

def printf(value):
#    print value, test function
    return value


def helper(func, options='args'):
    """
    Function reveals information about other functions

    Parameters
    ----------
    func: function
        Function to learn more about
    options: {'args', 'default'}
        If args give the argument names
        If defualt give the default values
        Else return the doc string


    """
    answer=inspect.getargspec(func)
    if options=='args':
        print answer[0]
    elif options=='default':
        print answer[-1]
    else:
        print func.__doc__


if __name__ == "__main__":
    print 'Welcome to the pyXPD control system'