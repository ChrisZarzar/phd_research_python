#!/usr/bin/python

"""
Purpose: This script will run a majority filter on all 
classication output to clean up the salt and pepper look 
of the per-pixel classification

Majority Filter Description: Replaces cells in a raster based on the 
majority of their contiguous neighboring cells.


"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2017/03/13 11:17:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 13 March 2017
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 03-Mar-2017

EDIT: Chris Zarzar 03-Mar-2017: Discovered that the raster was float and 
the majority filter needs an integer raster. I reclassified the data first
to account for this and convert to integers. 

_______________________________________________________


"""


# Import system modules
import os
import arcpy as ap
from arcpy import env
from arcpy.sa import *

## Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
    

dirList = ['aug2015'] #, 'mar2015', 'may2015', 'dec2014', 'dec2015'] Add other dates once that data processes. 

for d in dirList:
    print "Filtering %s classifications" %(d)
    
    ## Set environment settings
    env.workspace = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\RWorkspace\\lpr\\lpr_classification_output\\%s\\outRasters\\" %(d)
    
    ## Check if postprocessing output directory exists and create it if it does not already exists
    if not os.path.exists(env.workspace+"\\postProcessed_Rasters"):
        os.makedirs(env.workspace+"\\postProcessed_Rasters")
        
    ## List all GeoTIFF rasters in current environment workspace to loop through     
    fileList = ap.ListFiles("*.tif")
    for f in fileList: 
        
        ## Extract the name of the file without the extension 
        rasName = os.path.basename(f[:-4])
        
        ## Set local variables
        inRaster = f
        
        print "Converting %s values to integers" % (f)
        ## Reclassify raster to convert it to an integer while keeping the classification integrity 
        outReclass = Reclassify(f, "Value", RemapRange([[0,1.5,1],[1.5,2.5,2],[2.5,3.5,3]]), "NODATA")
        
        ## Save the output
        outReclass.save(env.workspace+"\\postProcessed_Rasters\\"+rasName+"_reclass.tif")
        
        print "Applying Majority Filter"
        ## Execute MajorityFilter
        outMajFilt = MajorityFilter(outReclass, "EIGHT", "MAJORITY")
        
        ## Save the output 
        outMajFilt.save(env.workspace+"\\postProcessed_Rasters\\"+rasName+"_majfilter.tif")
        
    
    
    
print "program complete"

## End