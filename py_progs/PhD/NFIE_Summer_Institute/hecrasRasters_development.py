#!/usr/bin/python

"""
Purpose: Michael has a completely different 
file structure to what we did last summer with 
his HECRAS output. I am therefore taking pieces
of the script and rewriting it so that it will do 
an os.walk to work through the entire file structure and 
postprocess everything



"""

__version__ = "$Revision: 2.4 $"[11:-2]
__date__ = "$Date: 2017/10/05 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 5 October 2017
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 5-Oct-2017
Had to adjust the script to handle the way Michael developed the new 
files structure using os.walk() and output the data to the same location
as the input data. 

EDITED: Chris Zarzar 5-Oct-2017

EDITED: Chris Zarzar 6-Oct-2017
Commented out processing for all other files except flood extent to
speed up processing and get the necessary data to Hossein and Michael
Also found that the current setup is cause the files to create multiple 
versions of each file. That is not good. I need to delete all this is 
unzip the original again. I will go ahead and run for flood extent, but
I will need to figure out how to make it process only once when I do it
for all of the conditional statements
_______________________________________________________

"""
#Setting up the script
import os
import arcpy
import shutil
from arcpy import env
from arcpy.sa import *
from arcpy import mapping as mp
import arcpy as ap
arcpy.env.overwriteOutput = True

##Set the base path for all files ***REQUIRED USER INPUT***
path = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\"

##Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

##Setup environment setting
env.workspace = path+"workspace\\"

##Input locaiton for original HEC-RAS rasters
hecRasdir = path+"modelOutput\\hecrasOutput\\"

##Location of the MXD document that will be created and edited
mapDoc = path+"imgCreation.mxd"
mxd = mp.MapDocument(mapDoc)

##Output location of the raster layers created
outlyrDir = path+"postprocessOutput\\rasters\\layers\\"

##Set up the spatial refernce for the file
spatialRef = arcpy.SpatialReference(32618) # 32618 is code for WGS_1984_UTM_Zone_18N 102387 is code for NAD_1983_2011_UTM_Zone_18N


##List the rasters in the HECRAS directory
#hecList = os.listdir(hecRasdir)

##List the files found in hecList with their full pathname
#fileList2 = [hecRasdir+"\\"+filename2 for filename2 in hecList]

##START THE SECOND PART OF SCRIPT: CREATE HECRAS ENSEMBLE RASTERS
##---------------------------------------------------------------------------

print "Beginning script processing"

#Set up look to postprocess HEC-RAS output
for dirName, subdirList, fileList2 in os.walk(hecRasdir):
    for hecRas in fileList2:
        if hecRas.endswith('.tif'):
            #Extract the .csv file name for naming purposes
            hecName = os.path.basename(hecRas[:-4])
            #has to add intergers to the naming convention so I can reference them later
            if "Depth" in hecName:
    
                print "Creating water depth rasters for "+hecName
                print "Working in directory: "+dirName
                
                outPath = dirName+"\\"
                outRasfldext = hecName+"_fldext.tif"
                if not os.path.exists(dirName+"\\"+outRasfldext): 
                    hecOut = Con(Raster(outPath+hecRas) > 0.05,2,1)
                    hecOut.save(outPath+outRasfldext)
    
                outRaswd1 = hecName+"_wd_hlfft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd1): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.15,2,1)
                    hecOut.save(outPath+outRaswd1)
                
                outRaswd2 = hecName+"_wd_1ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd2): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.305,2,1)
                    hecOut.save(outPath+outRaswd2)
                
                outRaswd3 = hecName+"_wd_2ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd3): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.61,2,1)
                    hecOut.save(outPath+outRaswd3)
    
                outRaswd4 = hecName+"_wd_3ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd4): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.91,2,1)
                    hecOut.save(outPath+outRaswd4)
                
                outRaswd5 = hecName+"_wd_4ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd5): 
                    hecOut = Con(Raster(outPath+hecRas) >= 1.22,2,1)
                    hecOut.save(outPath+outRaswd5)
    
                outRaswd6 = hecName+"_wd_5ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd6): 
                    hecOut = Con(Raster(outPath+hecRas) >= 1.5,2,1)
                    hecOut.save(outPath+outRaswd6)
                
                outRaswd7 = hecName+"_wd_6ft.tif"
                if not os.path.exists(dirName+"\\"+outRaswd7): 
                    hecOut = Con(Raster(outPath+hecRas) >= 1.83,2,1)
                    hecOut.save(outPath+outRaswd7)
        
            if "Velocity" in hecName:
                
                print "Creating flow velocity rasters for "+hecName
                
                outRasfv1 = hecName+"_fv_1mph.tif"
                if not os.path.exists(dirName+"\\"+outRasfv1): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.45,2,1)
                    hecOut.save(outPath+outRasfv1)
    
                outRasfv2 = hecName+"_fv_2mph.tif"
                if not os.path.exists(dirName+"\\"+outRasfv2): 
                    hecOut = Con(Raster(outPath+hecRas) >= 0.89,2,1)
                    hecOut.save(outPath+outRasfv2)
                
                outRasfv3 = hecName+"_fv_4mph.tif"
                if not os.path.exists(dirName+"\\"+outRasfv3): 
                    hecOut = Con(Raster(outPath+hecRas) >= 1.79,2,1)
                    hecOut.save(outPath+outRasfv3)
                
                outRasfv4 = hecName+"_fv_6mph.tif"
                if not os.path.exists(dirName+"\\"+outRasfv4): 
                    hecOut = Con(Raster(outPath+hecRas) >= 2.68,2,1)
                    hecOut.save(outPath+outRasfv4)
    
                outRasfv5 = hecName+"_fv_8mph.tif"
                if not os.path.exists(dirName+"\\"+outRasfv5): 
                    hecOut = Con(Raster(outPath+hecRas) >= 3.58,2,1)
                    hecOut.save(outPath+outRasfv5)
    
            #Now outside of these if statements do the critical conditions rasters so i can reference temp wd and fv rasters
            try:    
                try:
                    outRaswd1
                    outRasfv1
                except NameError:
                    print "Veloctiy output Rasters not yet created"
                else:
                    print "Creating critical condition rasters for "+hecName
                    
                    outRascrit1 = hecName+"_crit_hlf_4.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit1): 
                        hecOut = Con((Raster(outPath+outRaswd1)== 2) & (Raster(outPath+outRasfv3)==2),2,1)
                        hecOut.save(outPath+outRascrit1)
                    
                    outRascrit2 = hecName+"_crit_1_4.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit2): 
                        hecOut = Con((Raster(outPath+outRaswd2) == 2) & (Raster(outPath+outRasfv3)==2),2,1)
                        hecOut.save(outPath+outRascrit2)
                    
                    outRascrit3 = hecName+"_crit_2_4.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit3): 
                        hecOut = Con((Raster(outPath+outRaswd3) == 2) & (Raster(outPath+outRasfv3)==2),2,1)
                        hecOut.save(outPath+outRascrit3)
    
                    outRascrit4 = hecName+"_crit_hlf_6.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit4): 
                        hecOut = Con((Raster(outPath+outRaswd1) == 2) & (Raster(outPath+outRasfv4)==2),2,1)
                        hecOut.save(outPath+outRascrit4)
    
                    outRascrit5 = hecName+"_crit_1_6.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit5): 
                        hecOut = Con((Raster(outPath+outRaswd2) == 2) & (Raster(outPath+outRasfv4)==2),2,1)
                        hecOut.save(outPath+outRascrit5)
    
                    outRascrit6 = hecName+"_crit_2_6.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit6): 
                        hecOut = Con((Raster(outPath+outRaswd3) == 2) & (Raster(outPath+outRasfv4)==2),2,1)
                        hecOut.save(outPath+outRascrit6)
    
                    outRascrit7 = hecName+"_crit_3_2.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit7): 
                        hecOut = Con((Raster(outPath+outRaswd4) == 2) & (Raster(outPath+outRasfv2)==2),2,1)
                        hecOut.save(outPath+outRascrit7)
                    
                    outRascrit8 = hecName+"_crit_4_2.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit8): 
                        hecOut = Con((Raster(outPath+outRaswd5) == 2) & (Raster(outPath+outRasfv2)==2),2,1)
                        hecOut.save(outPath+outRascrit8)
    
                    outRascrit9 = hecName+"_crit_5_1.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit9): 
                        hecOut = Con((Raster(outPath+outRaswd6) == 2) & (Raster(outPath+outRasfv1)==2),2,1)
                        hecOut.save(outPath+outRascrit9) 
        
                    outRascrit10 = hecName+"_crit_6_1.tif"
                    if not os.path.exists(dirName+"\\"+outRascrit10): 
                        hecOut = Con((Raster(outPath+outRaswd7) == 2) & (Raster(outPath+outRasfv1)==2),2,1)
                        hecOut.save(outPath+outRascrit10) 
            except:
                pass 
#    
#    
    
    print "Second of script processing complete"


for dirName, subdirList, fileList2 in os.walk(hecRasdir):
    for hecRas in fileList2:
        if "fldext" in hecRas:
            if not os.path.exists(dirName+"\\FloodExtent\\"):
                    os.makedirs(dirName+"\\FloodExtent\\")
            shutil.copy(dirName+"\\"+hecRas,dirName+"\\FloodExtent\\" )

            