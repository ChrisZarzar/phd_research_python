# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 21:51:33 2017

@author: chris
"""

#!/usr/bin/python

"""
Purpose: Michael has a completely different 
file structure and the way the files are named has
screwed everything up with the compositing of the hecras 
and iric. So to try and fix this, the current script
will work through the directories and will rename the files in each folder. 



"""

__version__ = "$Revision: 2.4 $"[11:-2]
__date__ = "$Date: 2017/10/10 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 10 October 2017
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 10-Oct-2017

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
#        if "member 01" in dirName:
#            #Extract the .csv file name for naming purposes
#            hecName = "mem1_"+hecRas
#            print "Working in directory: "+dirName
#            outPath = dirName+"\\"
#            os.rename(outPath+hecRas, outPath+hecName)
        if "member 2" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem2_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 3" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem3_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 4" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem4_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 5" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem5_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 6" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem6_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 7" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem7_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 8" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem8_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 9" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem9_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 010" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem10_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
        if "member 011" in dirName:
            #Extract the .csv file name for naming purposes
            hecName = "mem11_"+hecRas
            print "Working in directory: "+dirName
            outPath = dirName+"\\"
            os.rename(outPath+hecRas, outPath+hecName)
