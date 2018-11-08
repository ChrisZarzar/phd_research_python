#!/usr/bin/python

"""
Purpose: This script will pull in
in raster files and will update the
raster symbology. It will then convert
the raster to kml format.



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/29 10:18:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 29 June 2016
Contact: chriszarzar@gmail.com

Notes: The script first removes all layers in the
map document provided. 

----History----

CREATED: Chris Zarzar 29-Jun-2016

EDITED: Chris Zarzar 29-Jun-2016
Added a line of code to reproject the rasters
before adding back in and updating the layer
_______________________________________________________
"""

#Set up the script
import arcpy as ap
import os
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Set up variables
env.workspace = "F:\\NFIE_SI_2016\\groupProject\\"
mapDoc = "F:\\NFIE_SI_2016\\groupProject\\imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

rasDir = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\composites\\"
outlyrDir = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\rasters\\layers\\"
outkmlDir = "F:\\NFIE_SI_2016\\groupProject\\postprocessOutput\\kml\\"

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
dirList = os.listdir(rasDir)

# List the files found in dirList with their full pathname
rasList = [rasDir+filename for filename in dirList if filename.endswith(".tif")]


# Set up loop for adding raster layers to MXD
for ras in rasList:
    rasName = os.path.basename(ras[:-4])
    if "Per" in rasName:
        outLyr = outlyrDir+rasName+".lyr"
        tmpLyr = outlyrDir+rasName
        rasProj = rasDir+rasName+"wbMerc.tif"
        ap.ProjectRaster_management(ras, rasProj, spatialRef)
        ap.MakeRasterLayer_management(rasProj, tmpLyr)
        ap.SaveToLayerFile_management(tmpLyr, outLyr)
        wrkLyr = mp.Layer(outLyr)
        # Update the symbology of the layers added
        if "fldext" in rasName:
            mp.UpdateLayer(df, wrkLyr, fldext_srcLyr, True)
        elif "wd" in rasName:
            mp.UpdateLayer(df, wrkLyr, wd_srcLyr, True)
        elif "fv" in rasName:
            mp.UpdateLayer(df, wrkLyr, fv_srcLyr, True)
        elif "crit" in rasName:
            mp.UpdateLayer(df, wrkLyr, crit_srcLyr, True)
        mp.AddLayer(df, wrkLyr)
        

# Create the vector to loop through
lyrVec = mp.ListLayers(df)

# To be safe, start by hiding all of the layers
for lyr in lyrVec:
    lyr.visible = False
mxd.save()


# Loop through all layers and export PNGs
for lyr in lyrVec:
    # Set the name for out kml file
    lyrName = ap.Describe(lyr).name
    outKML = outkmlDir+lyrName[:-4]+".kmz"
    arcpy.LayerToKML_conversion(lyr, outKML)

mxd.save()

print "Processing Complete"



##END##
