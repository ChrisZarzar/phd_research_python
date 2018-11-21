#!/usr/bin/python

"""
Purpose: This script reads through
all folders in a directory and
assigns spatial reference information
to the files in the directory.



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/07/06 12:55:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 06 July 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 06-Jul-2016

EDITED: Chris Zarzar 10-Oct-2016
Added the ability to recursively work through a directory

_______________________________________________________

"""
#Set up import variables
import arcpy as ap
import os
from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

spatialRef = arcpy.SpatialReference(3857) # 3857 is for Web Mercator ;; 4269 is for GCS NAD 1983 ;; 4326 is code for GCS WGS 1984


#Path to directories
imgDir= "E:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\micasenseOrganized\\"

try:
#Loop through each directory and do operations on files in each directory
    for dirName, subdirList, fileList in os.walk(imgDir):
        imgList = [dirName+"\\"+filename for filename in fileList if filename.endswith(".tif")]
        for img in imgList:
            imgName = os.path.basename(img[:-4])
            ap.DefineProjection_management(img, spatialRef)
            desc = ap.Describe(img)
            imgSpatRef = desc.spatialReference
            print imgSpatRef  
        # print messages when the tool runs successfully
        print(arcpy.GetMessages(0))
    
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    
except Exception as ex:
    print(ex.args[0])

if imgSpatRef in locals() or globals():
    print "Processing Complete"
else:
    print "Error in processing"


##END##
