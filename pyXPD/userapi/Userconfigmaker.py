# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:58:45 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

import ConfigParser
import time


config = ConfigParser.SafeConfigParser()
config.optionxform = str

z = 'Info'
config.add_section(z)
config.set(z, 'version', '0.0.2')
config.set(z, 'Author', 'Christopher J. Wright')
config.set(z, 'date of creation', (time.strftime("%m/%d/%Y")))
config.set(z, 'comments', 'None yet')

# Gas Assignment Convention, VALVENAME,POSITION on VALVENAME
z = 'Example User Gas Assignments'
config.add_section(z)
config.set(z, 'F2', 'Valve_1:0')
config.set(z, 'FOOF', 'Valve_1:2')
config.set(z, 'SUPER AWESOME GAS', 'Valve_2:2')

z = 'Temperature System'
config.add_section(z)
config.set(z, 'Control', 'Eurotherm')
config.set(z, 'Heater/Cooler', 'Resistive')

with open('user.conf', 'wb') as configfile:
    config.write(configfile)
    print 'write complete'