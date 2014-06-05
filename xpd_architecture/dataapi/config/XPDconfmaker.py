# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:58:45 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

import ConfigParser
import time

config=ConfigParser.SafeConfigParser()
z='Info'
config.add_section(z)
config.set(z, 'version', '0.0.2')
config.set(z, 'Author', 'Chris Wright')
config.set(z, 'date of creation',(time.strftime("%m/%d/%Y")))
config.set(z,'comments', 'None yet')
z='PVs'
#z is the section name, the first entry is the alias, the second the PV name
config.add_section(z)
config.set(z, 'samx', 'test:motorx1')
config.set(z, 'samy', 'test:motorx2')
config.set(z, 'PhD', 'test:sensor1')
#more pvs

with open('XPD.conf', 'wb') as configfile:
    config.write(configfile)