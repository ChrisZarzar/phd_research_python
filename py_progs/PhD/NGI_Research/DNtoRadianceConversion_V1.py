#____________________________________________
#Created by Chris Zarzar 24 March 2016
#Contact: chriszarzar@gmail.com
#-----
#Edited by Chris Zarzar 24 March 2016
#Created program. Worked on hardcoding blueprint of the script
#____________________________________________

#This script uses two textfiles provided by the user to run zonal statistics
#as table on the sites provided and the associated raster image provided.
#This python program has been edited different from zonalStats because it
#changes how the files are named. It makes the names shorter for future
#programming ease.

import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Set environment settings
env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\"

#Set input raster
inRas = "C:\\cmzarzar\\CIR_UAS_Imagery\\test_ras.tif"

#*******Apply Band 1 Regression to Band 1 Raster Layer Data********


#Pull out band 1 layer from the raster
#rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery" **WILL USE THIS WHEN I ITERATE THE PROCESS
multibandraster = inRas
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))

#Pull out band 1 from the in_raster list and convert it to a regular string variable
rasBand1 = str(in_rasters[0])

#Apply the band 1 calibration equation to convert the raster values from DN to Radiance
outRas = 2773.7*Exp(0.0168*Raster(rasBand1))

#Save the newly DN to Radiance converted raster
outRas.save("C:\\cmzarzar\\CIR_UAS_Imagery\\test_ras_Rad.tif")

print "Success"

#END
