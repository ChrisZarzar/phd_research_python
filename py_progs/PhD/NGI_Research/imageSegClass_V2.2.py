#!/usr/bin/python

"""
Purpose: This script will segment an
image based on the color and shape of
pixels and features in the image
"""

__version__ = "$Revision: 2.2 $"[11:-2]
__date__ = "$Date: 2016/09/15 17:33:00 $"[7:-2]
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

EDITED: Chris Zarzar 15-Sep-2016
Added Maximum likelihood classifier to script. Tested 
script on Aug2015_SmallSubset
Adjusted to use the regular MLC where I had to create
a sig file. Could not get train classifier to work

EDITED: Chris Zarzar 19-Sep-2016
Added Maximum likelihood classifiers for the 
new test segments that did the best. 

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



##
###-----Segmentation-------
##startTime = time.time()
### Set local variables
##inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
##spectral_detail = "18.5"
##spatial_detail = "17"
##min_segment_size = ""
##band_indexes = "3 2 1"
##
##
##
### Execute 
##seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
##                              min_segment_size, min_segment_size)
##
### Save the output 
##segRas = seg_raster.save("C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_ArcSeg.tif")
##endTime = time.time()
##runTime = endTime - startTime
##
###-----End Segmentation-------


#-----Classification-------
# Set local variables
inRaster = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test2.tif.tif"
sigFile = "C:\\cmzarzar\\NGI_UAS\\GIS\\trainingPolygons\\aug2015_training_samples2.gsg"
probThreshold = "0.0"
aPrioriWeight = "EQUAL"
aPrioriFile = ""
outConfidence = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_2_confidence.tif"


# Execute 
mlcOut = MLClassify(inRaster, sigFile, probThreshold, aPrioriWeight, 
                    aPrioriFile, outConfidence) 

# Save the output 
mlcOut.save("C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_2.tif")

print "PROCESSING COMPLETE"

#-----Classification-------
# Set local variables
inRaster = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test3.tif.tif"
sigFile = "C:\\cmzarzar\\NGI_UAS\\GIS\\trainingPolygons\\aug2015_training_samples3.gsg"
probThreshold = "0.0"
aPrioriWeight = "EQUAL"
aPrioriFile = ""
outConfidence = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_3_confidence.tif"


# Execute 
mlcOut = MLClassify(inRaster, sigFile, probThreshold, aPrioriWeight, 
                    aPrioriFile, outConfidence) 

# Save the output 
mlcOut.save("C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_3.tif")

print "PROCESSING COMPLETE"


#-----Classification-------
# Set local variables
inRaster = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test6.tif.tif"
sigFile = "C:\\cmzarzar\\NGI_UAS\\GIS\\trainingPolygons\\aug2015_training_samples6.gsg"
probThreshold = "0.0"
aPrioriWeight = "EQUAL"
aPrioriFile = ""
outConfidence = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_6_confidence.tif"


# Execute 
mlcOut = MLClassify(inRaster, sigFile, probThreshold, aPrioriWeight, 
                    aPrioriFile, outConfidence) 

# Save the output 
mlcOut.save("C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_6.tif")

print "PROCESSING COMPLETE"


##***BELOW IS ANOTHER WAY THE CLASSIFICATION CAN BE DONE
#
#
#inSegRaster = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_ArcSeg.tif"
#train_features = "C:\\cmzarzar\\NGI_UAS\\GIS\\trainingPolygons\\arc_training_samples.gdb\\Aug2015_arc_train_samples"
#def_file = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC2.ecd"
#attributes = "COLOR;COUNT;COMPACTNESS;RECTANGULARITY" #MEAN;STD; can be used if an original .tif is provided
#in_additional_raster = ""
#
#
## Train the maximum likelihood classifer
#TrainMaximumLikelihoodClassifier(inSegRaster, train_features, def_file, 
#                                 in_additional_raster, attributes)
#
#
#
## Classify the image
#classifiedraster = ClassifyRaster(inSegRaster, def_file, "")
#
##save output
#classifiedraster.save("C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\classifications\\Aug2015_MLC_2.tif")

#-----End Classification-------
####END
