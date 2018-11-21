#!/usr/bin/python

"""
Purpose: This script extracts multiband raster information from
a .tif raster and  will apply a series of equations based on the
date and time information provided in the naming of the file
to convert values from radiance to reflectance


"""

__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/05/02 10:22:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
_______________________________________
Author: Chris Zarzar
Created: 05-02-2016
Contact: chriszarzar@gmail.com


----History----

EDITED: Chris Zarzar 05-02-16
Created program. 

EDITED: Chris Zarzar 05-03-16
Worked on finalizing program. Had to comment out and put new save destinations for the testing of the script.
Inserted print statement throughout to assess the progress of the program.

EDITED: Chris Zarzar 05-25-16
Fixed up the program to adjust the calculations so that units will match what they should with
the exoatmospheric calculated values.

EDITED: Chris Zarzar 29-Sep-16
Adjusted the script to run on the resampled imagery.
Fixed issue with compositing the rasters back together,
I simply had to put all the bands I am compositing together 
in a long quote together, not seperate them. 
Also I made the script simpler to use for the future
by changing how the rasDir, tempDir, outDir, and geoDir 
are used in the script. So now you just have 
to change those three initial variables.
Added try statement so that overwrite option
can be used.


EDITED: Chris Zarzar 07-Oct-2016
found out that I was off with my units. I simply need to change  
my exoatmospheric using to:
    EsunB1 = 1311.783056
    EsunB2 = 1591.481747
    EsunB3 = 1489.833873
From: 
    EsunB1 = 1.311783056
    EsunB2 = 1.591481747
    EsunB3 = 1.489833873 
____________________________________________


"""
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
arcpy.env.overwriteOutput = False

# Set environment settings
#env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

# Set up the variables
rasDir = "E:\\CIR_UAS_Imagery\\resampledCIR_25\\dntorad\\"
tempDir =  "E:\\CIR_UAS_Imagery\\resampledCIR_25\\temp_radtoref\\"
outDir = "E:\\CIR_UAS_Imagery\\resampledCIR_25\\radtoref\\"
geoDir = "C:\\cmzarzar\\NGI_UAS\\reflectanceCalculation\\"

#List the documents in that raster directory
dirList = os.listdir(rasDir)

#List the files found in dirList with their full pathname
fileList = [rasDir+"\\"+filename for filename in dirList]

#Set up loop
for inRas in fileList:

    #Run correction on files that end in .tif
    if inRas.endswith('.tif'):
        print "Converting image %s" % inRas

        #Extract the .tif file name for naming purposes
        tifName = os.path.basename(inRas[:-4])
        print "The raster being worked on is %s" % tifName

        #Extract time information if associated with current raster file name
        with open(geoDir+'nova_datetime.csv','rb') as csvfile:
            csvread = csv.DictReader(csvfile, delimiter = ',')
            for row in csvread:
                    print "Calculating reflectance for %s" % row['Raster']
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
                    with open(geoDir+'earthsunDistance.csv','rb') as csvfile:
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
                                   
                    try:
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
                        
                    except:        
                        if "ERROR 000725" in arcpy.GetMessages(2):
                            print "%s exists and overwrite turned off." %(os.path.basename(fname))
                        else: 
                            arcpy.GetMessages(1)                
                            arcpy.GetMessages(2)

print "Program complete"
#END


