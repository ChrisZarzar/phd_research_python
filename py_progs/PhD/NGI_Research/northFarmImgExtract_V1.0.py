#!/usr/bin/python

"""
Purpose: This script will extract data from a raster
that overlays the calibration panels from the
North Farm experiment. 



"""

__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/09/06 11:17:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 06 September 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 06-Sep-2016


EDITED: Chris Zarzar 16-Sep-2016
Continued work on the script
Realized that I would also have to split up the analysis
based on the percentage of the panel

EDITED: Chris Zarzar 17-Oct-2016
Setting up the script to work 
through the MicaSense images and polygons


_______________________________________________________


"""

##EXPECTED STEPS TO WRITING THIS SCRIPT:
#1. Loop through each of the shpaefiles I created for the extraction
#2. Pull the image name from the shapefile name and look through sorted imagery to find matching raster
#3. Loop through the bands of the matching raster and run zonal statistics
#4. Convert each dbf zonal statistics table created to csv
#5. Combine csv files for each site.
#6. Save combined csv file to a each appropriate altitude folder based on the input path of the raster image
#7. Can use the os.replace command to change the output location of the csv files based on input raster
#8. After entire script runs, go through each of the altitude directories and combine the csv files in each dir
#9. Run statistical testing
#10. Incorporate results into module 1. 

import os
import csv
from dbfpy import dbf
import arcpy
from arcpy import env
from arcpy.sa import *


# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = False

# Set environment settings
# env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

# Set local variables
shpDir = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\Micasense_Image_Extract\\"
imgDir = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\micasenseOrganized\\"
tempDir = "F:\\NGI_UAS\\GIS\\Temporary"

for dirName, subdirList, fileList in os.walk(shpDir):
    for fname in fileList:
        count = 0
        if fname.endswith(".shp"):
            for dirName2, subdirList2, fileList2 in os.walk(imgDir):
                for fname2 in fileList2:
                    if fname2.endswith(".JPG"):
                        imgName = "img"+fname2[4:8]
                        shpName = "img"+fname[3:7]
                        shpTarp = fname[0:13]
                        if imgName == shpName:
                            count1 = 0
                            # Extract the band information from the working image
                            multibandraster = "%s\\%s" %(dirName2,fname2)
                            desc = arcpy.Describe(multibandraster)
                            bands = desc.bandCount
                            in_rasters = []                                                
                            
                            
                            # Create a list of the image name with each band I will need
                            for band in desc.children:
                                bandName = band.name
                                in_rasters.append(os.path.join(multibandraster, bandName))
    
                            # Set up the variables I will need for the zonal statistics         
                            zoneField = "Id"
                            nullData = "DATA" 
                            statsType = "ALL"
                            zoneExt = dirName+"\\"+fname
    
                                
                            try:                          
                                print "Trying to run Zonal Statistics"
                                
                                # Create the csv file for this image 
                                csvOut = open(dirName+"\\"+shpTarp+".csv", 'w')
                                
                                #Start the output list that I will write to the csv file
                                outList = [imgName]  
                                
                                #Set up loop to extract data for image band
                                for ras in in_rasters:
                                    if "Band_4" in ras:
                                        continue
                                 
                                    #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
                                    ras = str(ras)
                                    #extract only the raster band so that the raster number and band information can be attached with the table.
                                    bandName = os.path.basename(ras)
                                    bandNum = bandName[5]
                                    
                                    #Setup the output table so a new one will be created for each loop
                                    outTable = "%s\\%s_%s.dbf" %(tempDir, shpTarp, bandName)
                                    
                                    # Execute ZonalStatisticsAsTable
                                    outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(dirName+"\\"+fname, zoneField, ras, outTable, nullData, statsType)
                                    print "Zonal Statisics for %s %s successful" %(shpTarp, ras)
    
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
                                    
                                    # Add the header line to the new CSV file if it is the first isntance of zonal staitstics on this image
                                    if count1 == 0:
                                        line = ["imgNum","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                                        # Convert list to a string that can be written to the csv file
                                        lineStr = ','.join(line)
                                        csvOut.write(lineStr+"\n")
                                        count1 += 1
                                    
                                    # Gather the mean band value extract for each band and add to the site output csv
                                    print "Writing extracted data to output list"
                                    with open(csv_fn, 'rb') as csvfile:
                                        tempCSV = csv.DictReader(csvfile, delimiter = ',')
                                        for row in tempCSV:
                                            # Assign the column for mean value I will need
                                            meanVal = row['MEAN']
                                            # Add each mean value extract from each band to the outList
                                            outList.extend([meanVal])
                                outStr = ','.join(outList)           
                                csvOut.write(outStr+"\n")
                                print "SUCCESS" 
                                csvOut.close()
                            except:
                                 print "UNSUCCESSFUL for %s" %(shpTarp)
                                 pass
            

        
#Set up loop to combine the files in the altitude directory into a single altitude based csv file
for dirName, subdirList, fileList in os.walk(shpDir):
    csvOut06 = open(dirName+"\\Combined06%.csv", 'w') 
    csvOut22 = open(dirName+"\\Combined22%.csv", 'w')  
    csvOut44 = open(dirName+"\\Combined44%.csv", 'w') 
    count06 = 0
    count22 = 0
    count44 = 0
    for fname in fileList:
        if fname.endswith(".csv"):
            try:
                if "_06%" in fname:
                    # Add the header line to the new CSV file if it is the first isntance of zonal staitstics on this image                
                    if count06 == 0:
                        line = ["imgNum","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                        # Convert list to a string that can be written to the csv file
                        lineStr = ','.join(line)
                        csvOut06.write(lineStr+"\n")
                        count06 += 1          
                    #Open the csv files in the dirName and  the information to the altitude csv file
                    with open(dirName+"\\"+fname, 'r') as csvFile1: 
                        csvFile1.next() #skip the header row     
                        for row in csvFile1:
                            csvOut06.write(row) # Write data to output csv file
                 
                    
                if "_22%" in fname:
                    # Add the header line to the new CSV file if it is the first isntance of zonal staitstics on this image
                    if count22 == 0:
                        line = ["imgNum","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                        # Convert list to a string that can be written to the csv file
                        lineStr = ','.join(line)
                        csvOut22.write(lineStr+"\n")
                        count22 += 1            
                    #Open the csv files in the dirName and  the information to the altitude csv file
                    with open(dirName+"\\"+fname, 'r') as csvFile2: 
                        csvFile2.next() #skip the header row                
                        for row in csvFile2:
                            csvOut22.write(row) # Write data to output csv file
               
                    
                if "_44%" in fname:       
                    # Add the header line to the new CSV file if it is the first isntance of zonal staitstics on this image
                    if count44 == 0:
                        line = ["imgNum","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                        # Convert list to a string that can be written to the csv file
                        lineStr = ','.join(line)
                        csvOut44.write(lineStr+"\n")
                        count44 += 1          
                    #Open the csv files in the dirName and  the information to the altitude csv file
                    with open(dirName+"\\"+fname, 'r') as csvFile3: 
                        csvFile3.next() #skip the header row                   
                        for row in csvFile3:
                            csvOut44.write(row) # Write data to output csv file
            except StopIteration:
                pass
                
csvOut06.close()
csvOut22.close()
csvOut44.close()               
#END
