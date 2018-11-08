#!/usr/bin/python

"""
Purpose: This script will segment an
image based on the color and shape of
pixels and features in the image
"""

__version__ = "$Revision: 2.1 $"[11:-2]
__date__ = "$Date: 2016/09/12 12:37:00 $"[7:-2]
__author__ = "Chris Zarzar <chris.zarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 31 August 2016
Contact: chris.zarzar@gmail.com

----History----

CREATED: Chris Zarzar 31-Aug-2016
Chose to start with the Slic segementation function
because the comparison on the webpage appeared to
be most similar to my segments using the Slic
function.

EDITED: Chris Zarzar 12-Sep-2016
Took out all test except for test 8 since that is the one I am going
to use. Added in classification training and
execution as well

_______________________________________________________


"""

import arcpy
from arcpy.sa import *
from arcpy import env
import time


# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Set environment settings
env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True




#-----Segmentation-------
startTime = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015_SmallSubset.tif"
spectral_detail = "18.5"
spatial_detail = "17"
min_segment_size = ""
band_indexes = "3 2 1"
segRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015SmallSub_ArcSeg.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(segRas)
endTime = time.time()
runTime = endTime - startTime


#-----Classification-------
inSegRaster = "c:/test/moncton_seg.tif"
train_features = "c:/test/train.gdb/train_features"
out_definition = "c:/output/moncton_sig.ecd"
in_additional_raster = "c:/moncton.tif"
attributes = "COLOR;MEAN;STD;COUNT;COMPACTNESS;RECTANGULARITY"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute 
TrainMaximumLikelihoodClassifier(inSegRaster, train_features, out_definition, 
                                 in_additional_raster, attributes)



####END
