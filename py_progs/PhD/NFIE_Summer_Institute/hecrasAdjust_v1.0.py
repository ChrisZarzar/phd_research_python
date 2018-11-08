#!/usr/bin/python

"""
Purpose: This script will
take the HEC-RAS 2D output
that Michael Gomez provides
and will create new rasters
based on certain thresholds



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/07/12 9:34:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 12 July 2016
Contact: chriszarzar@gmail.com



----History----

CREATED: Chris Zarzar 12-Jul-2016


_______________________________________________________
"""

#Setting up the script
import os
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap
arcpy.env.overwriteOutput = True


#Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\Chris\\Desktop\\groupProject\\"

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
csvDir = path+"modelOutput\\"

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



#Set up look to postprocess HEC-RAS output

for hecRas in fileList2:
    if hecRas.endswith('.vrt'):
        #Extract the .csv file name for naming purposes
        hecName = os.path.basename(hecRas[:-4])
        if "Depth" in hecName:

            outRaswd = hecName+"_wd_1ft.tif"
            hecOut = Con(Raster(hecRas) >= .305, 1,0)
            hecOut.save(outPathras+outRaswd)
            outRaswd = hecName+"_wd_4ft.tif"
            hecOut2 = Con(Raster(hecRas) >=1.22,1,0)
            hecOut2.save(outPathras+outRaswd)



            #hecOut = Con((Raster("hecRas") >= .45) & (Raster("hecDepth") >=0.05),1,0)
##END##
