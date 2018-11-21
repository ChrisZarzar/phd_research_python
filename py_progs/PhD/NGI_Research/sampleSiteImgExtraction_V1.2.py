#!/usr/bin/python

"""
Purpose: This script which will buffer
around a point shapefile, then will
convert the buffer to a 3x3 pixel square
then it will extract data from a raster
that overlays the buffered square, and
finally it will organize all of the data
in a table. 

Required Modules:
arcpy (with spatial extension)
astral
csv
dbfpy
math
os
sys


"""

__version__ = "$Revision: 1.2 $"[11:-2]
__date__ = "$Date: 2016/08/18 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 18 August 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 18-Aug-2016
Started writing script which will buffer around a point
shapefile, then will convert the buffer to a 3x3 pixel square
then it will extract data from a raster that overlays the
buffered square, and finally it will organize all of the
data in a table.

EDITED: Chris Zarzar 26-Aug-2016
Added square buffer component of script
Added zonal statistics portion of script


EDITED: Chris Zarzar 29-Aug-2016
Added atmospheric correction portion to script
Added radiance to reflectance conversion to script
Corrected order of operations in atmospheric correction script
Added loop to go through samplesite geodatabases to first part of script
_______________________________________________________


"""
import csv
from dbfpy import dbf
import datetime
import astral
import math
import os
import sys
import arcpy
from arcpy import env
from arcpy.sa import *


# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True

# Set local variables
bufDir = "C:\\cmzarzar\\NGI_UAS\\GIS\\SampleSiteBuffers\\"
gdbDir = "C:\\cmzarzar\\NGI_UAS\\GIS\\Sample_Site_Geodatabases\\"
imgDir = "E:\\LPR_Data\\Original_Canon_CIR_Images\\"
tempDir = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary\\"

siteImgList = open("C:\\cmzarzar\\NGI_UAS\\GIS\\Data_Extraction_Dash\\sampleSites_assocaitedImage_test.csv", 'r')
csvOut = open("C:\\cmzarzar\\NGI_UAS\\GIS\\Data_Extraction_Dash\\site_img_extraction.csv", 'w')



##---------------------------------------------------------------------------
##START FIRST PART OF SCRIPT: BUFFER AND SQUARE BUFFER AROUND SAMPLE SITES
##---------------------------------------------------------------------------

# List the geodatabases 
gdbs = ["SBA_December_2014.gdb", "SBA_March_2015.gdb", "SBA_May_2015.gdb", "SBA_August_2015.gdb", "SBA_December_2015.gdb"]

#Loop through all the geodatabases in this list and buffer each feature in the geodatabases
for gdb in gdbs:
        print "Creating sample site buffers for %s" %(gdb)
        # Set environment settings
        env.workspace = os.path.join(gdbDir, gdb)

        # List features in the working geodatabase
        fcList = arcpy.ListFeatureClasses()

        # Loop through feature list and buffer each feature
        for fc in fcList:
                arcpy.Buffer_analysis(fc,bufDir+fc+"_buffer.shp","2 Inches")
                arcpy.FeatureEnvelopeToPolygon_management(bufDir+fc+"_buffer.shp", bufDir+fc+"_squareBuffer.shp")
	

##---------------------------------------------------------------------------
##SECOND PART OF SCRIPT: IMAGE EXTRACTION
##---------------------------------------------------------------------------

# Read through first line of sampleSites_assocaitedImage_ALL CSV file
count = 0
for row in siteImgList:
        # Split the row to seperate the columns into a list
        columns = row.split(',')
        # Assign the columns I will need
        siteNum = columns[0]
        siteLat = columns[1]
        siteLon = columns[2]
        siteRas = columns[3]
        # Check whether the row is at the header line, if it is then start the next iteration on the second row
        if siteNum == "Site_Num":
                continue
        if siteRas == "NoData":
                continue
        # Set up list that I will use to write to final output csv
        outList = [siteNum,siteLat,siteLon]

        # Extract the band information from the working image
        multibandraster = "%s\\%s" %(imgDir,siteRas)
        desc = arcpy.Describe(multibandraster)
        bands = desc.bandCount
        in_rasters = []

        # Create a list of the image name with each band I will need
        for band in desc.children:
            bandName = band.name
            in_rasters.append(os.path.join(multibandraster, bandName))

        # Set up the variables I will need for the zonal statistics         
        zoneField = "Site_Num"
        nullData = "DATA" 
        statsType = "MEAN"
        bufFeat = bufDir+ "\\Site_Num_"+siteNum+"_squareBuffer.shp"

        # Write the header line for the final output CSV file if count equals zero, otherwise skip it
        if count == 0:
                line = ["Site","Lat","Lon","BV_Band1","BV_Band2","BV_Band3","R_Band1","R_Band2","R_Band3","Rrs_Band1","Rrs_Band2","Rrs_Band3"]
                # Convert list to a string that can be written to the csv file
                lineStr = ','.join(line)
                csvOut.write(lineStr+"\n")

            
        try: 
                print "Trying to run Zonal Statistics"
                #Set up loop to extract data for image band
                count2 = 0
                for ras in in_rasters:
                        if "Band_4" in ras:
                                continue

                        count2 += 1
                        
                        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
                        ras = str(ras)
                        #extract only the raster band so that the raster number and band information can be attached with the table.
                        bandName = os.path.basename(ras)
                        bandNum = bandName[5]
                        #Setup the output table so a new one will be created for each loop
                        outTable = "%s\\%s_%s.dbf" %(tempDir, siteNum, bandName)
                        # Execute ZonalStatisticsAsTable
                        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(bufFeat, zoneField, ras, outTable, nullData, statsType)
                        print "Zonal Statisics for %s %s successful" %(siteNum, ras)

                        # Convert temp dbf file to csv
                        print "Converting Zonal Statistics table to csv format"
                        csv_fn = outTable[:-4]+ ".csv"
                        with open(csv_fn,'wb') as csvfile:
                            in_db = dbf.Dbf(outTable)
                            out_csv = csv.writer(csvfile)
                            names = []
                            for field in in_db.header.fields:
                                names.append(field.name)
                            out_csv.writerow(names)
                            for rec in in_db:
                                out_csv.writerow(rec.fieldData)
                            in_db.close()        


                        # Combine objects extracted from sampleSites_assocaitedImage_ALL.csv and out_csv then add all to final output csv
                        print "Writing extracted data to output list"
                        with open(csv_fn, 'rb') as csvfile:
                                tempCSV = csv.DictReader(csvfile, delimiter = ',')
                                for row in tempCSV:
                                        # Assign the column for mean value I will need
                                        meanVal = row['MEAN']
                                        # Add each mean value extract from each band to the outList
                                        outList.extend([meanVal])

                        # Run atmospheric correction calculation on mean zonal statistics value for each band and store in variable for later use
                        if count2 == 1:
                                print "Correcting for Band 1"
                                radBand1 = 2773.7*(Exp(0.0168*float(meanVal)))
                                                      
                        elif count2 == 2:
                                print "Correcting for Band 2"
                                radBand2 = 2247.1*(Exp(0.0171*float(meanVal)))
                                                      
                        elif count2 == 3:
                                print "Correcting for Band 3"
                                radBand3 = 2501.7*(Exp(0.0182*float(meanVal)))

                        # Calculate reflectance of the mean zonal statistics value for each band and store in variable for later use        
                        with open('C:\\cmzarzar\\NGI_UAS\\reflectanceCalculation\\nova_datetime.csv','rb') as csvfile:
                                csvread = csv.DictReader(csvfile, delimiter = ',')
                                for row in csvread:
                                        if row['Raster'] == os.path.basename(multibandraster):
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
                                                with open('C:\\cmzarzar\\NGI_UAS\\reflectanceCalculation\\earthsunDistance.csv','rb') as csvfile:
                                                        csvread = csv.DictReader(csvfile, delimiter = ',')
                                                        for esrow in csvread:
                                                                if esrow['DOY'] == str(dayNum):
                                                                        esDis = esrow['d']
                                                                        print "E-S distance is %s" % esDis
                                                                        esDis = float(esDis)

                                                #Assign the exoatmospheric solar spectral irradiance for each band
                                                EsunB1 = 1.311783056
                                                EsunB2 = 1.591481747
                                                EsunB3 = 1.489833873

                                                if count2 == 1:
                                                        print "Converting band 1 of imagery"
                                                        #Calculate reflectance for band 1
                                                        refBand1 = ((math.pi*((radBand1)*(10**-3))*(esDis*esDis))/(EsunB1*(math.sin(solElev*(math.pi/180)))))

                                                elif count2 == 2:
                                                        print "Converting band 2 of imagery"
                                                        #Calculate reflectance for band 2
                                                        refBand2 = ((math.pi*((radBand2)*(10**-3))*(esDis*esDis))/(EsunB2*(math.sin(solElev*(math.pi/180)))))

                                                elif count2 == 3:
                                                        print "Converting band 3 of imagery"
                                                        #Calculate reflectance for band 3
                                                        refBand3 = ((math.pi*((radBand3)*(10**-3))*(esDis*esDis))/(EsunB3*(math.sin(solElev*(math.pi/180)))))
                                
                # Convert list to a string that can be written to the csv file
                outList.extend([str(radBand1), str(radBand2), str(radBand3), str(refBand1), str(refBand2), str(refBand3)])
                outStr = ','.join(outList)           
                csvOut.write(outStr+"\n")
                print "SUCCESS" 
        except:
                print "UNSUCCESSFUL for %s" %(siteNum)
                pass

        count += 1

         
siteImgList.close()
csvOut.close()




#END
