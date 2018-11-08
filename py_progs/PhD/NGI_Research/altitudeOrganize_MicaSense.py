"""
Purpose: Purpose: This script will create
a textfile list of the altitude information
extracted from images in a directory.



"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/21 12:09:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar


Purpose: This script will extract gps information from the
North Farm Experiment Canon DSLR camera and will
copy the images into folders depending on their GPS information

Requirements:
1. Python Image Library (PIL)
2. ExifRead
3. imageinfo
    a. gpsExtract 
______________________________________________________________________________
#### HISTORY ####

21-jun-2016 [Chris Zarzar]: Created

EDITED Chris Zarzar 20-Sep-2016:
Working on getting the script to work for
the MicaSense imagery.

EDITED Chris Zarzar 21-Sep-2016:
Used Lee Hathcocks scripst as examples for adjusting this 
script to work with TIFS. Mainly, I switched from using 
PIL to using exifread to get the tags. 


EDITED Chris Zarzar 27-Sep-2016:
I got the listFlightData script working, so i will use that script
to adjust this script and get this one to work for sorting the data. 
______________________________________________________________________________
"""


from imageinfo import gpsExtract
import os
import shutil

imageDir = "I:\\Research\\NorthFarm_Experiment\\micasenseBRDF"

#create required directories
orgDir = imageDir + "/micasenseBRDFOrganized"
if not os.path.exists(orgDir):
    os.makedirs(orgDir)
    
altVector = (30,100,200,300,400,500,600,700,800)
for x in altVector:
    if not os.path.exists(orgDir+"/"+str(x)):
        os.makedirs(orgDir+"/"+str(x))

# Loop through the image directory and extract metadata information from each image. 
try:
    for dirName, subdirList, fileList in os.walk(imageDir):
        for fname in fileList:
            if fname.endswith('.tif') or fname.endswith('.TIF'):
                print "Extracting GPS information from %s" % fname
                fpath = dirName+"\\"+fname
                gpsInfo = gpsExtract.gpsInfo
                gpsOut = gpsInfo(fpath)
                if 2<= (gpsOut[2]- 84.1) <=16:
                    outDir = orgDir+"/30"
                    shutil.copy2(fpath, outDir)
                elif 23<= (gpsOut[2]- 84.1) <=37:
                    outDir = orgDir+"/100"
                    shutil.copy2(fpath, outDir)
                elif 53<= (gpsOut[2]- 84.1) <=67:
                    outDir = orgDir+"/200"
                    shutil.copy2(fpath, outDir)
                elif 84<= (gpsOut[2]- 84.1) <=98:
                    outDir = orgDir+"/300"
                    shutil.copy2(fpath, outDir)
                elif 115<= (gpsOut[2]- 84.1) <=129:
                    outDir = orgDir+"/400"
                    shutil.copy2(fpath, outDir)
                elif 145<= (gpsOut[2]- 84.1) <=159:
                    outDir = orgDir+"/500"
                    shutil.copy2(fpath, outDir)
                elif 175<= (gpsOut[2]- 84.1) <=189:
                    outDir = orgDir+"/600"
                    shutil.copy2(fpath, outDir)
                elif 206<= (gpsOut[2]- 84.1) <=220:
                    outDir = orgDir+"/700"
                    shutil.copy2(fpath, outDir)
                elif 236<= (gpsOut[2]- 84.1) <=250:
                    outDir = orgDir+"/800"
                    shutil.copy2(fpath, outDir)
except:
    pass                    
print "Processing complete"
                 
print "Processing complete"

 ##END##
                

  
