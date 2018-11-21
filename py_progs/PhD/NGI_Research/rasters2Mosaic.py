#!/usr/bin/python

"""
Purpose: This script will walk through a directory of 
rasters and will sorth them into lists based on a certain
criteria. It will then create mosaics from the sorted lists 
of the files. 

____________________________________________
Author: Chris Zarzar
Created: 1 November 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 1-Nov-2016

EDITES: Chris Zarzar 10-Jan-2017. 
Had to comment some sections out and move around the August Rad mosaic creation 
because of troubles with storage space and now running simaltaneous instances
of the script. I just need to rearrange that radiance mosaic creation order
and to comment everything back in once the script finishes running. 
_______________________________________________________

EXAMPLES 
arcpy.MosaicToNewRaster_management inputs;inputs... output_location raster_dataset_name_with_extension ## {coordinate_system_for_the_raster} 8_BIT_UNSIGNED | 1_BIT | 2_BIT | 4_BIT ## | 8_BIT_SIGNED | 16_BIT_UNSIGNED | 16_BIT_SIGNED | 32_BIT_FLOAT | 32_BIT_UNSIGNED ## | 32_BIT_SIGNED | | 64_BIT {cellsize} number_of_bands {LAST | FIRST | BLEND | MEAN ## | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH} 
import arcpy 
arcpy.env.workspace = r"\\MyMachine\PrjWorkspace\RasGP" 
##Mosaic several TIFF images to a new TIFF image 
arcpy.MosaicToNewRaster_management("landsatb4a.tif;landsatb4b.tif","Mosaic2New", "landsat.tif", "World_Mercator.prj", "8_BIT_UNSIGNED", "40", "1", "LAST","FIRST")

arcpy.MosaicToNewRaster_management("land1.tif;land2.tif", "Mosaic2New", "landnew.tif", "", "8_BIT_UNSIGNED", "", "4", "BLEND","")


"""
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = False

print "Mosaic program begin"


# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped"
outDir = "G:\\zarzar_lpr_mosaics\\"
outList1 = []
outList2 = []
outList3 = []
outList4 = []
outList5 = []
#Spatial reference
spatialRef = arcpy.SpatialReference(102003) # 102003: USA_Contiguous_Albers_Equal_Area_Conic | 32618: WGS_1984_UTM_Zone_18N | 102387: NAD_1983_2011_UTM_Zone_18N
#Number of bands in the raster
bandNum = 4
#Method for merging overlapping rasters
mergeMethod = "BLEND"
#Raster output pixel depth
pixDepth = "32_BIT_FLOAT"
#Raster output cell size
cellSize = ""

#List the contents in the raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up loop
for f in fileList:
    if f.endswith('.tif'):
        if '2014-12' in f:
            outList1.append(f)
        elif '2015-3' in f:
            outList2.append(f)
        elif '2015-5' in f:
            outList3.append(f)
        elif '2015-8' in f:
            outList4.append(f)
        elif '2015-12' in f:
            outList5.append(f)
                               

outStr1 = ';'.join(outList1)
arcpy.MosaicToNewRaster_management(outStr1, outDir, "dec2014BV25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

#outStr2 = ';'.join(outList2)
#arcpy.MosaicToNewRaster_management(outStr2, outDir, "mar2015BV25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr3 = ';'.join(outList3)
arcpy.MosaicToNewRaster_management(outStr3, outDir, "may2015BV25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr4 = ';'.join(outList4)
arcpy.MosaicToNewRaster_management(outStr4, outDir, "aug2015BV25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr5 = ';'.join(outList5)
arcpy.MosaicToNewRaster_management(outStr5, outDir, "dec2015BV25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")


# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\temp_dntorad_move_back_when_done"
outDir = "G:\\zarzar_lpr_mosaics\\"
outList1 = []
outList2 = []
outList3 = []
outList4 = []
outList5 = []
#Spatial reference
spatialRef = arcpy.SpatialReference(102003) # 102003: USA_Contiguous_Albers_Equal_Area_Conic | 32618: WGS_1984_UTM_Zone_18N | 102387: NAD_1983_2011_UTM_Zone_18N
#Number of bands in the raster
bandNum = 3
#Method for merging overlapping rasters
mergeMethod = "BLEND"
#Raster output pixel depth
pixDepth = "32_BIT_FLOAT"
#Raster output cell size
cellSize = ""

#List the contents in the raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up loop
for f in fileList:
    if f.endswith('.tif'):
        if '2014-12' in f:
            outList1.append(f)
        elif '2015-3' in f:
            outList2.append(f)
        elif '2015-5' in f:
            outList3.append(f)
        elif '2015-8' in f:
            outList4.append(f)
        elif '2015-12' in f:
            outList5.append(f)
                           

outStr1 = ';'.join(outList1)
arcpy.MosaicToNewRaster_management(outStr1, outDir, "dec2014Rad25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr2 = ';'.join(outList2)
arcpy.MosaicToNewRaster_management(outStr2, outDir, "mar2015Rad25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr3 = ';'.join(outList3)
arcpy.MosaicToNewRaster_management(outStr3, outDir, "may2015Rad25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr5 = ';'.join(outList5)
arcpy.MosaicToNewRaster_management(outStr5, outDir, "dec2015Rad25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")         

outStr4 = ';'.join(outList4)
arcpy.MosaicToNewRaster_management(outStr4, outDir, "aug2015Rad25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")


# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\radtoref"
outDir = "G:\\zarzar_lpr_mosaics\\"
outList1 = []
outList2 = []
outList3 = []
outList4 = []
outList5 = []
#Spatial reference
spatialRef = arcpy.SpatialReference(102003) # 102003: USA_Contiguous_Albers_Equal_Area_Conic | 32618: WGS_1984_UTM_Zone_18N | 102387: NAD_1983_2011_UTM_Zone_18N
#Number of bands in the raster
bandNum = 3
#Method for merging overlapping rasters
mergeMethod = "BLEND"
#Raster output pixel depth
pixDepth = "32_BIT_FLOAT"
#Raster output cell size
cellSize = ""

#List the contents in the raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up loop
for f in fileList:
    if f.endswith('.tif'):
        if '2014-12' in f:
            outList1.append(f)
        elif '2015-3' in f:
            outList2.append(f)
        elif '2015-5' in f:
            outList3.append(f)
        elif '2015-8' in f:
            outList4.append(f)
        elif '2015-12' in f:
            outList5.append(f)
                           

outStr1 = ';'.join(outList1)
arcpy.MosaicToNewRaster_management(outStr1, outDir, "dec2014Ref25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr2 = ';'.join(outList2)
arcpy.MosaicToNewRaster_management(outStr2, outDir, "mar2015Ref25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr3 = ';'.join(outList3)
arcpy.MosaicToNewRaster_management(outStr3, outDir, "may2015Ref25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr4 = ';'.join(outList4)
arcpy.MosaicToNewRaster_management(outStr4, outDir, "aug2015Ref25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")

outStr5 = ';'.join(outList5)
arcpy.MosaicToNewRaster_management(outStr5, outDir, "dec2015Ref25.tif", spatialRef, pixDepth, cellSize, bandNum, mergeMethod,"")


print "COMPLETED SUCCESSFULLY. Dr. Dash, the external harddrive can be unplugged."

#END