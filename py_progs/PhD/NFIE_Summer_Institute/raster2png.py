#!/usr/bin/python

"""
Purpose: This script is will
go about creating and exporting
image from the raster I make



"""

__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/06/27 11:34:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 207 June 2016
Contact: chriszarzar@gmail.com

Notes: The script first removes all layers in the
map document provided. It will then add a source layer
simply as a reference layer

----History----

CREATED: Chris Zarzar 27-Jun-2016

EDITED: Chris Zarzar 28-Jun-2016
Was having a lot of trouble getting the layer visibilities
to work correctly and a lot of trouble getting layers to
loop correctly. It seems like having the visibility command
included in a for loop is necessary. 

EDITED: Chris Zarzar 28-Jun-2016
Rewrote entire script to simplify while making more robust
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

#Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\Chris\\Desktop\\groupProject\\"

# Set up variables
env.workspace = path+"workspace\\"
mapDoc = path+"\\imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

rasDir =  path+"postprocessOutput\\rasters\\composites\\"
outlyrDir =  path+"postprocessOutput\\rasters\\layers\\"
outimgDir =  path+"ArcMap_Images\\"

# Source layers that will be used for symbology reference
fldext_srcLyr = mp.Layer(outlyrDir+"fldext_source_stretch.lyr")
wd_srcLyr = mp.Layer(outlyrDir+"wd_source_stretch.lyr")
fv_srcLyr = mp.Layer(outlyrDir+"fv_source_stretch.lyr")
crit_srcLyr = mp.Layer(outlyrDir+"crit_source_stretch.lyr")


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
        ap.MakeRasterLayer_management(ras, tmpLyr)
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
        

#Set up the extent view
viewExtent = wrkLyr.getSelectedExtent()
df.extent = viewExtent
mxd.save()

# Create the vector to loop through
lyrVec = mp.ListLayers(df)

# To be safe, start by hiding all of the layers
for lyr in lyrVec:
    lyr.visible = False
mxd.save()

# Loop through all layers and export PNGs
for lyr in lyrVec:
    lyr.visible = True
    # Set the name for out PNG file
    lyrName = ap.Describe(lyr).name
    outPNG = outimgDir+lyrName[:-4]+".png"
    mp.ExportToPNG(mxd,outPNG,df,640,480,96, True)
    lyr.visible = False

mxd.save()


del mxd, df

try:
    del env.workspace, mapDoc, fldext_srcLyr, wd_srcLyr, fv_srcLyr, cric_srcLyr, rasDir, outlyrDir, outimgDir, refLayer, dirList, rasList, ras, rasName, outLyr, tmpLyr, wrkLyr #Do your cleanup properly

except:

    pass

finally:

    print "Processing Complete"



##END##
