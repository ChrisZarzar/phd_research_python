#!/usr/bin/python

"""
Purpose: This script will provide projection
information to the exported PNGs



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/29 08:34:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 29 June 2016
Contact: chriszarzar@gmail.com



----History----

CREATED: Chris Zarzar 29-Jun-2016
_______________________________________________________
"""

#Set up the script
import arcpy as ap
import os
from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Set up variables
env.workspace = "F:\\NFIE_SI_2016\\groupProject\\"
pngDir = "F:\\NFIE_SI_2016\\groupProject\\ArcMap_Images\\"

# Set up the spatial reference information
spatialRef = arcpy.SpatialReference(3857) # 3857 is code for WGS_1984_Web_Mecator (auxiliary 

# Set up png list
dirList = os.listdir(pngDir)

# List the files found in dirList with their full pathname
pngList = [pngDir+filename for filename in dirList if filename.endswith(".png")]


try:
    # Set up loop adding spatial reference info to PNGs
    for png in pngList:
        pngName = os.path.basename(png[:-4])
        if "Per" in pngName:
            ap.DefineProjection_management(png, spatialRef)
            desc = ap.Describe(png)
            pngSpatRef = desc.spatialReference
            print pngSpatRef
            
    # print messages when the tool runs successfully
    print(arcpy.GetMessages(0))
    
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    
except Exception as ex:
    print(ex.args[0])

if pngSpatRef in locals() or globals():
    print "Processing Complete"
else:
    print "Error in processing"


##END##
