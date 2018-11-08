#!/usr/bin/python

"""
Purpose: This script takes a csv file
generated from each iRIC ensemble and
it will read through the rows to create
new csv files that will be used to convert
to raster and used to create the final
images


"""

__version__ = "$Revision: 2.0 $"[11:-2]
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


EDITED: Chris Zarzar 23-Jun-2016
Added in new depths, flow velocities, and critical thresholds
Also decreased raster size to 10 meters for more detail
_______________________________________________________

"""


#Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace ="F:\\NFIE_SI_2016\\groupProject\\"

#output location of the shapefiles
outPathshp = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\shapefiles\\"

#output location of the Rasters
outPathras = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\ensembles\\"

#Path of your CSV Files 
csvDir = "F:\\NFIE_SI_2016\\groupProject\\iricOutput\\"

#Set up the spatial refernce for the file
spatialRef = arcpy.SpatialReference(32618) # 32618 is code for WGS_1984_UTM_Zone_18N 102387 is code for NAD_1983_2011_UTM_Zone_18N

#List the files in the CSV directory
dirList = os.listdir(csvDir)

#List the files found in dirList with their full pathname
fileList = [csvDir+"\\"+filename for filename in dirList]

"""---CREATE SHAPEFILE---"""

#Set up loop
for csvFile in fileList:
    if csvFile.endswith('.csv'):
        #Extract the .csv file name for naming purposes
        csvName = os.path.basename(csvFile[:-4])

        #Name of the shapefile to create
        outFC = csvName+".shp"

        print "Creating shapefile from csv file: %s" % csvName

        #Add the XY data
        arcpy.MakeXYEventLayer_management(csvFile, "X", "Y", "tempLay", spatialRef)

        #Convert the XY data layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion("tempLay", outPathshp, outFC)

        #Add fields I will need to the shapefile attribute table
        arcpy.AddField_management(outPathshp+outFC,"fldext", "TEXT")
        
        arcpy.AddField_management(outPathshp+outFC,"wd_hlfft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_1ft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_2ft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_3ft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_4ft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_5ft", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"wd_6ft", "TEXT")
        
        arcpy.AddField_management(outPathshp+outFC,"fv_1mph", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"fv_2mph", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"fv_4mph", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"fv_6mph", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"fv_8mph", "TEXT")
        
        arcpy.AddField_management(outPathshp+outFC,"crit_hlf_4", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_1_4", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_2_4", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_hlf_6", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_1_6", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_2_6", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_3_2", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_4_2", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_5_1", "TEXT")
        arcpy.AddField_management(outPathshp+outFC,"crit_6_1", "TEXT")

        upCur = arcpy.UpdateCursor(outPathshp+outFC)
        
        #values of output are in SI units. So these values used in
        #conditional statements below will now match the imperial
        #units in the header name
        for row in upCur:
            if (row.Depth > 0): row.fldext = 1
            else: row.fldext = 0
            
            if (row.Depth >= .15): row.wd_hlfft = 1
            else: row.wd_hlfft = 0
            if (row.Depth >= .305): row.wd_1ft = 1
            else: row.wd_1ft = 0
            if (row.Depth >= .61): row.wd_2ft = 1
            else: row.wd_2ft = 0
            if (row.Depth >= .91): row.wd_3ft = 1
            else: row.wd_3ft = 0
            if (row.Depth >= 1.22): row.wd_4ft = 1
            else: row.wd_4ft = 0
            if (row.Depth >= 1.5): row.wd_5ft = 1
            else: row.wd_5ft = 0
            if (row.Depth >= 1.83): row.wd_6ft = 1
            else: row.wd_6ft = 0
            
            if (row.Velocity__ >=.45): row.fv_1mph = 1
            else: row.fv_1mph = 0
            if (row.Velocity__ >=.89): row.fv_2mph = 1
            else: row.fv_2mph = 0
            if (row.Velocity__ >=1.79): row.fv_4mph = 1
            else: row.fv_4mph = 0
            if (row.Velocity__ >=2.68): row.fv_6mph = 1
            else: row.fv_6mph = 0
            if (row.Velocity__ >=3.58): row.fv_8mph = 1
            else: row.fv_8mph = 0


            if (row.Depth >=.15 and row.Velocity__ >=1.79): row.crit_hlf_4 = 1
            else: row.crit_hlf_4 = 0
            if (row.Depth >=.305 and row.Velocity__ >=1.79): row.crit_1_4 = 1
            else: row.crit_1_4 = 0
            if (row.Depth >=.61 and row.Velocity__ >=1.79): row.crit_2_4 = 1
            else: row.crit_2_4 = 0
            if (row.Depth >=.15 and row.Velocity__ >=2.68): row.crit_hlf_6 = 1
            else: row.crit_hlf_6 = 0
            if (row.Depth >=.305 and row.Velocity__ >=2.68): row.crit_1_6 = 1
            else: row.crit_1_6 = 0
            if (row.Depth >=.61 and row.Velocity__ >=2.68): row.crit_2_6 = 1
            else: row.crit_2_6 = 0
            if (row.Depth >=.91 and row.Velocity__ >=.89): row.crit_3_2 = 1
            else: row.crit_3_2 = 0
            if (row.Depth >=1.22 and row.Velocity__ >=.89): row.crit_4_2 = 1
            else: row.crit_4_2 = 0
            if (row.Depth >= 1.5 and row.Velocity__ >=.45): row.crit_5_1 = 1
            else: row.crit_5_1 = 0
            if (row.Depth >= 1.83 and row.Velocity__ >=.45): row.crit_6_1 = 1
            else: row.crit_6_1 = 0
            
            upCur.updateRow(row)
        del upCur, row
        arcpy.Delete_management("tempLay", 'GPFeatureLayer')
        
        """----CREATE RASTERS FROM SHAPEFILE----"""
        
        #Name of the flood extent raster to create
        outRasfldext= csvName+"_fldext.tif"

        print "Creating %s flood extent raster" % csvName

        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fldext", outPathras+outRasfldext, "MOST_FREQUENT", "", 10)



        #Name of the .5 foot water depth raster to create
        outRaswd= csvName+"_wd_hlfft.tif"
        print "Creating %s 1/2 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_hlfft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 1 foot water depth raster to create
        outRaswd= csvName+"_wd_1ft.tif"
        print "Creating %s 1 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_1ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 2 foot water depth raster to create
        outRaswd= csvName+"_wd_2ft.tif"
        print "Creating %s 2 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_2ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 3 foot water depth raster to create
        outRaswd= csvName+"_wd_3ft.tif"
        print "Creating %s 3 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_3ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 4 foot water depth raster to create
        outRaswd= csvName+"_wd_4ft.tif"
        print "Creating %s 4 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_4ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 5 foot water depth raster to create
        outRaswd= csvName+"_wd_5ft.tif"
        print "Creating %s 5 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_5ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)

        #Name of the 6 foot water depth raster to create
        outRaswd= csvName+"_wd_6ft.tif"
        print "Creating %s 6 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_6ft", outPathras+outRaswd, "MOST_FREQUENT", "", 10)


        
        #Name of the 1 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_1mph.tif"
        print "Creating %s 1 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_1mph", outPathras+outRasfv, "MOST_FREQUENT", "", 10)

        #Name of the 2 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_2mph.tif"
        print "Creating %s 2 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_2mph", outPathras+outRasfv, "MOST_FREQUENT", "", 10)

        #Name of the 4 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_4mph.tif"
        print "Creating %s 4 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_4mph", outPathras+outRasfv, "MOST_FREQUENT", "", 10)

        #Name of the 6 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_6mph.tif"
        print "Creating %s 6 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_6mph", outPathras+outRasfv, "MOST_FREQUENT", "", 10)

        #Name of the 8 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_8mph.tif"
        print "Creating %s 8 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_8mph", outPathras+outRasfv, "MOST_FREQUENT", "", 10)


        
        #Name of the .5 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_hlf_4.tif"
        print "Creating %s 1/2 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_hlf_4", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 1 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_1_4.tif"
        print "Creating %s 1 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_1_4", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 2 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_2_4.tif"
        print "Creating %s 2 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_2_4", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the .5 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_hlf_6.tif"
        print "Creating %s 1/2 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_hlf_6", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 1 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_1_6.tif"
        print "Creating %s 1 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_1_6", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 2 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_2_6.tif"
        print "Creating %s 2 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_2_6", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 3 foot wd, 2 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_3_2.tif"
        print "Creating %s 3 ft 2 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_3_2", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 4 foot wd, 2 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_4_2.tif"
        print "Creating %s 4 ft 2 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_4_2", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 5 foot wd, 1 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_5_1.tif"
        print "Creating %s 5 ft 1 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_5_1", outPathras+outRascrit, "MOST_FREQUENT", "", 10)

        #Name of the 6 foot wd, 1 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_6_1.tif"
        print "Creating %s 6 ft 1 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_6_1", outPathras+outRascrit, "MOST_FREQUENT", "", 10)
     
print "Processing complete"


##END##
