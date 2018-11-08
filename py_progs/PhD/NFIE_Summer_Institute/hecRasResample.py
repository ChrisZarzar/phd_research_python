# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 22:28:17 2017

@author: chris
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 21:51:33 2017

@author: chris
"""

#!/usr/bin/python

"""
Purpose: Michael no longer generated the HECRAS data on a 5x5 
grid, so I need to use a nearest neighbor resampling technique to fix the data. 


"""

__version__ = "$Revision: 2.4 $"[11:-2]
__date__ = "$Date: 2017/10/10 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 10 October 2017
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 10-Oct-2017

_______________________________________________________

"""
#Setting up the script
import os
import arcpy
import shutil
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap
arcpy.env.overwriteOutput = True

##Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\"

##Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

##Setup environment setting
env.workspace = path+"workspace\\"

##Input locaiton for original HEC-RAS rasters
hecRasdir = path+"modelOutput\\hecrasOutput\\"


print "Beginning script processing"

#Set up look to postprocess HEC-RAS output
for dirName, subdirList, fileList2 in os.walk(hecRasdir):
    for hecRas in fileList2:
        if hecRas.endswith('.tif'):
            hecName = "resamp_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            arcpy.Resample_management(outPath+hecRas, outPath+hecName, "5", "NEAREST")

