#!/usr/bin/python

"""
Purpose: This script will project the raster and
in doing so it is set up to also resample
the rasters
"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/08/31 14:55:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
_______________________________________
Author: Chris Zarzar
Created: 08-31-2016
Contact: chriszarzar@gmail.com


----History----

CREATED: Chris Zarzar 31-Aug-16

EDITED: Chris Zarzar 16-Sep-16
Modified the paths of the script so that it 
wil resample all that has been moved onto the
new harddrive install on my computer. 

EDITED: Chris Zarzar 29-Sep-16
Added try statement so that overwrite option
can be used. 
____________________________________________


"""
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = False

# Set environment settings
#env.workspace = "K:\\general\\cmzarzar\\CIR_UAS_Imagery\\Original_CIR_Images\\"
env.workspace = "E:\\CIR_UAS_Imagery\\Original_Clipped\\"

#Set the location of the raster data
#rasDir = "K:\\general\\cmzarzar\\CIR_UAS_Imagery\\Original_CIR_Images\\"
rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\"

# Set the output location of the resampled and reprojected raster data
#outDir = "K:\\general\\cmzarzar\\CIR_UAS_Imagery\\resampledImagery\\"
outDir = "E:\\CIR_UAS_Imagery\\resampledCIR_05\\"

# Set up variables for the resampling#

#Interpolation method
interpolation = "CUBIC"   # Options include NEAREST | BILINEAR | CUBIC | MAJORITY

#Spatial reference
spatialRef = arcpy.SpatialReference(102003) # 102003: USA_Contiguous_Albers_Equal_Area_Conic | 32618: WGS_1984_UTM_Zone_18N | 102387: NAD_1983_2011_UTM_Zone_18N

#Cell size (meters)
cellSize = "0.25"

#Geographic Transformation (Required if going from WGS 1984 to NAD 1983
geoTrans = "WGS_1984_(ITRF00)_To_NAD_1983"

#List the documents in that raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

for fname in fileList:
    if fname.endswith('.tif'):
        try: 
            print "Resampling raster %s" %(os.path.basename(fname[:-4]))
            arcpy.ProjectRaster_management(fname, outDir+os.path.basename(fname[:-4])+"_Albers.tif",\
                                       spatialRef, interpolation, cellSize,\
                                       geoTrans)                                     
        except:        
            if "ERROR 000725" in arcpy.GetMessages(2):
                print "%s exists and overwrite turned off." %(os.path.basename(fname))
            else: 
                arcpy.GetMessages(1)                
                arcpy.GetMessages(2)

print "Program complete"
####END
        
# Walk through all directories and subdirectories
#for dirName, subdirList, fileList in os.walk(rasDir):
#    print dirName
#    print subdirList
#    print fileList