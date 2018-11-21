#____________________________________________
#Created by Chris Zarzar 02 December 2015
#-----
#Edited 03 March 2016
#Chris Zarzar: Adjusted the script to set it up for the December 2015 mission
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

# Set local variables
siteDir="C:\\cmzarzar\\NGI_UAS\\GIS\\Calibration_panel_shapefiles"
outDir = "C:\\cmzarzar\\NGI_UAS\\GIS\\Brightness_values_extracted_Dec2015"



#****FOR SITE 149********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_149.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_149.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row



#****FOR SITE 150-151********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_150-151.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_150-151.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row


    
#****FOR SITE 152********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_152.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_152.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

    

#****FOR SITE 153********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_153.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_153.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

    


#****FOR SITE 154-155********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_154-155.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_154-155.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

    

#****FOR SITE 158********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_158.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_158.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

    
#****FOR SITE 161********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_161.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_161.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

    

#****FOR SITE 163********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_163.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_163.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row


    
#****FOR SITE 164********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pySiteList_164.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyTextFiles_December2015\\pyRasList_164.txt"
rasList = [line.rstrip() for line in open(inputfile)]

# Drop the .tif from the raster names in rasList for later use of the names
rasList1 = [line.rstrip(".tif") for line in open(inputfile)]

#This is not an issue now because I am only viewing 1 raster at a time, but it would be idea if I could somehow have this embedded in the loop so that it would step through the first raster listed and go with the associated sites, then load each band, then run the zonal statistics, then new to the next block of sites and the next raster image that corresponds with those. 
rasDir = "C:\\cmzarzar\\CIR_UAS_Imagery"
multibandraster = "%s\\%s" %(rasDir,rasList[0])
desc = arcpy.Describe(multibandraster)
bands = desc.bandCount
in_rasters = []

for band in desc.children:
    bandName = band.name
    in_rasters.append(os.path.join(multibandraster, bandName))
   
# Define zone field to do polygon extraction on
zoneField = "Id"
# Define weather null data will be withheld from calculations ("DATA") or if it will be included ("NODATA")
nullData = "DATA" 
# Define the statistics you want to calculation. Options are "ALL", "MEAN", "MAXIMUM","MINIMUM","MEDIAN", "MAJORITY", "MINORITY", "RANGE", "STD", "SUM", "VARIETY", "MIN_MAX", "MEAN_STD", "MIN_MAX_MEAN"
statsType = "ALL"
#Set up loop to run through all of the sites in the siteList text file
for site in siteList:
    #Set up loop to work through all bands of raster
    for ras in in_rasters:
        #in_rasters has unicode formatting with u' in front of the filename. Convert it to a regular string
        ras = str(ras)
        #extract only the raster band so that the raster number and band information can be attached with the table.
        bandName = os.path.basename(ras)
        #Setup the output table so a new one will be created for each loop
        outTable = "%s\\%s_%s.dbf" %(outDir, site, bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
        siteLoc = site[0:3]
        siteNum = site[3:6]
        calPan = site[7:9]
        bandNum = bandName[5]
        arcpy.AddField_management(outTable,"SiteLoc", "TEXT")
        arcpy.AddField_management(outTable,"SiteNum", "TEXT")
        arcpy.AddField_management(outTable,"CalPanel", "TEXT")
        arcpy.AddField_management(outTable,"Band", "TEXT")
        upCur = arcpy.UpdateCursor(outTable)
        for row in upCur:
            row.SiteLoc = "%s"    % siteLoc
            row.SiteNum  = "%s"    % siteNum
            row.CalPanel = "%s"     % calPan
            row.Band = "%s"    % bandNum
            upCur.updateRow(row)
        del upCur, row

print "Success" 

#END
