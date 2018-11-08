# -*- coding: utf-8 -*-
"""
___________________________________________
Author: Chris Zarzar
Created: 03-24-16
Contact: chriszarzar@gmail.com

NOTES: This script extracts multiband raster information from
a .tif raster and  will apply a given calibration equation to
all pixels in the raster. 

-----
EDITED: Chris Zarzar 24-Mar-16
Created program. Worked on hardcoding blueprint of the script

EDITED: Chris Zarzar 11-Apr-16
Worked on setting up the script for automation
Set up the script to look through a raster directory and perform
given operations on files with a .tif extension.

EDITED: Chris Zarzar 12-Apr-16
Fixed the looping issue with the script. I was also able
to get the composite of the files together to work.
Because I fixed that, I commented out all the individually
saved layers because I realized that I could save a lot of
computer space by combining the rasters together with the
raster composite tool.

EDITED: Chris Zarzar 11-May-16
Adjust the file paths to adjust a single image I will need.

EDITED: Chris Zarzar 29-Aug-16
Fixed order of operations in correction
was missing a parenthses before the Exp poriton of the script

EDITED: Chris Zarzar 29-Sep-16
Adjusted the script to run on the resampled imagery.
Fixed issue with compositing the rasters back together,
I simply had to put all the bands I am compositing together 
in a long quote together, not seperate them. 
Also I made the script simpler to use for the future
by changing how the rasDir, outDir, and tempDir 
are used in the script. So now you just have 
to change those three initial variables.
Added try statement so that overwrite option
can be used.
____________________________________________


"""
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = False

# Set environment settings
#env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\"

# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\resampledCIR_05\\"
tempDir =  "E:\\CIR_UAS_Imagery\\resampledCIR_05\\temp_dntorad\\"
outDir = "E:\\CIR_UAS_Imagery\\resampledCIR_05\\dntorad\\"

#List the documents in that raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up loop
for inRas in fileList:

    #Run correction on files that end in .tif
    if inRas.endswith('.tif'):
        print "Correcting image %s" % inRas

        #Extract the .tif file name for naming purposes
        tifName = os.path.basename(inRas[:-4])

        #Seperate the bands of the multiband raster
        multibandraster = inRas
        desc = arcpy.Describe(multibandraster)
        bands = desc.bandCount
        in_rasters = []
        for band in desc.children:
            bandName = band.name
            in_rasters.append(os.path.join(multibandraster, bandName))

        #Pull out band 1 (green) from the in_raster list and convert it to a regular string variable
        rasBand1 = str(in_rasters[0])

        #Pull out band 2 (red) from the in_raster list and convert it to a regular string variable
        rasBand2 = str(in_rasters[1])

        #Pull out band 3 (nir) from the in_raster list and convert it to a regular string variable
        rasBand3 = str(in_rasters[2])
        try:
            print "Correcting band 1 of imagery"
    
            #Apply the band 1 calibration equation to convert the raster values from DN to Radiance
            outRasB1 = 2773.7*(Exp(0.0168*Raster(rasBand1)))
    
            #Save the corrected band 1 raster
            outRasB1.save(tempDir+tifName+"_B1.tif")
    
            print "Correcting band 2 of imagery"
    
            #Apply the band 2 calibration equation to convert the raster values from DN to Radiance
            outRasB2 = 2247.1*(Exp(0.0171*Raster(rasBand2)))
    
            #Save the corrected band 2 raster
            outRasB2.save(tempDir+tifName+"_B2.tif")
    
            print "Correcting band 3 of imagery"
    
            #Apply the band 3 calibration equation to convert the raster values from DN to Radiance
            outRasB3 = 2501.7*(Exp(0.0182*Raster(rasBand3)))
                
            #Save the corrected band 3 raster
            outRasB3.save(tempDir+tifName+"_B3.tif")
    
            #Combine the rasters back into a multiband raster (Not currently working)
            arcpy.CompositeBands_management(""+tempDir+tifName+"_B1.tif;"+tempDir+tifName+"_B2.tif;"+tempDir+tifName+"_B3.tif",""+outDir+tifName+".tif")
            
            print "Correction complete for image %s" % inRas  
              
        except:        
            if "ERROR 000725" in arcpy.GetMessages(2):
                print "%s exists and overwrite turned off." %(os.path.basename(fname))
            else: 
                arcpy.GetMessages(1)                
                arcpy.GetMessages(2)
                
print "Program complete"
#END
