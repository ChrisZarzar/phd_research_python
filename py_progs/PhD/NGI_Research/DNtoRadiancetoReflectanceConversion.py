# -*- coding: utf-8 -*-
"""
___________________________________________
Author: Chris Zarzar
Created: 11-30-16
Contact: chriszarzar@gmail.com

NOTES: This script merges two scripts, DNtoRadianceConversion.py and RadiancetoReflectance.py
This script extracts multiband raster information from
a .tif raster and  will apply a given calibration equation to
all pixels in the raster. It will then take those calculated radiance
values and will create new rasters and calculates the Remote Sensing Reflectance


-----
EDITED: Chris Zarzar 17-Dec-16
Realized that the script was looping through the rasters very wronge
It took so long because it had to work through the file list multiple times 
because it was calculating the reflectance over and over for each row that it worked
through. I wonder if this has implications for the reflectance script I wrote.
Now I wonder if that script calculated reflectance correctly. I am starting to think
that it did not. So may have to redo my reflectance calculations. That could be
why they look so bad. 
ADDED "2" to my geog files so I could run this same script for both the original CIR 
images and for the resampled25 data

____________________________________________


"""
import os
import arcpy
from arcpy import env
from arcpy.sa import *


#Comment out the below once these mosaics are generated. Also, move files from Dec 2015, Dec 2014, and up through 2015-3-19-14-49-43 to a new directory so I can start from where the script originally left off in march.

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True

# Set environment settings
#env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

#
#
## Set up the variables
#rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\"
#tempDir =  "E:\\CIR_UAS_Imagery\\Original_Clipped\\temp_dntorad\\"
#outDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\dntorad\\"
#
##List the documents in that raster directory
#dirList = os.listdir(rasDir)
#
##List the files found in dirList with their full pathname
#fileList = [rasDir+"\\"+filename for filename in dirList]
#
##Set up loop
#for inRas in fileList:
#
#    #Run correction on files that end in .tif
#    if inRas.endswith('.tif'):
#        print "Correcting image %s" % inRas
#
#        #Extract the .tif file name for naming purposes
#        tifName = os.path.basename(inRas[:-4])
#
#        #Seperate the bands of the multiband raster
#        multibandraster = inRas
#        desc = arcpy.Describe(multibandraster)
#        bands = desc.bandCount
#        in_rasters = []
#        for band in desc.children:
#            bandName = band.name
#            in_rasters.append(os.path.join(multibandraster, bandName))
#
#        #Pull out band 1 (green) from the in_raster list and convert it to a regular string variable
#        rasBand1 = str(in_rasters[0])
#
#        #Pull out band 2 (red) from the in_raster list and convert it to a regular string variable
#        rasBand2 = str(in_rasters[1])
#
#        #Pull out band 3 (nir) from the in_raster list and convert it to a regular string variable
#        rasBand3 = str(in_rasters[2])
#        try:
#            print "Correcting band 1 of imagery"
#    
#            #Apply the band 1 calibration equation to convert the raster values from DN to Radiance
#            outRasB1 = 2773.7*(Exp(0.0168*Raster(rasBand1)))
#    
#            #Save the corrected band 1 raster
#            outRasB1.save(tempDir+tifName+"_B1.tif")
#    
#            print "Correcting band 2 of imagery"
#    
#            #Apply the band 2 calibration equation to convert the raster values from DN to Radiance
#            outRasB2 = 2247.1*(Exp(0.0171*Raster(rasBand2)))
#    
#            #Save the corrected band 2 raster
#            outRasB2.save(tempDir+tifName+"_B2.tif")
#    
#            print "Correcting band 3 of imagery"
#    
#            #Apply the band 3 calibration equation to convert the raster values from DN to Radiance
#            outRasB3 = 2501.7*(Exp(0.0182*Raster(rasBand3)))
#                
#            #Save the corrected band 3 raster
#            outRasB3.save(tempDir+tifName+"_B3.tif")
#    
#            #Combine the rasters back into a multiband raster 
#            arcpy.CompositeBands_management(""+tempDir+tifName+"_B1.tif;"+tempDir+tifName+"_B2.tif;"+tempDir+tifName+"_B3.tif",""+outDir+tifName+".tif")
#            
#            print "Correction complete for image %s" % inRas  
#            
#            #Remove the temporary files to save space
#            dirListrm = os.listdir(tempDir)
#            #List the files found in dirList with their full pathname
#            fileListrm = [tempDir+"\\"+filenamerm for filenamerm in dirListrm]
#            for f in fileListrm:
#                os.remove(f)
#            
#        except:        
#            if "ERROR 000725" in arcpy.GetMessages(2):
#                print "%s exists and overwrite turned off." %(os.path.basename(fname))
#            else: 
#                arcpy.GetMessages(1)                
#                arcpy.GetMessages(2)
#
#
#       
#print "Program part 1 complete"
##END

print "Program part 2 begin"
import os
import datetime
import astral
import csv
import math
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True

# Set environment settings
#env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\dntorad\\"
tempDir =  "E:\\CIR_UAS_Imagery\\Original_Clipped\\temp_radtoref\\"
outDir = "E:\\CIR_UAS_Imagery\\Original_Clipped\\radtoref\\"
geoDir = "C:\\cmzarzar\\NGI_UAS\\reflectanceCalculation\\"

#Extract time information if associated with current raster file name
with open(geoDir+'nova_datetime2.csv','rb') as csvfile:
    csvread = csv.DictReader(csvfile, delimiter = ',')
    for row in csvread:
            try:
                Ras = row['Raster']
                inRas = rasDir+Ras
                tifName = os.path.basename(inRas[:-4])
                print "The raster being worked on is %s" % tifName
                
                dateTime = row['DateTime']
                print "The raster being worked on is for date %s" % dateTime
                
                #Set the format for date and time
                DB_TIME_FORMAT = '%m/%d/%Y %H:%M'
    
                #Assign date and time that will be used for solar elevation calculation
                d = datetime.datetime.strptime(dateTime, DB_TIME_FORMAT)
                print "The current date processing is %s" % d
    
                #Calculate solar elevation angle in LPR estuary
                a = astral.Astral()
                solElev = a.solar_elevation(d, 30.20, -89.63)
                print "Solar elevation is %s" % solElev
    
                #Figure out the day of the year based on the given datetime
                dayNum = d.timetuple().tm_yday
                print "Day number from start of year is %s" % dayNum
    
                #Lookup Earth-Sun distance
                with open(geoDir+'earthsunDistance2.csv','rb') as csvfile:
                    csvread = csv.reader(csvfile, delimiter = ',')
                    for esrow in csvread:
                        if esrow[0] == str(dayNum):
                            esDis = esrow[1]
                            print "E-S distance is %s" % esDis
                            esDis = float(esDis)
    
                #Assign the exoatmospheric solar spectral irradiance for each band
                EsunB1 = 1311.783056
                EsunB2 = 1591.481747
                EsunB3 = 1489.833873
    
                 
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
                               
                
                print "Converting band 1 of imagery"

                #Calculate reflectance for band 1
                outRasB1 = (math.pi*(Raster(rasBand1)*(10**-3))*(esDis*esDis))/(EsunB1*(math.sin(solElev*(math.pi/180))))
                
                #Save the converted band 1 raster
                #outRasB1.save("K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B1.tif")
                outRasB1.save(tempDir+tifName+"_B1.tif")

                print "Converting band 2 of imagery"

                #Calculate reflectance for band 2
                outRasB2 = (math.pi*(Raster(rasBand2)*(10**-3))*(esDis*esDis))/(EsunB2*(math.sin(solElev*(math.pi/180))))

                #Save the converted band 2 raster
                #outRasB2.save("K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B2.tif")
                outRasB2.save(tempDir+tifName+"_B2.tif")
                
                print "Converting band 3 of imagery"

                #Calculate reflectance for band 3
                outRasB3 = (math.pi*(Raster(rasBand3)*(10**-3))*(esDis*esDis))/(EsunB3*(math.sin(solElev*(math.pi/180))))
                    
                #Save the converted band 3 raster
                #outRasB3.save("K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B3.tif")
                outRasB3.save(tempDir+tifName+"_B3.tif")
                
                #Combine the rasters back into a multiband raster
                #arcpy.CompositeBands_management("K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B1.tif;K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B2.tif;K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\singleBandRasters\\"+tifName+"_B3.tif","K:\\general\\cmzarzar\\CIR_UAS_Imagery\\correctedImagery\\"+tifName+".tif")
                arcpy.CompositeBands_management(""+tempDir+tifName+"_B1.tif;"+tempDir+tifName+"_B2.tif;"+tempDir+tifName+"_B3.tif",""+outDir+tifName+".tif")               
                print "Correction complete for image %s" % inRas 
                  
                #Remove the temporary files to save space
                dirListrm = os.listdir(tempDir)
                #List the files found in dirList with their full pathname
                fileListrm = [tempDir+"\\"+filenamerm for filenamerm in dirListrm]
                for f in fileListrm:
                    os.remove(f)
            except:        
                if "ERROR 000725" in arcpy.GetMessages(2):
                    print "%s exists and overwrite turned off." %(os.path.basename(fname))
                else: 
                    arcpy.GetMessages(1)                
                    arcpy.GetMessages(2)
                  
                    

print "Program part 2 complete"
#END


print "Final part Complete"



#END