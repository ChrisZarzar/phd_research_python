#!/usr/bin/python

"""
Purpose: This script takes a csv file
generated from each iRIC ensemble and
it will read through the rows to create
new csv files that will be used to convert
to raster and used to create the final
images


"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/22 10:43:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 20 June 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 22-Jun-2016
Created script and set up to take the output iRIC csv
and edit the columns based on certain threshold requirements


**EDITED: Chris Zarzar 22-Jun-2016
***The creation of the csv2floodRaster.py script has made this script obsolete***
_______________________________________________________

"""


#Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace ="F:\\NFIE_SI_2016\\groupProject\\iricOutput\\"

#output location of the shapefiles
outPathshp = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\shapefiles\\"

#Path of your CSV Files
csvDir = "F:\\NFIE_SI_2016\\groupProject\\iricOutput\\"

#Name of the shapefile to create
outFC = csvName+".shp"

#Add the XY data
arcpy.MakeXYEventLayer_management(csvFile, "X", "Y", "tempLay", spatialRef)

#Convert the XY data layer to a shapefile
arcpy.FeatureClassToFeatureClass_conversion("tempLay", outPathshp, outFC)


#Add fields I will need to the shapefile attribute table
arcpy.AddField_management(outPathshp+outFC,"fldext", "TEXT")
arcpy.AddField_management(outPathshp+outFC,"wd_2ft", "TEXT")
arcpy.AddField_management(outPathshp+outFC,"fv_7mph", "TEXT")
arcpy.AddField_management(outPathshp+outFC,"crit_2_7", "TEXT")
upCur = arcpy.UpdateCursor(outPathshp+outFC)
for row in upCur:
    if (row.Depth > 0): row.fldext = 1
    else: row.fldext = 0
    if (row.Depth >= 2): row.wd_2ft = 1
    else: row.wd_2ft = 0
    if (row.Velocity__ >=7): row.fv_7mph = 1
    else: row.fv_7mph = 0
    if (row.Depth >= 2 and row.Velocity__ >=7): row.crit_2_7 = 1
    else: row.crit_2_7 = 0
    upCur.updateRow(row)
del upCur, row

    
print "Processing complete"


##END##
