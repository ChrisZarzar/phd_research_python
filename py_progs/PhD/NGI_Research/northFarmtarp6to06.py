#!/usr/bin/python

"""
Purpose: This script will go 
through a directory and will change any 
occasion where the 6% tarp is labled 
as "6" to "06"



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/17 22:04:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 17 October 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 17-Oct-2016



_______________________________________________________
"""

import os
import shutil
# Set local variables
shpDir = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\Micasense_Image_Extract\\"
for dirName, subdirList, fileList in os.walk(shpDir):
    for fname in fileList:
        if "_6%_" in fname:
            print "Changing file name %s" % (fname)
            fnameNew = fname.replace('_6%_', '_06%_')
            shutil.move(dirName+"\\"+fname, dirName+"\\"+fnameNew)
            
print "Program complete"
#End