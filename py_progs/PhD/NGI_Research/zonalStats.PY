#This script uses two textfiles provided by the user to run zonal statistics
#as table on the sites provided and the associated raster image provided.

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
outDir = "C:\\cmzarzar\\NGI_UAS\\GIS\\Brightness_values_extracted"



#****FOR SITE 110-111********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR110-111.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR110-111.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 



#****FOR SITE 113********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR113.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR113.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 114********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR114.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR114.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 115********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR115.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR115.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 119********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR119.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR119.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 120-121********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR120-121.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR120-121.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 122-123********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR122-123.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR122-123.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 124********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR124.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR124.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 127********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR127.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR127.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 128-130********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR128-130.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR128-130.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 



#****FOR SITE 131-133********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR131-133.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR131-133.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 





#****FOR SITE 134********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR134.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR134.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 135-136********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR135-136.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR135-136.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 137-139********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR137-139.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR137-139.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 140-141********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR140-141.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR140-141.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 142-145********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR142-145.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR142-145.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 




#****FOR SITE 147-148********
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pySiteList_LPR147-148.txt"
siteList = [line.rstrip() for line in open(inputfile)]
inputfile = "C:\\cmzarzar\\NGI_UAS\\GIS\\pyRasList_LPR147-148.txt"
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
        outTable = "%s\\%s_%s%s.dbf" %(outDir, site, rasList1[0],bandName)
        sitePath = "%s\\%s.shp" %(siteDir,site)
        # Execute ZonalStatisticsAsTable
        outZSaT = arcpy.gp.ZonalStatisticsAsTable_sa(sitePath, zoneField, ras, outTable, nullData, statsType) 
