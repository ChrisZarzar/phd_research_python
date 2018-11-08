# -*- coding: utf-8 -*-
"""
Purpose: This script will convert the FaSTMECH 
conditional rasters I created, will convert those 
back to shapefiles, interpolate those shapefiles, 
and will finally convert that back into rasters for 
use in the raster composite portion of the script



"""

__version__ = "$Revision: 2.4 $"[11:-2]
__date__ = "$Date: 2016/07/6 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 28 February 2017
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 28-Feb-2017



____________________________________________
"""

import os
import arcpy
from arcpy import env  
from arcpy.sa import *

#Setup environment setting
#env.workspace = "C:\\Users\\chris\\Desktop\\Research\\NFIE_JWRPA_Data\\workspace\\"
env.workspace = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\workspace\\"

#Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\"

#Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True

## Set file directories

## Input rasters
rasDir = path+"\\postprocessOutput\\rasters\\usgs_ensembles\\"

## Temp output shapefile location
shpOut = env.workspace

## Output raster location
rasOut = path+"\\postprocessOutput\\rasters\\usgs_ensembles_idw\\"

## Set up loop through raster directory

## List the files in the shapefile to raster directory
rasList = os.listdir(rasDir)

## List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in rasList]

for inRas in fileList:
    if inRas.endswith('.tif'):
        ## Extract file name
        rasName = os.path.basename(inRas[:-4])
        print "Processing raster: " + rasName
        ## Convert rasters to point shapefiles 
        shpName = shpOut+rasName+".shp"
        arcpy.RasterToPoint_conversion(inRas, shpName, "VALUE") 
        
        ## Set up IDW interpolation
        ## Set local variables
        inPointFeatures = shpName
        zField = "GRID_CODE"
        cellSize = 5
        power = 2
        searchRadius = RadiusVariable(1, 5) ## (Num Points, Max Dist)
        
        # Execute IDW
        outIDW = Idw(inPointFeatures, zField, cellSize, power, searchRadius)
        
        # Save the output 
        outIDW.save(rasOut+rasName+"_idw.tif")
        
        
        
        
##  END  ##
