# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Take a directory of polygons and 
clip raster images from the LPR
missions. 

Required Modules:
arcpy (with spatial extension)
os


"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/04 19:21:00 $"[7:-2]
__author__ = "Chris Zarzar <chris.zarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 04 October 2016
Contact: chris.zarzar@gmail.com

----History----

CREATED: Chris Zarzar 04-Oct-2016

_______________________________________________________

"""
# Import modules
import arcpy
import os


# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = False

# Set up local variables
polyDir = "I:\\NGI_UAS\\GIS\\FlightBoundaryPolygons\\wgs1984\\"
rasDir = "E:\\CIR_UAS_Imagery\\Original_CIR_Images\\"
outDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\"


#List the documents in that raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
count = 0
for dirName, subdirList, fileList in os.walk(rasDir):
    for fname in fileList:
        if fname.endswith(".tif"):
            for dirName2, subdirList2, fileList2 in os.walk(polyDir):
                for fname2 in fileList2:
                    if fname2.endswith(".shp"):
                        imgName = fname[:-4]
                        shpName = fname2[:-8]
                        if imgName == shpName:
                            print " Clipping %s" %(imgName)
                            arcpy.Clip_management (dirName+fname, "", outDir+imgName+".tif", dirName2+fname2, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        count += 1
#END










