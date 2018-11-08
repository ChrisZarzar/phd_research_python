#!/usr/bin/python

"""
Purpose: This script takes a csv file
generated from each iRIC ensemble and
it will read through the rows to create
new csv files that will be used to convert
to raster and used to create the final
images. This script then takes a directory
of hydraulic ensemble data and adds
together the rasters into a new composite raster.



"""

__version__ = "$Revision: 2.1 $"[11:-2]
__date__ = "$Date: 2016/07/6 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 20 June 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 21-Jun-2016
Created script and set up to take a directory of ensembles
and add together grid cells that correspond to certain criteria

EDITED: Chris Zarzar 22-Jun-2016
Added nested if statements to create composites from each
ensemble raster output from the csv2floodRaster.py script

CREATED: Chris Zarzar 22-Jun-2016
Part two created script and set up to take the output iRIC csv
and edit the columns based on certain threshold requirements

EDITED: Chris Zarzar 23-Jun-2016
Added in new depths, flow velocities, and critical thresholds
Also decreased raster size to 10 meters for more detail

EDITED: Chris Zarzar 23-Jun-2016
Added new wd, fv, and crit threshold rasters.

EDITED: Chris Zarzar 30-Jun-2016
Added second portion to script which will take the raster
output, will reproject the raster, and will update
the symbology of the rasters. The reason for this is that
I do not need to export from raster format anymore because
I am not going to use Tehtys

EDITED: Chris Zarzar 6-Jul-2016
Script was not working with new results. I think it was
because of how it is determining the values of each new
raster cell. It is using mode, this will not work
if there are many zeros. I am thinkikng that I should use Max.
Max scares me, but I will use that for now and change later

EDITED: Chris Zarzar 6-Jul-2016
Changed cell size to 50 m because the Nyce 2D cell
size is 50 m

EDITED: Chris Zarzar 6-Jul-2016
Increased lowest value allow to call it inundated to 0.05.
This is because every cell is at least 0.01, so a value of
5 cm (~ 2 in) will be good to call it inundated.

EDITED: Chris Zarzar 6-Jul-2016
Tried to dynamically create variable and assign them to
the blank raster. It did not work. 

_______________________________________________________

"""
print "Beginning first step of script processing"

#Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace ="F:\\NFIE_SI_2016\\groupProject\\workspace\\"

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

        arcpy.AddField_management(outPathshp+outFC,"blank", "TEXT")
        
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

            row.blank = 0

            if (row.Depth > 0.05): row.fldext = 1
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
        
      
        #Size of output raster cells
        cellSize = "50"

        #Value parameter for cell assignment
        cellAssign = "MAXIMUM"

        #Set up blank rasters to add onto each
        outBlank = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\blankRaster\\blankRaster.tif"
        print "Creating %s blank raster" % csvName
        arcpy.PointToRaster_conversion(outPathshp+outFC, "blank", outBlank, cellAssign, "", cellSize)

        
        #Name of the .5 foot water depth raster to create
        outRasfldext= csvName+"_fldext.tif"
        print "Creating %s flood extent raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fldext", outPathras+outRasfldext, cellAssign, "", cellSize)


        #Name of the .5 foot water depth raster to create
        outRaswd= csvName+"_wd_hlfft.tif"
        print "Creating %s 1/2 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_hlfft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 1 foot water depth raster to create
        outRaswd= csvName+"_wd_1ft.tif"
        print "Creating %s 1 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_1ft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 2 foot water depth raster to create
        outRaswd= csvName+"_wd_2ft.tif"
        print "Creating %s 2 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_2ft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 3 foot water depth raster to create
        outRaswd= csvName+"_wd_3ft.tif"
        print "Creating %s 3 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_3ft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 4 foot water depth raster to create
        outRaswd= csvName+"_wd_4ft.tif"
        print "Creating %s 4 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_4ft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 5 foot water depth raster to create
        outRaswd= csvName+"_wd_5ft.tif"
        print "Creating %s 5 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_5ft", outPathras+outRaswd, cellAssign, "", cellSize)

        #Name of the 6 foot water depth raster to create
        outRaswd= csvName+"_wd_6ft.tif"
        print "Creating %s 6 foot water depth exceedance raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "wd_6ft", outPathras+outRaswd, cellAssign, "", cellSize)


        
        #Name of the 1 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_1mph.tif"
        print "Creating %s 1 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_1mph", outPathras+outRasfv, cellAssign, "", cellSize)

        #Name of the 2 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_2mph.tif"
        print "Creating %s 2 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_2mph", outPathras+outRasfv, cellAssign, "", cellSize)

        #Name of the 4 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_4mph.tif"
        print "Creating %s 4 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_4mph", outPathras+outRasfv, cellAssign, "", cellSize)

        #Name of the 6 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_6mph.tif"
        print "Creating %s 6 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_6mph", outPathras+outRasfv, cellAssign, "", cellSize)

        #Name of the 8 miles per hour flow velocity raster to create
        outRasfv = csvName+"_fv_8mph.tif"
        print "Creating %s 8 mph water flow velocity exceedance raster" % csvName 
        #Convert the newly created shapefile to a flow velocity magnitude raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "fv_8mph", outPathras+outRasfv, cellAssign, "", cellSize)


        
        #Name of the .5 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_hlf_4.tif"
        print "Creating %s 1/2 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_hlf_4", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 1 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_1_4.tif"
        print "Creating %s 1 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_1_4", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 2 foot wd, 4 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_2_4.tif"
        print "Creating %s 2 ft 4 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_2_4", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the .5 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_hlf_6.tif"
        print "Creating %s 1/2 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_hlf_6", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 1 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_1_6.tif"
        print "Creating %s 1 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_1_6", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 2 foot wd, 6 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_2_6.tif"
        print "Creating %s 2 ft 6 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_2_6", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 3 foot wd, 2 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_3_2.tif"
        print "Creating %s 3 ft 2 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_3_2", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 4 foot wd, 2 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_4_2.tif"
        print "Creating %s 4 ft 2 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_4_2", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 5 foot wd, 1 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_5_1.tif"
        print "Creating %s 5 ft 1 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_5_1", outPathras+outRascrit, cellAssign, "", cellSize)

        #Name of the 6 foot wd, 1 mph fv critical condition raster to create
        outRascrit= csvName+"_crit_6_1.tif"
        print "Creating %s 6 ft 1 mph critical condition raster" % csvName
        #Convert the newly created shapefile to a water depth raster
        arcpy.PointToRaster_conversion(outPathshp+outFC, "crit_6_1", outPathras+outRascrit, cellAssign, "", cellSize)
     
print "CSV to Raster processing complete"

print "First step of script processing complete"


"""
---------------------------------------------------------------------------
START THE SECOND PART OF SCRIPT
---------------------------------------------------------------------------
"""
outRasfldext= csvName+"_fldext.tif"

print "Beginning second step of script processing"


#Setting up the script
import arcpy
import os
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace ="F:\\NFIE_SI_2016\\groupProject\\workspace"

#input directory of the raster
rasDir = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\ensembles\\"

#output location of the Rasters
outPathras = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\composites\\"

#List the files in the CSV directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up count which will be used to calculated the percent in each grid
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0
count12 = 0
count13 = 0
count14 = 0
count15 = 0
count16 = 0
count17 = 0
count18 = 0
count19 = 0
count20 = 0
count21 = 0
count22 = 0
count23 = 0

#Assign value rasters to the blank raster
valRas = dict()
for n in range(1,24):
    valRas[n] = Raster("F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\blankRaster\\blankRaster.tif")

#Set up loop
for inRas in fileList:
    if inRas.endswith('.tif'):
        if "fldext" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)
            
            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[1] += valRas
            
            count1 += 1
            
        elif "wd_hlfft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[2] += valRas
            
            count2 += 1

        elif "wd_1ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[3] += valRas
            
            count3 += 1
            
        elif "wd_2ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[4] += valRas

            count4 += 1

        elif "wd_3ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[5] += valRas
            
            count5 += 1

        elif "wd_4ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[6] += valRas
            
            count6 += 1

        elif "wd_5ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[7] += valRas

            count7 += 1

        elif "wd_6ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[8] += valRas
            
            count8 += 1
        
            
        elif "fv_1mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[9] += valRas
            
            count9 += 1

            
        elif "fv_2mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[10] += valRas
            
            count10 += 1


        elif "fv_4mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[11] += valRas
            
            count11 += 1

        elif "fv_6mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[12] += valRas
            
            count12 += 1

        elif "fv_8mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[13] += valRas
            
            count13 += 1


        elif "crit_hlf_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[14] += valRas

            count14 += 1
            
        elif "crit_1_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[15] += valRas
            
            count15 += 1
            
        elif "crit_2_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[16] += valRas

            count16 += 1
            
        elif "crit_hlf_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            #valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[17] += valRaster
            
            count17 += 1

        elif "crit_1_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            #valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[18] += valRaster
            
            count18 += 1

        elif "crit_2_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[19] += valRas
            
            count19 += 1

        elif "crit_3_2" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[20] += valRas
            
            count20 += 1


        elif "crit_4_2" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[21] += valRas
            
            count21 += 1

        elif "crit_5_1" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[22] += valRas
            
            count22 += 1

        elif "crit_6_1" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Add raster to composite raster
            valRas[23] += valRas
            
            count23 += 1

            


#Divide each composite raster by the count to get the percent agreement 
outRas1 = valRas1/count1

outRas2 = valRas2/count2
outRas3 = valRas3/count3
outRas4 = valRas4/count4
outRas5 = valRas5/count5
outRas6 = valRas6/count6
outRas7 = valRas7/count7
outRas8 = valRas8/count8

outRas9 = valRas9/count9
outRas10 = valRas10/count10
outRas11 = valRas11/count11
outRas12 = valRas12/count12
outRas13 = valRas13/count13

outRas14 = valRas14/count14
outRas15 = valRas15/count15
outRas16 = valRas16/count16
outRas17 = valRas17/count17
outRas18 = valRas18/count18
outRas19 = valRas19/count19
outRas20 = valRas20/count20
outRas21 = valRas21/count21
outRas22 = valRas22/count22
outRas23 = valRas23/count23

#Save the composite raster        
valRas1.save(outPathras+"rasComp_fldext.tif")

valRas2.save(outPathras+"rasComp_wd_hlfft.tif")
valRas3.save(outPathras+"rasComp_wd_1ft.tif")
valRas4.save(outPathras+"rasComp_wd_2ft.tif")
valRas5.save(outPathras+"rasComp_wd_3ft.tif")
valRas6.save(outPathras+"rasComp_wd_4ft.tif")
valRas7.save(outPathras+"rasComp_wd_5ft.tif")
valRas8.save(outPathras+"rasComp_wd_6ft.tif")

valRas9.save(outPathras+"rasComp_fv_1mph.tif")
valRas10.save(outPathras+"rasComp_fv_2mph.tif")
valRas11.save(outPathras+"rasComp_fv_4mph.tif")
valRas12.save(outPathras+"rasComp_fv_6mph.tif")
valRas13.save(outPathras+"rasComp_fv_8mph.tif")

valRas14.save(outPathras+"rasComp_crit_hlf_4.tif")
valRas15.save(outPathras+"rasComp_crit_1_4.tif")
valRas16.save(outPathras+"rasComp_crit_2_4.tif")
valRas17.save(outPathras+"rasComp_crit_hlf_6.tif")
valRas18.save(outPathras+"rasComp_crit_1_6.tif")
valRas19.save(outPathras+"rasComp_crit_2_6.tif")
valRas20.save(outPathras+"rasComp_crit_3_2.tif")
valRas21.save(outPathras+"rasComp_crit_4_2.tif")
valRas22.save(outPathras+"rasComp_crit_5_1.tif")
valRas23.save(outPathras+"rasComp_crit_6_1.tif")

#Save the final percentage raster
outRas1.save(outPathras+"rasCompPer_fldext.tif")

outRas2.save(outPathras+"rasCompPer_wd_hlfft.tif")
outRas3.save(outPathras+"rasCompPer_wd_1ft.tif")
outRas4.save(outPathras+"rasCompPer_wd_2ft.tif")
outRas5.save(outPathras+"rasCompPer_wd_3ft.tif")
outRas6.save(outPathras+"rasCompPer_wd_4ft.tif")
outRas7.save(outPathras+"rasCompPer_wd_5ft.tif")
outRas8.save(outPathras+"rasCompPer_wd_6ft.tif")

outRas9.save(outPathras+"rasCompPer_fv_1mph.tif")
outRas10.save(outPathras+"rasCompPer_fv_2mph.tif")
outRas11.save(outPathras+"rasCompPer_fv_4mph.tif")
outRas12.save(outPathras+"rasCompPer_fv_6mph.tif")
outRas13.save(outPathras+"rasCompPer_fv_8mph.tif")

outRas14.save(outPathras+"rasCompPer_crit_hlf_4.tif")
outRas15.save(outPathras+"rasCompPer_crit_1_4.tif")
outRas16.save(outPathras+"rasCompPer_crit_2_4.tif")
outRas17.save(outPathras+"rasCompPer_crit_hlf_6.tif")
outRas18.save(outPathras+"rasCompPer_crit_1_6.tif")
outRas19.save(outPathras+"rasCompPer_crit_2_6.tif")
outRas20.save(outPathras+"rasCompPer_crit_3_2.tif")
outRas21.save(outPathras+"rasCompPer_crit_4_2.tif")
outRas22.save(outPathras+"rasCompPer_crit_5_1.tif")
outRas23.save(outPathras+"rasCompPer_crit_6_1.tif")

print "Second step of script processing complete"


"""
---------------------------------------------------------------------------
START THE THIRD PART OF SCRIPT
---------------------------------------------------------------------------
"""


print "Beginning third step of script processing"


# Set up variables
env.workspace = "F:\\NFIE_SI_2016\\groupProject\\workspace\\"
mapDoc = "F:\\NFIE_SI_2016\\groupProject\\imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

rasDir2 = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\composites\\"
outlyrDir = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\layers\\"


# Source layers that will be used for symbology reference
fldext_srcLyr = mp.Layer(outlyrDir+"fldext_source_stretch.lyr")
wd_srcLyr = mp.Layer(outlyrDir+"wd_source_stretch.lyr")
fv_srcLyr = mp.Layer(outlyrDir+"fv_source_stretch.lyr")
crit_srcLyr = mp.Layer(outlyrDir+"crit_source_stretch.lyr")

spatialRef = arcpy.SpatialReference(3857) # 3857 is code for WGS_1984_Web_Mecator (auxiliary sphere)

# Remove all current possible layers in the MXD
for df in mp.ListDataFrames(mxd):
    for lyr in mp.ListLayers(mxd,"*",df):
        mp.RemoveLayer(df, lyr)


# Set up raster list
dirList2 = os.listdir(rasDir2)

# List the files found in dirList with their full pathname
rasList2 = [rasDir2+filename for filename in dirList2 if filename.endswith(".tif")]


# Set up loop for adding raster layers to MXD
for ras in rasList2:
    rasName2 = os.path.basename(ras[:-4])
    if "Per" in rasName2:
        outLyr = outlyrDir+rasName2+".lyr"
        tmpLyr = outlyrDir+rasName2
        rasProj = rasDir2+rasName2+"wbMerc.tif"
        ap.ProjectRaster_management(ras, rasProj, spatialRef)
        ap.MakeRasterLayer_management(rasProj, tmpLyr)
        ap.SaveToLayerFile_management(tmpLyr, outLyr)
        wrkLyr = mp.Layer(outLyr)
        # Update the symbology of the layers added
        if "fldext" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            mp.UpdateLayer(df, wrkLyr, fldext_srcLyr, True)
        elif "wd" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            mp.UpdateLayer(df, wrkLyr, wd_srcLyr, True)
        elif "fv" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            mp.UpdateLayer(df, wrkLyr, fv_srcLyr, True)
        elif "crit" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            mp.UpdateLayer(df, wrkLyr, crit_srcLyr, True)
        mp.AddLayer(df, wrkLyr)
        
        

# Create the vector to loop through
lyrVec = mp.ListLayers(df)

# To be safe, start by hiding all of the layers
for lyr in lyrVec:
    lyr.visible = False
mxd.save()


print "Processing Complete"



##END##

