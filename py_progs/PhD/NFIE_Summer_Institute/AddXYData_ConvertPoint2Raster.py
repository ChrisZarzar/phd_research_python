#!/usr/bin/python

"""
Purpose: This script adds XY data
from a CSV file and saves it as a shapefile.
The second portion of the script converts that
shapefile to a raster


"""

__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/06/20 19:15:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""

__________________________________________________
Author: Chris Zarzar
Created: 20 June 2016
Contact: chriszarzar@gmail.com

----History----

EDITED: Chris Zarzar 20-Jun-2016
Adjusted the script to specifically take iRIC
csv data and create a shapefile from that data. The script then takes
the new multipoint shapefile and creates a raster with 25 meter cells by
averaging all points that lie within each cell

EDITED: Chris Zarzar 22-Jun-2016
The creations of the csv2floodRaster.py script has made this script obsolete
______________________________________________________________________________

"""


#Setting up the script
import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True
#from glob import glob #Use if this script is converted to a loop

arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace ="F:\\NFIE_SI_2016\\groupProject\\iricOutput\\"

#output location of the shapefiles
outPathshp = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\shapefiles\\"

#output location of the Rasters
outPathras = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\"

#Path of your CSV Files
csvDir = "F:\\NFIE_SI_2016\\groupProject\\iricOutput\\"


#Set up the spatial refernce for the file
spatialRef = arcpy.SpatialReference(32618) # 32618 is code for WGS_1984_UTM_Zone_18N 102387 is code for NAD_1983_2011_UTM_Zone_18N

#List the files in the CSV directory
dirList = os.listdir(csvDir)

#List the files found in dirList with their full pathname
fileList = [csvDir+"\\"+filename for filename in dirList]

#Set up loop
for csvFile in fileList:
    if csvFile.endswith('.csv'):
        #Extract the .csv file name for naming purposes
        csvName = os.path.basename(csvFile[:-4])

        print "Creating shapefile from csv file: %s" % csvName

        #Name of the shapefile to create
        outFC = csvName+".shp"
        
        #Add the XY data
        arcpy.MakeXYEventLayer_management(csvFile, "X", "Y", "tempLay", spatialRef)

        #Convert the XY data layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion("tempLay", outPathshp, outFC)

        #Name of the water depth raster to create
        outRaswd= csvName+"_wd.tif"

        print "Creating %s water depth raster" % csvName 
        
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "Depth", outPathras+outRaswd, "MEAN", "", 25)
        
##        #Name of the water surface elevation raster to create
##        outRaswse = csvName+"_wse.tif"

##        print "Creating %s water surface elevation raster" % csvName 
##        
##        #Convert the newly created shapefile to a water surface elevation raster
##        arcpy.PointToRaster_conversion(outPathshp+outFC, "WaterSurfa", outPathras+outRaswse, "MEAN", "", 25)

        #Name of the water flow velocity raster to create
        outRaswfv = csvName+"_wfv.tif"

        print "Creating %s water flow velocity raster" % csvName 
        
        #Convert the newly created shapefile to a water flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "Velocity__", outPathras+outRaswfv, "MEAN", "", 25)

        print "Processing complete"

##END##
