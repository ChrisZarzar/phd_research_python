#!/usr/bin/python

"""
Purpose: This script will segment an
image based on the color and shape of
pixels and features in the image
"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/08/31 12:37:00 $"[7:-2]
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



#-----Test 2-------
startTime2 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "17"
spatial_detail = "10"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test2.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime2 = time.time()
runTime2 = endTime2 - startTime2


#-----Test 3-------
startTime3 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "18"
spatial_detail = "12"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test3.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime3 = time.time()
runTime3 = endTime3 - startTime3


#-----Test 4-------
startTime4 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "7"
spatial_detail = "2"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test4.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime4 = time.time()
runTime4 = endTime4 - startTime4

#-----Test 5-------
startTime5 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "11"
spatial_detail = "11"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test5.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime5 = time.time()
runTime5 = endTime5 - startTime5


#-----Test 6-------
startTime6 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "19"
spatial_detail = "3"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test6.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime6 = time.time()
runTime6 = endTime6 - startTime6


#-----Test 7-------
startTime7 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "18"
spatial_detail = "16"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test7.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime7 = time.time()
runTime7 = endTime7 - startTime7


#-----Test 8-------
startTime8 = time.time()
# Set local variables
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\BVSubsets\\Aug_2015.tif"
spectral_detail = "5"
spatial_detail = "18"
min_segment_size = ""
band_indexes = "3 2 1"
outRas = "C:\\cmzarzar\\NGI_UAS\\surfaceClassification\\arcpyClassifications\\segementation\\Aug2015_test8.tif"


# Execute 
seg_raster = SegmentMeanShift(inRas, spectral_detail, spatial_detail, 
                              min_segment_size, min_segment_size)

# Save the output 
seg_raster.save(outRas)
endTime8 = time.time()
runTime8 = endTime8 - startTime8


####END
