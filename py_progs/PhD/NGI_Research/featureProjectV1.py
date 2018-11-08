# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Chance the projection of
a directory of polygons

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
polyDir = "E:\\NGI_UAS\\GIS\\FlightBoundaryPolygons\\"

#Spatial reference
spatialRef = arcpy.SpatialReference(4326) # 4326: GCS_WGS_1984 | 102003: USA_Contiguous_Albers_Equal_Area_Conic | 32618: WGS_1984_UTM_Zone_18N | 102387: NAD_1983_2011_UTM_Zone_18N

#Geographic Transformation (Required if going from WGS 1984 to NAD 1983
geoTrans = "WGS_1984_(ITRF00)_To_NAD_1983"

# Whether extra vertices will be added to preserve the feature shape
preserveShape = "PRESERVE_SHAPE"

#List the documents in that raster directory
dirList = os.listdir(polyDir)

#List the files found in dirList with their full pathname
fileList = [polyDir+"\\"+filename for filename in dirList]
for fname in fileList:
    if fname.endswith('.shp'):
        inPoly = fname     
        outPoly = inPoly[:-17]+"WGS.shp"

        # Project the polygons
        arcpy.Project_management(inPoly, outPoly, spatialRef, geoTrans,"",preserveShape,"")









