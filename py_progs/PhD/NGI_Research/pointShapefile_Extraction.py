#!/usr/bin/python

"""
Purpose: This script will extract classification 
sample information from point shapefiles created in Arc



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/11/09 11:17:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 09 Novemeber 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 09-Nov-2016

Adopted the NorthFarmImgExtract_V1 to create the script
Script is set up so that it will loop through each image in
the directory and will extract shapefile data for each of
those image. It will store that information in a csv 
specific to each image.

***ISSUE FOUND ON 12-8-16:
    In the CSV, it keeps inputting that the Land samples use the Aquatics_class.shp
    to extract the data, but then the fname output in the script realtime
    output says it is using Land_Class.shp and is working appropriately. I 
    cannot figuru out the reason why it is incorrectly naming in the CSV, but
    I cross checked a bunch of the points with the csv output from the extraction 
    and all is correct. There were some inconsistencies between the FID and 
    the ID of the land and water samples because I adjusted a few of those, 
    but besides that everything checks out. So the land samples did use the correct 
    Land_Class.shp file. Just some weird naming glitch in the script I guess. 
    Ill leave that to figure out another time, I am going to many 
    adjust the csv now.

EDITED: Chris Zarzar 10-Mar-2017: Adjusted script so that it can selectively
work through certain dates to extract from the relative points samples. 

EDITED: Chris Zarzar 11-Mar-2017: Changed it to list files raster than os.walk() directories
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
import sys
from dbfpy import dbf
import arcpy
#from arcpy import env
#from arcpy.sa import *
#sys.stdout = open("C:\\Users\\chris\\OneDrive\\Desktop\\Research\\CIR_UAS_Imagery\\resampledCIR_25_Mosaics\\outPut.txt", "w")

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Allow overwriting yes (True) or no (False)
arcpy.env.overwriteOutput = True

# Set environment settings
# env.workspace = "C:\\cmzarzar\\NGI_UAS\\GIS\\Temporary"

# Set local variables
shpDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\NGI_UAS\\GIS\\classification_shapefiles\\"
imgDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\CIR_UAS_Imagery\\resampledCIR_25_Mosaics\\"
tempDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\NGI_UAS\\GIS\\Temporary\\"

## DECEMBER 2015 ##
## List the documents in that raster directory
dirList = os.listdir(imgDir)
## List the files found in dirList with their full pathname
fileList = [imgDir+"\\"+filename for filename in dirList]
for fname in fileList:                                 
    if fname.endswith(".tif"):
        if "dec2014" in fname:                    
            count = 0
            imgName = os.path.basename(fname[:-4])
            print "Working raster is %s" %(imgName)
            csvOut = open(imgDir+imgName+".csv", 'w')
            # Add the header line to the new CSV file if it is the first isntance of zonal staitstics on this image
            if count == 0:
                line = ["Site","Class","Image","Shapefile","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                # Convert list to a string that can be written to the csv file
                lineStr = ','.join(line)
                csvOut.write(lineStr+"\n")
                count += 1
           # Extract the band information from the working image
            multibandraster = fname
            desc = arcpy.Describe(multibandraster)
            bands = desc.bandCount
            in_rasters = [] 
            # Create a list of the image name with each band I will need
            for band in desc.children:
                bandName = band.name
                in_rasters.append(os.path.join(multibandraster, bandName))
            ## Set up zonal statistics loop        
            dirList2 = os.listdir(shpDir)
            ## List the files found in dirList with their full pathname
            fileList2 = [shpDir+"\\"+filename for filename in dirList2]  
            for fname2 in fileList2:
                if fname2.endswith(".shp"):
                    print "Setting up shapefile and write lists"
                    if "Land_Class_300_dec2014" in fname2:
                        print fname2
                        shpName = os.path.basename(fname2[:-4])
                        #Start the output list that I will write to the csv file
                        Class = "Land"                            
                        ClassList = []
                        imgList = []
                        meanList_B1 = []
                        meanList_B2 = []
                        meanList_B3 = []
                        siteList = []
                        shpList = []
                        shpList = []      
              
                    elif "Water_Class_300_dec2014" in fname2:
                        print fname2
                        shpName = os.path.basename(fname2[:-4])
                        #Start the output list that I will write to the csv file
                        Class = "Water"
                        ClassList = []
                        imgList = []
                        meanList_B1 = []
                        meanList_B2 = []
                        meanList_B3 = []
                        siteList = []
                        shpList = []
                        
                    elif "Aquatics_Class_300_dec2014" in fname2:
                        print fname2
                        shpName = os.path.basename(fname2[:-4])
                        #Start the output list that I will write to the csv file
                        Class = "Aquatics"                            
                        ClassList = []
                        imgList = []
                        meanList_B1 = []
                        meanList_B2 = []
                        meanList_B3 = []
                        siteList = []
                        shpList = []
                        
                    else: 
                        continue

                    
                    count1 = 0

                    # Set up the variables I will need for the zonal statistics         
                    zoneField = "Id"
                    nullData = "" 
                    statsType = "ALL"

                    try:                          
                        print "Trying to run Zonal Statistics"
                        
                        #Set up lists to store values
                        for ras in in_rasters:
                            if "Band_4" in ras:
                                continue
                         
                            #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
                            ras = str(ras)
                            #extract only the raster band so that the raster number and band information can be attached with the table.
                            band = os.path.basename(ras)
                            bandNum = band[5]
                            
                            #Setup the output table so a new one will be created for each loop
                            outTable = "%s\\%s_%s.dbf" %(tempDir, imgName, band)
                            
                            # Execute ZonalStatisticsAsTable
                            outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(fname2, zoneField, ras, outTable, nullData, statsType)
                            print "Zonal Statisics for %s %s successful" %(shpName, ras)
                               
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
                            # Gather the mean band value extract for each band and add to the site output csv
                            print "Writing extracted data to output list"
                            with open(csv_fn, 'rb') as csvfile:
                                tempCSV = csv.DictReader(csvfile, delimiter = ',')
                                for row in tempCSV:
                                    # Assign the column for mean values for band 1
                                    if bandNum == '1':   
                                        meanVal_B1 = row['MEAN']
                                        siteId = row['ID']
                                        meanList_B1.append(meanVal_B1)
                                        siteList.append(siteId)                                               
                                        ClassList.append(Class)
                                        imgList.append(imgName)
                                        shpList.append(shpName)
                                    elif bandNum == '2':   
                                        meanVal_B2 = row['MEAN']
                                        meanList_B2.append(meanVal_B2)
                                    elif bandNum == '3':   
                                        meanVal_B3 = row['MEAN']
                                        meanList_B3.append(meanVal_B3)
                                    # Add each mean value extract from each band to the outList
                        for n in zip(siteList,ClassList,imgList,shpList,meanList_B1,meanList_B2,meanList_B3):
                            outStr = (str(n[0])+","+str(n[1])+","+str(n[2])+","+str(n[3])+","+str(n[4])+","+str(n[5])+","+str(n[6]))          
                            csvOut.write(outStr+"\n")
                        print "SUCCESS for %s" %(imgName) 
                    except:
                         print "UNSUCCESSFUL for %s" %(imgName)
                         break
                    count1 += 1
            csvOut.close()
"""
## THIS WAS THE OLD METHOD I USED

## MAY 2015 ##
for dirName, subdirList, fileList in os.walk(imgDir):
    for fname in fileList:                                 
        if fname.endswith(".tif"):
            if "may2015" in fname:                    
                count = 0
                imgName = fname[:-4]
                csvOut = open(dirName+"\\"+imgName+".csv", 'w')
               # Extract the band information from the working image
                multibandraster = "%s\\%s" %(dirName,fname)
                desc = arcpy.Describe(multibandraster)
                bands = desc.bandCount
                in_rasters = [] 
                # Create a list of the image name with each band I will need
                for band in desc.children:
                    bandName = band.name
                    in_rasters.append(os.path.join(multibandraster, bandName))

                for dirName2, subdirList2, fileList2 in os.walk(shpDir):
                    for fname2 in fileList2:
                        if fname2.endswith(".shp"):
                            if "Land_Class_300_may2015" in fname2:
                                print fname2
                                shpName = fname2
                                #Start the output list that I will write to the csv file
                                Class = 'Land'                            
                                ClassList = []
                                imgList = []
                                meanList_B1 = []
                                meanList_B2 = []
                                meanList_B3 = []
                                siteList = []
                                shpList = []
                                shpList = []      
                      
                            if "Water_Class_300_may2015" in fname2:
                                print fname2
                                shpName = fname2
                                #Start the output list that I will write to the csv file
                                Class = 'Water'
                                ClassList = []
                                imgList = []
                                meanList_B1 = []
                                meanList_B2 = []
                                meanList_B3 = []
                                siteList = []
                                shpList = []
                                
                            if "Aquatics_Class_300_may2015" in fname2:
                                print fname2
                                shpName = fname2
                                #Start the output list that I will write to the csv file
                                Class = 'Aquatics'                            
                                ClassList = []
                                imgList = []
                                meanList_B1 = []
                                meanList_B2 = []
                                meanList_B3 = []
                                siteList = []

                            
                            count1 = 0

                            # Set up the variables I will need for the zonal statistics         
                            zoneField = "Id"
                            nullData = "DATA" 
                            statsType = "ALL"

                            try:                          
                                print "Trying to run Zonal Statistics"
                                
                                #Set up loop to extract data for image band
                                countRas = 0
                                #Set up lists to store values
                                for ras in in_rasters:
                                    countRas += 1
                                    if "Band_4" in ras:
                                        continue
                                 
                                    #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
                                    ras = str(ras)
                                    #extract only the raster band so that the raster number and band information can be attached with the table.
                                    band = os.path.basename(ras)
                                    bandNum = band[5]
                                    
                                    #Setup the output table so a new one will be created for each loop
                                    outTable = "%s\\%s_%s.dbf" %(tempDir, imgName, band)
                                    
                                    # Execute ZonalStatisticsAsTable
                                    outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(dirName2+"\\"+fname2, zoneField, ras, outTable, nullData, statsType)
                                    print "Zonal Statisics for %s %s successful" %(shpName, ras)
                                       
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
                                    if count == 0:
                                        line = ["Site","Class","Image","Shapefile","Avg_BV_Band1","Avg_BV_Band2","Avg_BV_Band3"]
                                        # Convert list to a string that can be written to the csv file
                                        lineStr = ','.join(line)
                                        csvOut.write(lineStr+"\n")
                                        count += 1
                                    # Gather the mean band value extract for each band and add to the site output csv
                                    print "Writing extracted data to output list"
                                    with open(csv_fn, 'rb') as csvfile:
                                        tempCSV = csv.DictReader(csvfile, delimiter = ',')
                                        for row in tempCSV:
                                            # Assign the column for mean values for band 1
                                            if countRas == 1:   
                                                meanVal_B1 = row['MEAN']
                                                siteId = row['ID']
                                                meanList_B1.append(meanVal_B1)
                                                siteList.append(siteId)                                               
                                                ClassList.append(Class)
                                                imgList.append(imgName)
                                                shpList.append(shpName)
                                            elif countRas == 2:   
                                                meanVal_B2 = row['MEAN']
                                                meanList_B2.append(meanVal_B2)
                                            elif countRas == 3:   
                                                meanVal_B3 = row['MEAN']
                                                meanList_B3.append(meanVal_B3)
                                            # Add each mean value extract from each band to the outList
                                for n in zip(siteList,ClassList,imgList,shpList,meanList_B1,meanList_B2,meanList_B3):
                                    outStr = (str(n[0])+","+str(n[1])+","+str(n[2])+","+str(n[3])+","+str(n[4])+","+str(n[5])+","+str(n[6]))          
                                    csvOut.write(outStr+"\n")
                                print "SUCCESS for %s" %(imgName) 
                            except:
                                 print "UNSUCCESSFUL for %s" %(imgName)
                                 pass
                            count1 += 1
                csvOut.close()         

     
"""
print "program complete"
