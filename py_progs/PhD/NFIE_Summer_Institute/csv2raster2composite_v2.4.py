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

__version__ = "$Revision: 2.4 $"[11:-2]
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
Tried adding if statment to create first composite layer
rather than using a blank raster. Script does not work

EDITED: Chris Zarzar 7-Jul-2016
After trial and error, I have taken my old script from
ensembleComposite.py and put it back in here. I also
found that the method I use to create the blank raster
and then add to the main raster were the basis of all
of my issues.

EDITED: Chris Zarzar 7-Jul-2016
Adjusted the script so that the User can provide the
root path to all of the data. This requires that the
user have a similar structure set up to the program.
The primary this is that all data is located under a
main directory. In that main directory will be:
[MAINDIR]\\workspace\\
[MAINDIR]\\modelOutput\\
[MAINDIR]\\postprocessOutput\\shapefiles\\
[MAINDIR]\\postprocessOutput\\rasters\\ensembles\\
[MAINDIR]\\postprocessOutput\\rasters\\composites\\
[MAINDIR]\\postprocessOutput\\rasters\\layers\\
[MAINDIR]\\imgCreation.mxd

EDITED: Chris Zarzar 7-Jul-2016
Basic reorganization of the script

EDITED: Chris Zarzar 7-Jul-2016
Discovered that the issue I was having is that I needed
to make it a float calculation. So all I had to do
after those days of work was simply make each count
float(count#)

EDITED: Chris Zarzar 12-Jul-2016
Added in a third portion to the script that will process
rasters that do not need shapefile conversion prior,
they just need to have conditional test done on them
and create new rasters from those results
Also added the Con(IsNull()) when i added the rasters
together because the output of both converts anypoint
in the grid that does not have data to a value of NoData.
That causes issues when adding rasters together, so
this will fix that problem. 
_______________________________________________________

"""
print "Beginning first step of script processing"
#Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap
arcpy.env.overwriteOutput = True


#Set the base path for all files ***REQUIRED USER INPUT***
path = "F:\\NFIE_SI_2016\\groupProject\\"

#Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#Setup environment setting
env.workspace = path+"workspace\\"

#output location of the shapefiles
outPathshp = path+"postprocessOutput\\shapefiles\\"

#output location of the rasters
outPathras = path+"postprocessOutput\\rasters\\ensembles\\"

#Input locaiton for original HEC-RAS rasters
hecRasdir = path+"modelOutput\\hecrasOutput\\"

#Input location of the rasters for part 2 of script
rasDir = path+"postprocessOutput\\rasters\\ensembles\\"

#Path of your CSV Files 
csvDir = path+"modelOutput\\csvFiles\\"

#output location of the composite rasters for part 2 of script
outPathcomp = path+"postprocessOutput\\rasters\\composites\\"

#input location of the rasters for part 3 of script
rasDir2 = path+"postprocessOutput\\rasters\\composites\\"

#Location of the MXD document that will be created and edited
mapDoc = path+"imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

#Output location of the raster layers created
outlyrDir = path+"postprocessOutput\\rasters\\layers\\"

#Set up the spatial refernce for the file
spatialRef = arcpy.SpatialReference(32618) # 32618 is code for WGS_1984_UTM_Zone_18N 102387 is code for NAD_1983_2011_UTM_Zone_18N

#List the files in the CSV directory
dirList = os.listdir(csvDir)

#List the files found in dirList with their full pathname
fileList = [csvDir+"\\"+filename for filename in dirList]

#List the rasters in the CSV directory
hecList = os.listdir(hecRasdir)

#List the files found in hecList with their full pathname
fileList2 = [hecRasdir+"\\"+filename2 for filename2 in hecList]

#List the files in the ensemble directory
dirList2 = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList3 = [rasDir+"\\"+filename3 for filename3 in dirList2]




"""---CREATE SHAPEFILE---"""

#Set up loop to postprocess iRIC output
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
##
##        arcpy.AddField_management(outPathshp+outFC,"blank", "TEXT")
##        
##        arcpy.AddField_management(outPathshp+outFC,"fldext", "TEXT")
##        
##        arcpy.AddField_management(outPathshp+outFC,"wd_hlfft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_1ft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_2ft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_3ft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_4ft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_5ft", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"wd_6ft", "TEXT")
##        
##        arcpy.AddField_management(outPathshp+outFC,"fv_1mph", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"fv_2mph", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"fv_4mph", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"fv_6mph", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"fv_8mph", "TEXT")
##        
##        arcpy.AddField_management(outPathshp+outFC,"crit_hlf_4", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_1_4", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_2_4", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_hlf_6", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_1_6", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_2_6", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_3_2", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_4_2", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_5_1", "TEXT")
##        arcpy.AddField_management(outPathshp+outFC,"crit_6_1", "TEXT")
##
##        upCur = arcpy.UpdateCursor(outPathshp+outFC)
##        
##        #values of output are in SI units. So these values used in
##        #conditional statements below will now match the imperial
##        #units in the header name
##        for row in upCur:
##
##            row.blank = 0
##
##            if (row.Depth > 0.05): row.fldext = 1
##            else: row.fldext = 0
##            
##            if (row.Depth >= .15): row.wd_hlfft = 1
##            else: row.wd_hlfft = 0
##            if (row.Depth >= .305): row.wd_1ft = 1
##            else: row.wd_1ft = 0
##            if (row.Depth >= .61): row.wd_2ft = 1
##            else: row.wd_2ft = 0
##            if (row.Depth >= .91): row.wd_3ft = 1
##            else: row.wd_3ft = 0
##            if (row.Depth >= 1.22): row.wd_4ft = 1
##            else: row.wd_4ft = 0
##            if (row.Depth >= 1.5): row.wd_5ft = 1
##            else: row.wd_5ft = 0
##            if (row.Depth >= 1.83): row.wd_6ft = 1
##            else: row.wd_6ft = 0
##            
##            if (row.Velocity__ >=.45 and row.Depth >=0.05): row.fv_1mph = 1
##            else: row.fv_1mph = 0
##            if (row.Velocity__ >=.89 and row.Depth >=0.05): row.fv_2mph = 1
##            else: row.fv_2mph = 0
##            if (row.Velocity__ >=1.79 and row.Depth >=0.05): row.fv_4mph = 1
##            else: row.fv_4mph = 0
##            if (row.Velocity__ >=2.68 and row.Depth >=0.05): row.fv_6mph = 1
##            else: row.fv_6mph = 0
##            if (row.Velocity__ >=3.58 and row.Depth >=0.05): row.fv_8mph = 1
##            else: row.fv_8mph = 0
##
##
##            if (row.Depth >=.15 and row.Velocity__ >=1.79): row.crit_hlf_4 = 1
##            else: row.crit_hlf_4 = 0
##            if (row.Depth >=.305 and row.Velocity__ >=1.79): row.crit_1_4 = 1
##            else: row.crit_1_4 = 0
##            if (row.Depth >=.61 and row.Velocity__ >=1.79): row.crit_2_4 = 1
##            else: row.crit_2_4 = 0
##            if (row.Depth >=.15 and row.Velocity__ >=2.68): row.crit_hlf_6 = 1
##            else: row.crit_hlf_6 = 0
##            if (row.Depth >=.305 and row.Velocity__ >=2.68): row.crit_1_6 = 1
##            else: row.crit_1_6 = 0
##            if (row.Depth >=.61 and row.Velocity__ >=2.68): row.crit_2_6 = 1
##            else: row.crit_2_6 = 0
##            if (row.Depth >=.91 and row.Velocity__ >=.89): row.crit_3_2 = 1
##            else: row.crit_3_2 = 0
##            if (row.Depth >=1.22 and row.Velocity__ >=.89): row.crit_4_2 = 1
##            else: row.crit_4_2 = 0
##            if (row.Depth >= 1.5 and row.Velocity__ >=.45): row.crit_5_1 = 1
##            else: row.crit_5_1 = 0
##            if (row.Depth >= 1.83 and row.Velocity__ >=.45): row.crit_6_1 = 1
##            else: row.crit_6_1 = 0
##            
##            upCur.updateRow(row)
##        del upCur, row
        arcpy.Delete_management("tempLay", 'GPFeatureLayer')


        
        
        """----CREATE RASTERS FROM SHAPEFILE----"""
        
      
        #Size of output raster cells
        cellSize = "5"

        #Value parameter for cell assignment
        cellAssign = "MAXIMUM"

        #Set up blank rasters to add onto each
        outBlank = path+"postprocessOutput\\rasters\\blankRaster\\blankRaster.tif"
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
START THE SECOND PART OF SCRIPT: CREATE HECRAS ENSEMBLE RASTERS
---------------------------------------------------------------------------
"""
print "Beginning second step of script processing"



##
##
##"""
##---------------------------------------------------------------------------
##START THE SECOND PART OF SCRIPT: CREATE HECRAS ENSEMBLE RASTERS
##---------------------------------------------------------------------------
##"""
##print "Beginning second step of script processing"
##
###Set up look to postprocess HEC-RAS output
##
##for hecRas in fileList2:
##    if hecRas.endswith('.tif'):
##        #Extract the .csv file name for naming purposes
##        hecName = os.path.basename(hecRas[:-4])
##        #has to add intergers to the naming convention so I can reference them later
##        if "Depth" in hecName:
##
##            print "Creating water depth rasters for "+hecName
##
##            outRasfldext = hecName+"_fldext.tif"
##            hecOut = Con(Raster(hecRas) > 0.05,2,1)
##            hecOut.save(outPathras+outRasfldext)
##
##            outRaswd1 = hecName+"_wd_hlfft.tif"
##            hecOut = Con(Raster(hecRas) >= 0.15,2,1)
##            hecOut.save(outPathras+outRaswd1)
##            
##            outRaswd2 = hecName+"_wd_1ft.tif"
##            hecOut = Con(Raster(hecRas) >= 0.305,2,1)
##            hecOut.save(outPathras+outRaswd2)
##            
##            outRaswd3 = hecName+"_wd_2ft.tif"
##            hecOut = Con(Raster(hecRas) >= 0.61,2,1)
##            hecOut.save(outPathras+outRaswd3)
##
##            outRaswd4 = hecName+"_wd_3ft.tif"
##            hecOut = Con(Raster(hecRas) >= 0.91,2,1)
##            hecOut.save(outPathras+outRaswd4)
##            
##            outRaswd5 = hecName+"_wd_4ft.tif"
##            hecOut = Con(Raster(hecRas) >= 1.22,2,1)
##            hecOut.save(outPathras+outRaswd5)
##
##            outRaswd6 = hecName+"_wd_5ft.tif"
##            hecOut = Con(Raster(hecRas) >= 1.5,2,1)
##            hecOut.save(outPathras+outRaswd6)
##            
##            outRaswd7 = hecName+"_wd_6ft.tif"
##            hecOut = Con(Raster(hecRas) >= 1.83,2,1)
##            hecOut.save(outPathras+outRaswd7)
##
##        if "Velocity" in hecName:
##            
##            print "Creating flow velocity rasters for "+hecName
##            
##            outRasfv1 = hecName+"_fv_1mph.tif"
##            hecOut = Con(Raster(hecRas) >= 0.45,2,1)
##            hecOut.save(outPathras+outRasfv1)
##
##            outRasfv2 = hecName+"_fv_2mph.tif"
##            hecOut = Con(Raster(hecRas) >= 0.89,2,1)
##            hecOut.save(outPathras+outRasfv2)
##            
##            outRasfv3 = hecName+"_fv_4mph.tif"
##            hecOut = Con(Raster(hecRas) >= 1.79,2,1)
##            hecOut.save(outPathras+outRasfv3)
##            
##            outRasfv4 = hecName+"_fv_6mph.tif"
##            hecOut = Con(Raster(hecRas) >= 2.68,2,1)
##            hecOut.save(outPathras+outRasfv4)
##
##            outRasfv5 = hecName+"_fv_8mph.tif"
##            hecOut = Con(Raster(hecRas) >= 3.58,2,1)
##            hecOut.save(outPathras+outRasfv5)
##
##        #Now outside of these if statements do the critical conditions rasters so i can reference temp wd and fv rasters
##            try:
##                outRaswd1
##                outRasfv1
##            except NameError:
##                print "Veloctiy output Rasters not yet created"
##            else:
##                print "Creating critical condition rasters for "+hecName
##                
##                outRascrit1 = hecName+"_crit_hlf_4.tif"
##                hecOut = Con((Raster(outPathras+outRaswd1)== 2) & (Raster(outPathras+outRasfv3)==2),2,1)
##                hecOut.save(outPathras+outRascrit1)
##                
##                outRascrit2 = hecName+"_crit_1_4.tif"
##                hecOut = Con((Raster(outPathras+outRaswd2) == 2) & (Raster(outPathras+outRasfv3)==2),2,1)
##                hecOut.save(outPathras+outRascrit2)
##                
##                outRascrit3 = hecName+"_crit_2_4.tif"
##                hecOut = Con((Raster(outPathras+outRaswd3) == 2) & (Raster(outPathras+outRasfv3)==2),2,1)
##                hecOut.save(outPathras+outRascrit3)
##
##                outRascrit4 = hecName+"_crit_hlf_6.tif"
##                hecOut = Con((Raster(outPathras+outRaswd1) == 2) & (Raster(outPathras+outRasfv4)==2),2,1)
##                hecOut.save(outPathras+outRascrit4)
##
##                outRascrit5 = hecName+"_crit_1_6.tif"
##                hecOut = Con((Raster(outPathras+outRaswd2) == 2) & (Raster(outPathras+outRasfv4)==2),2,1)
##                hecOut.save(outPathras+outRascrit5)
##
##                outRascrit6 = hecName+"_crit_2_6.tif"
##                hecOut = Con((Raster(outPathras+outRaswd3) == 2) & (Raster(outPathras+outRasfv4)==2),2,1)
##                hecOut.save(outPathras+outRascrit6)
##
##                outRascrit7 = hecName+"_crit_3_2.tif"
##                hecOut = Con((Raster(outPathras+outRaswd4) == 2) & (Raster(outPathras+outRasfv2)==2),2,1)
##                hecOut.save(outPathras+outRascrit7)
##                
##                outRascrit8 = hecName+"_crit_4_2.tif"
##                hecOut = Con((Raster(outPathras+outRaswd5) == 2) & (Raster(outPathras+outRasfv2)==2),2,1)
##                hecOut.save(outPathras+outRascrit8)
##
##                outRascrit9 = hecName+"_crit_5_1.tif"
##                hecOut = Con((Raster(outPathras+outRaswd6) == 2) & (Raster(outPathras+outRasfv1)==2),2,1)
##                hecOut.save(outPathras+outRascrit9) 
##
##                outRascrit10 = hecName+"_crit_6_1.tif"
##                hecOut = Con((Raster(outPathras+outRaswd7) == 2) & (Raster(outPathras+outRasfv1)==2),2,1)
##                hecOut.save(outPathras+outRascrit10) 
##
##
##
##print "Second of script processing complete"
##





print "Second of script processing complete"



"""
---------------------------------------------------------------------------
START THE THIRD PART OF SCRIPT: CREATE COMPOSIT RASTERS
---------------------------------------------------------------------------
"""

print "Beginning third step of script processing"



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


#Set the output rasters to a blank raster that the ensembles can be added to
outRascomp_fldext = Con(Raster(outBlank), 0, 0, "Value = 0")

outRascomp_wd_hlfft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_1ft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_2ft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_3ft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_4ft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_5ft = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_wd_6ft = Con(Raster(outBlank), 0, 0, "Value = 0")

outRascomp_fv_1mph = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_fv_2mph = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_fv_4mph = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_fv_6mph = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_fv_8mph = Con(Raster(outBlank), 0, 0, "Value = 0")

outRascomp_crit_hlf_4 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_1_4 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_2_4 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_hlf_6 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_1_6 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_2_6 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_3_2 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_4_2 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_5_1 = Con(Raster(outBlank), 0, 0, "Value = 0")
outRascomp_crit_6_1 = Con(Raster(outBlank), 0, 0, "Value = 0")


#Set up loop
for inRas in fileList3:
    if inRas.endswith('.tif'):
        if "fldext" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)
            
            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")
            
            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fldext = Con(IsNull(outRascomp_fldext),0,outRascomp_fldext)
            valRas = Con(IsNull(valRas),0,valRas)

            #Add raster to composite raster
            outRascomp_fldext += valRas
            
            count1 += 1
            
        elif "wd_hlfft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_hlfft = Con(IsNull(outRascomp_wd_hlfft),0,outRascomp_wd_hlfft)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_wd_hlfft += valRas

            count2 += 1

        elif "wd_1ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_1ft = Con(IsNull(outRascomp_wd_1ft),0,outRascomp_wd_1ft)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_wd_1ft += valRas

            count3 += 1
            
        elif "wd_2ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_2ft = Con(IsNull(outRascomp_wd_2ft),0,outRascomp_wd_2ft)
            valRas = Con(IsNull(valRas),0,valRas)
           
            #Add raster to composite raster
            outRascomp_wd_2ft += valRas

            count4 += 1

        elif "wd_3ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_3ft = Con(IsNull(outRascomp_wd_3ft),0,outRascomp_wd_3ft)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_wd_3ft += valRas

            count5 += 1

        elif "wd_4ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_4ft = Con(IsNull(outRascomp_wd_4ft),0,outRascomp_wd_4ft)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_wd_4ft += valRas

            count6 += 1

        elif "wd_5ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_5ft = Con(IsNull(outRascomp_wd_5ft),0,outRascomp_wd_5ft)
            valRas = Con(IsNull(valRas),0,valRas)

            #Add raster to composite raster
            outRascomp_wd_5ft += valRas

            count7 += 1

        elif "wd_6ft" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_wd_6ft = Con(IsNull(outRascomp_wd_6ft),0,outRascomp_wd_6ft)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_wd_6ft += valRas

            count8 += 1
        
            
        elif "fv_1mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fv_1mph = Con(IsNull(outRascomp_fv_1mph),0,outRascomp_fv_1mph)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_fv_1mph += valRas

            count9 += 1

            
        elif "fv_2mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fv_2mph = Con(IsNull(outRascomp_fv_2mph),0,outRascomp_fv_2mph)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_fv_2mph += valRas

            count10 += 1


        elif "fv_4mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fv_4mph = Con(IsNull(outRascomp_fv_4mph),0,outRascomp_fv_4mph)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_fv_4mph += valRas

            count11 += 1

        elif "fv_6mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fv_6mph = Con(IsNull(outRascomp_fv_6mph),0,outRascomp_fv_6mph)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_fv_6mph += valRas

            count12 += 1

        elif "fv_8mph" in inRas:

            #Assign the raster an object 
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_fv_8mph = Con(IsNull(outRascomp_fv_8mph),0,outRascomp_fv_8mph)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_fv_8mph += valRas

            count13 += 1


        elif "crit_hlf_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_hlf_4 = Con(IsNull(outRascomp_crit_hlf_4),0,outRascomp_crit_hlf_4)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_hlf_4 += valRas

            count14 += 1
            
        elif "crit_1_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_1_4 = Con(IsNull(outRascomp_crit_1_4),0,outRascomp_crit_1_4)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_1_4 += valRas

            count15 += 1
            
        elif "crit_2_4" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_2_4 = Con(IsNull(outRascomp_crit_2_4),0,outRascomp_crit_2_4)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_2_4 += valRas

            count16 += 1
            
        elif "crit_hlf_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_hlf_6 = Con(IsNull(outRascomp_crit_hlf_6),0,outRascomp_crit_hlf_6)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_hlf_6 += valRas

            count17 += 1

        elif "crit_1_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_1_6 = Con(IsNull(outRascomp_crit_1_6),0,outRascomp_crit_1_6)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_1_6 += valRas

            count18 += 1

        elif "crit_2_6" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_2_6 = Con(IsNull(outRascomp_crit_2_6),0,outRascomp_crit_2_6)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_2_6 += valRas

            count19 += 1

        elif "crit_3_2" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_3_2 = Con(IsNull(outRascomp_crit_3_2),0,outRascomp_crit_3_2)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_3_2 += valRas

            count20 += 1


        elif "crit_4_2" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_4_2 = Con(IsNull(outRascomp_crit_4_2),0,outRascomp_crit_4_2)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_4_2 += valRas

            count21 += 1

        elif "crit_5_1" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_5_1 = Con(IsNull(outRascomp_crit_5_1),0,outRascomp_crit_5_1)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_5_1 += valRas

            count22 += 1

        elif "crit_6_1" in inRas:

            #Assign the raster an object  
            valueRaster = Raster(inRas)

            #Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
            valRas = Con(valueRaster, 1, 0, "Value = 2")

            #Convert values of NoData to Zero so that slight differences in extent will not matter
            outRascomp_crit_6_1 = Con(IsNull(outRascomp_crit_6_1),0,outRascomp_crit_6_1)
            valRas = Con(IsNull(valRas),0,valRas)
            
            #Add raster to composite raster
            outRascomp_crit_6_1 += valRas

            count23 += 1

            
#Save the composite raster        
outRascomp_fldext.save(outPathcomp+"rasComp_fldext.tif")

outRascomp_wd_hlfft.save(outPathcomp+"rasComp_wd_hlfft.tif")
outRascomp_wd_1ft.save(outPathcomp+"rasComp_wd_1ft.tif")
outRascomp_wd_2ft.save(outPathcomp+"rasComp_wd_2ft.tif")
outRascomp_wd_3ft.save(outPathcomp+"rasComp_wd_3ft.tif")
outRascomp_wd_4ft.save(outPathcomp+"rasComp_wd_4ft.tif")
outRascomp_wd_5ft.save(outPathcomp+"rasComp_wd_5ft.tif")
outRascomp_wd_6ft.save(outPathcomp+"rasComp_wd_6ft.tif")

outRascomp_fv_1mph.save(outPathcomp+"rasComp_fv_1mph.tif")
outRascomp_fv_2mph.save(outPathcomp+"rasComp_fv_2mph.tif")
outRascomp_fv_4mph.save(outPathcomp+"rasComp_fv_4mph.tif")
outRascomp_fv_6mph.save(outPathcomp+"rasComp_fv_6mph.tif")
outRascomp_fv_8mph.save(outPathcomp+"rasComp_fv_8mph.tif")

outRascomp_crit_hlf_4.save(outPathcomp+"rasComp_crit_hlf_4.tif")
outRascomp_crit_1_4.save(outPathcomp+"rasComp_crit_1_4.tif")
outRascomp_crit_2_4.save(outPathcomp+"rasComp_crit_2_4.tif")
outRascomp_crit_hlf_6.save(outPathcomp+"rasComp_crit_hlf_6.tif")
outRascomp_crit_1_6.save(outPathcomp+"rasComp_crit_1_6.tif")
outRascomp_crit_2_6.save(outPathcomp+"rasComp_crit_2_6.tif")
outRascomp_crit_3_2.save(outPathcomp+"rasComp_crit_3_2.tif")
outRascomp_crit_4_2.save(outPathcomp+"rasComp_crit_4_2.tif")
outRascomp_crit_5_1.save(outPathcomp+"rasComp_crit_5_1.tif")
outRascomp_crit_6_1.save(outPathcomp+"rasComp_crit_6_1.tif")

#Divide each composite raster by the count to get the percent agreement 
outRas1 = outRascomp_fldext/float(count1)

outRas2 = outRascomp_wd_hlfft/float(count2)
outRas3 = outRascomp_wd_1ft/float(count3)
outRas4 = outRascomp_wd_2ft/float(count4)
outRas5 = outRascomp_wd_3ft/float(count5)
outRas6 = outRascomp_wd_4ft/float(count6)
outRas7 = outRascomp_wd_5ft/float(count7)
outRas8 = outRascomp_wd_6ft/float(count8)

outRas9 = outRascomp_fv_1mph/float(count9)
outRas10 = outRascomp_fv_2mph/float(count10)
outRas11 = outRascomp_fv_4mph/float(count11)
outRas12 = outRascomp_fv_6mph/float(count12)
outRas13 = outRascomp_fv_8mph/float(count13)

outRas14 = outRascomp_crit_hlf_4/float(count14)
outRas15 = outRascomp_crit_1_4/float(count15)
outRas16 = outRascomp_crit_2_4/float(count16)
outRas17 = outRascomp_crit_hlf_6/float(count17)
outRas18 = outRascomp_crit_1_6/float(count18)
outRas19 = outRascomp_crit_2_6/float(count19)
outRas20 = outRascomp_crit_3_2/float(count20)
outRas21 = outRascomp_crit_4_2/float(count21)
outRas22 = outRascomp_crit_5_1/float(count22)
outRas23 = outRascomp_crit_6_1/float(count23)

#Save the final percentage raster
outRas1.save(outPathcomp+"rasCompPer_fldext.tif")

outRas2.save(outPathcomp+"rasCompPer_wd_hlfft.tif")
outRas3.save(outPathcomp+"rasCompPer_wd_1ft.tif")
outRas4.save(outPathcomp+"rasCompPer_wd_2ft.tif")
outRas5.save(outPathcomp+"rasCompPer_wd_3ft.tif")
outRas6.save(outPathcomp+"rasCompPer_wd_4ft.tif")
outRas7.save(outPathcomp+"rasCompPer_wd_5ft.tif")
outRas8.save(outPathcomp+"rasCompPer_wd_6ft.tif")

outRas9.save(outPathcomp+"rasCompPer_fv_1mph.tif")
outRas10.save(outPathcomp+"rasCompPer_fv_2mph.tif")
outRas11.save(outPathcomp+"rasCompPer_fv_4mph.tif")
outRas12.save(outPathcomp+"rasCompPer_fv_6mph.tif")
outRas13.save(outPathcomp+"rasCompPer_fv_8mph.tif")

outRas14.save(outPathcomp+"rasCompPer_crit_hlf_4.tif")
outRas15.save(outPathcomp+"rasCompPer_crit_1_4.tif")
outRas16.save(outPathcomp+"rasCompPer_crit_2_4.tif")
outRas17.save(outPathcomp+"rasCompPer_crit_hlf_6.tif")
outRas18.save(outPathcomp+"rasCompPer_crit_1_6.tif")
outRas19.save(outPathcomp+"rasCompPer_crit_2_6.tif")
outRas20.save(outPathcomp+"rasCompPer_crit_3_2.tif")
outRas21.save(outPathcomp+"rasCompPer_crit_4_2.tif")
outRas22.save(outPathcomp+"rasCompPer_crit_5_1.tif")
outRas23.save(outPathcomp+"rasCompPer_crit_6_1.tif")

print "Third of script processing complete"


"""
---------------------------------------------------------------------------
START THE FOURTH PART OF SCRIPT
---------------------------------------------------------------------------
"""


print "Beginning fourth step of script processing"





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

