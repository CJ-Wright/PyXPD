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
config.optionxform=str

z='Info'
config.add_section(z)
config.set(z, 'version', '0.0.2')
config.set(z, 'Author', 'Chris Wright')
config.set(z, 'date of creation',(time.strftime("%m/%d/%Y")))
config.set(z,'comments', 'None yet')
z='Motor PVs'
#z is the section name, the first entry is the alias, the second the PV name
config.add_section(z)
config.set(z, 'samx', 'test:motorx1')
config.set(z, 'samy', 'test:motorx2')

z='Count PVs'
config.add_section(z)

config.set(z, 'PhotoD', 'test:sensor1')

#DETECTOR PVS
d='13SIM1:'
z='Detector PVs'
config.add_section(z)
#Detector controls
s='cam1:'
config.set(z,'Callabacks',d+s+'ArrayCallbacks')
config.set(z, 'Status', d+s+'DetectorState_RBV')
config.set(z, 'Aq', d+s+'Acquire')
#Detector Parameters
config.set(z,'Manufacturer',d+s+'Manufacturer_RBV')
config.set(z,'DetTemp',d+s+'Temperature_RBV')
config.set(z,'ImageMode',d+s+'ImageMode') #
config.set(z,'TriggerMode',d+s+'TriggerMode')
#PE Specific
config.set(z, 'NumExp', d+s+'NumExposures')
config.set(z, 'NumExpRBV', d+s+'NumExposures_RBV')
config.set(z, 'NumImages',d+s+'NumImages')
config.set(z, 'NumImagesRBV',d+s+'NumImages_RBV')
config.set(z, 'AcquireTime', d+s+'AcquireTime')
config.set(z, 'AcquireTimeRBV',d+s+'AcquireTime_RBV')

#Image handeling
s='TIFF1:'
config.set(z, 'AutoS', d+s+'AutoSave')
config.set(z,'AutoSRBV',d+s+'AutoSave_RBV')
config.set(z,'Format',d+s+'FileFormat')
config.set(z,'FormatRBV',d+s+'FileFormat_RBV')
config.set(z,'Capture',d+s+'Capture')
config.set(z,'CaptureNum',d+s+'NumCapture')
config.set(z,'AutoI', d+s+'AutoIncrement')
config.set(z,'AutoIRBV',d+s+'AutoIncrement_RBV')
config.set(z, 'File_Temp', d+s+'FileTemplate')
config.set(z,'FullName',d+s+'FullFileName_RBV')
config.set(z, 'FileNum', d+s+'FileNumber')

z='PE PVs'
s='cam1:'
config.add_section(z)
#PE offset
config.set(z, 'NumOffset',d+s+'PENumOffsetFrames')
config.set(z, 'OffsetFrame',d+s+'PECurrentOffsetFrame')
config.set(z, 'AqOff', d+s+'PEAcquireOffset')
config.set(z, 'UseOff', d+s+'PEUseOffset')
config.set(z, 'OffAvail', d+s+'PEOffsetAvailable')
#PE Gain
config.set(z, 'NumGain',d+s+'PENumGainFrames')
config.set(z, 'GainFrame',d+s+'PECurrentGainFrame')
config.set(z, 'AqGain', d+s+'PEAcquireGain')
config.set(z, 'UseGain', d+s+'PEUseGain')
config.set(z, 'GainAvail', d+s+'PEGainAvailable')
#PE Bad Pixel
config.set(z, 'UsePixel', d+s+'PEUsePixelCorrection')
config.set(z, 'PixelAvail', d+s+'PEPixelCorrectionAvailable')
config.set(z, 'PixelFile', d+s+'PEBadPixelFile')
#Load corrections
config.set(z, 'PixelFileRBV', d+s+'PEBadPixelFile_RBV')
config.set(z, 'CorrDir', d+s+'PECorrectionsDir')
config.set(z, 'LoadCorr', d+s+'PELoadCorrections')
config.set(z, 'SaveCorr', d+s+'PESaveCorrections')

#Correction files
z='PE files'
config.add_section(z)

z='Single Default'
config.add_section(z)


with open('XPD.conf', 'wb') as configfile:
    config.write(configfile)
    print 'write complete'