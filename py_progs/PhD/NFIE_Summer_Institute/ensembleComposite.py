#!/usr/bin/python

"""
Purpose: This script takes a directory
of hydraulic ensemble data and adds
together the rasters into a new raster.


"""

__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/06/21 12:57:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
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

EDITED: Chris Zarzar 23-Jun-2016
Added new wd, fv, and crit threshold rasters.

EDITED: Chris Zarzar 30-Jun-2016
Added second portion to script which will take the raster
output, will reproject the raster, and will update
the symbology of the rasters. The reason for this is that
I do not need to export from raster format anymore because
I am not going to use Tehtys

EDITED: Chris Zarzar 4-Mar-2017
Deleted entire script and replaced with the final portions of processing
in the csv2raster2composite script. This made it more concise
Also discovered the ApplySymbologyFromLayer_management arcpy command
which may work better than the UpdateLayer command.


_______________________________________________________

"""

print "Importing modules and setting up system variables"

##Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap
arcpy.env.overwriteOutput = True

##Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\"

##Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

##Setup environment setting
env.workspace = path+"workspace\\"

##Input locaiton for original HEC-RAS rasters
#hecRasdir = path+"modelOutput\\hecrasOutput\\"

##Input location of the all postprocessed rasters I ant composited for part 2 of script
rasDir = path+"postprocessOutput\\rasters\\ensembles\\"

##output location of the composite rasters for part 2 of script
outPathcomp = path+"postprocessOutput\\rasters\\composites\\"

#input location of the rasters for part 3 of script
rasDir2 = path+"postprocessOutput\\rasters\\composites\\"

##Location of the MXD document that will be created and edited
mapDoc = path+"imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

##Output location of the raster layers created
outlyrDir = path+"postprocessOutput\\rasters\\layers\\"

##Set up the spatial refernce for the file
spatialRef = arcpy.SpatialReference(32618) # 32618 is code for WGS_1984_UTM_Zone_18N 102387 is code for NAD_1983_2011_UTM_Zone_18N
print "Beginning third step of script processing"

#Set up blank raster to use
outBlank = path+"postprocessOutput\\rasters\\blankRaster\\blankRaster.tif"
print "Creating blank raster" 
##blankOut = Con((Raster(path+preRasdir+"\\FM_1_Q1_Depth.tif") == 2),0,0)
##blankOut.save(outBlank) 

##List the files in the ensemble directory
dirList2 = os.listdir(rasDir)

##List the files found in dirList with their full pathname
fileList3 = [rasDir+"\\"+filename3 for filename3 in dirList2]

##Set up count which will be used to calculated the percent in each grid
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


##Set the output rasters to a blank raster that the ensembles can be added to
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


##Set up loop
try:
    for inRas in fileList3:
        if inRas.endswith('.tif'):
            if "fldext" in inRas:
                
                print "processing"+inRas
                
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
                
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
                
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fldext = Con(IsNull(outRascomp_fldext),0,outRascomp_fldext)
                valRas = Con(IsNull(valRas),0,valRas)
    
                ##Add raster to composite raster
                outRascomp_fldext += valRas
                
                count1 += 1
                
            elif "wd_hlfft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_hlfft = Con(IsNull(outRascomp_wd_hlfft),0,outRascomp_wd_hlfft)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_wd_hlfft += valRas
    
                count2 += 1
    
            elif "wd_1ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_1ft = Con(IsNull(outRascomp_wd_1ft),0,outRascomp_wd_1ft)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_wd_1ft += valRas
    
                count3 += 1
                
            elif "wd_2ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_2ft = Con(IsNull(outRascomp_wd_2ft),0,outRascomp_wd_2ft)
                valRas = Con(IsNull(valRas),0,valRas)
               
                ##Add raster to composite raster
                outRascomp_wd_2ft += valRas
    
                count4 += 1
    
            elif "wd_3ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_3ft = Con(IsNull(outRascomp_wd_3ft),0,outRascomp_wd_3ft)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_wd_3ft += valRas
    
                count5 += 1
    
            elif "wd_4ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_4ft = Con(IsNull(outRascomp_wd_4ft),0,outRascomp_wd_4ft)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_wd_4ft += valRas
    
                count6 += 1
    
            elif "wd_5ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_5ft = Con(IsNull(outRascomp_wd_5ft),0,outRascomp_wd_5ft)
                valRas = Con(IsNull(valRas),0,valRas)
    
                ##Add raster to composite raster
                outRascomp_wd_5ft += valRas
    
                count7 += 1
    
            elif "wd_6ft" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_wd_6ft = Con(IsNull(outRascomp_wd_6ft),0,outRascomp_wd_6ft)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_wd_6ft += valRas
    
                count8 += 1
            
                
            elif "fv_1mph" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object 
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fv_1mph = Con(IsNull(outRascomp_fv_1mph),0,outRascomp_fv_1mph)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_fv_1mph += valRas
    
                count9 += 1
    
                
            elif "fv_2mph" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object 
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fv_2mph = Con(IsNull(outRascomp_fv_2mph),0,outRascomp_fv_2mph)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_fv_2mph += valRas
    
                count10 += 1
    
    
            elif "fv_4mph" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object 
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fv_4mph = Con(IsNull(outRascomp_fv_4mph),0,outRascomp_fv_4mph)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_fv_4mph += valRas
    
                count11 += 1
    
            elif "fv_6mph" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object 
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fv_6mph = Con(IsNull(outRascomp_fv_6mph),0,outRascomp_fv_6mph)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_fv_6mph += valRas
    
                count12 += 1
    
            elif "fv_8mph" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object 
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_fv_8mph = Con(IsNull(outRascomp_fv_8mph),0,outRascomp_fv_8mph)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_fv_8mph += valRas
    
                count13 += 1
    
    
            elif "crit_hlf_4" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_hlf_4 = Con(IsNull(outRascomp_crit_hlf_4),0,outRascomp_crit_hlf_4)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_hlf_4 += valRas
    
                count14 += 1
                
            elif "crit_1_4" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_1_4 = Con(IsNull(outRascomp_crit_1_4),0,outRascomp_crit_1_4)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_1_4 += valRas
    
                count15 += 1
                
            elif "crit_2_4" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_2_4 = Con(IsNull(outRascomp_crit_2_4),0,outRascomp_crit_2_4)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_2_4 += valRas
    
                count16 += 1
                
            elif "crit_hlf_6" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_hlf_6 = Con(IsNull(outRascomp_crit_hlf_6),0,outRascomp_crit_hlf_6)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_hlf_6 += valRas
    
                count17 += 1
    
            elif "crit_1_6" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_1_6 = Con(IsNull(outRascomp_crit_1_6),0,outRascomp_crit_1_6)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_1_6 += valRas
    
                count18 += 1
    
            elif "crit_2_6" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_2_6 = Con(IsNull(outRascomp_crit_2_6),0,outRascomp_crit_2_6)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_2_6 += valRas
    
                count19 += 1
    
            elif "crit_3_2" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_3_2 = Con(IsNull(outRascomp_crit_3_2),0,outRascomp_crit_3_2)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_3_2 += valRas
    
                count20 += 1
    
    
            elif "crit_4_2" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_4_2 = Con(IsNull(outRascomp_crit_4_2),0,outRascomp_crit_4_2)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_4_2 += valRas
    
                count21 += 1
    
            elif "crit_5_1" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_5_1 = Con(IsNull(outRascomp_crit_5_1),0,outRascomp_crit_5_1)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_5_1 += valRas
    
                count22 += 1
    
            elif "crit_6_1" in inRas:
                
                print "processing"+inRas
    
                ##Assign the raster an object  
                valueRaster = Raster(inRas)
    
                ##Con statement to fix the values. While the field values are correct, the pixel values are 1 for field values of 0 and 2 for field values of 1.
                valRas = Con(valueRaster, 1, 0, "Value = 2")
    
                ##Convert values of NoData to Zero so that slight differences in extent will not matter
                outRascomp_crit_6_1 = Con(IsNull(outRascomp_crit_6_1),0,outRascomp_crit_6_1)
                valRas = Con(IsNull(valRas),0,valRas)
                
                ##Add raster to composite raster
                outRascomp_crit_6_1 += valRas
    
                count23 += 1
    
                
    ##Save the composite raster        
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
    
    ##Divide each composite raster by the count to get the percent agreement 
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
    
    ##Save the final percentage raster
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
except:
    pass

"""
---------------------------------------------------------------------------
START THE FOURTH PART OF SCRIPT
---------------------------------------------------------------------------
"""


print "Beginning fourth step of script processing"





## Source layers that will be used for symbology reference
fldext_srcLyr = mp.Layer(outlyrDir+"fldext_source_stretch.lyr")
wd_srcLyr = mp.Layer(outlyrDir+"wd_source_stretch.lyr")
fv_srcLyr = mp.Layer(outlyrDir+"fv_source_stretch.lyr")
crit_srcLyr = mp.Layer(outlyrDir+"crit_source_stretch.lyr")

spatialRef = arcpy.SpatialReference(3857) # 3857 is code for WGS_1984_Web_Mecator (auxiliary sphere)

## Remove all current possible layers in the MXD
for df in mp.ListDataFrames(mxd):
    for lyr in mp.ListLayers(mxd,"*",df):
        mp.RemoveLayer(df, lyr)


## Set up raster list
dirList2 = os.listdir(rasDir2)

## List the files found in dirList with their full pathname
rasList2 = [rasDir2+filename for filename in dirList2 if filename.endswith(".tif")]


## Set up loop for adding raster layers to MXD
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
        ## Update the symbology of the layers added
        if "fldext" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            #mp.UpdateLayer(df, wrkLyr, fldext_srcLyr, True)
            ap.ApplySymbologyFromLayer_management(wrkLyr, fldext_srcLyr)
        elif "wd" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            #mp.UpdateLayer(df, wrkLyr, wd_srcLyr, True)
            ap.ApplySymbologyFromLayer_management(wrkLyr, wd_srcLyr)
        elif "fv" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            #mp.UpdateLayer(df, wrkLyr, fv_srcLyr, True)
            ap.ApplySymbologyFromLayer_management(wrkLyr, fv_srcLyr)
        elif "crit" in rasName2:
            wrkLyr.name = os.path.basename(rasProj[:-4])
            #mp.UpdateLayer(df, wrkLyr, crit_srcLyr, True)
            ap.ApplySymbologyFromLayer_management(wrkLyr, crit_srcLyr)
        mp.AddLayer(df, wrkLyr)
        
        

## Create the vector to loop through
lyrVec = mp.ListLayers(df)

## To be safe, start by hiding all of the layers
for lyr in lyrVec:
    lyr.visible = False
mxd.save()


print "Processing Complete"
