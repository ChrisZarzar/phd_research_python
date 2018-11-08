"""
Purpose: Purpose: This script will create
a textfile list of the altitude information
extracted from images in a directory.



"""
__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2017/05/30 12:09:47 $"[7:-2]
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

30-may-2017 [Chris Zarzar]: Edited; Adjusted to make more intuative by creating
necessary directories and searching. 
______________________________________________________________________________
"""


from imageinfo import gpsExtract
import os
import shutil

imageDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\NorthFarm_Experiment\\canon\\images"

#create required directories
orgDir = imageDir + "\\canonOrganized"
if not os.path.exists(orgDir):
    os.makedirs(orgDir)
    
altVector = (30,100,200,300,400,500,600,700,800)
for x in altVector:
    if not os.path.exists(orgDir+"/"+str(x)):
        os.makedirs(orgDir+"/"+str(x))
try: 
    # Loop through the image directory and extract metadata information from each image. 
    for dirName, subdirList, fileList in os.walk(imageDir):
        for fname in fileList:
            if fname.endswith('.jpg') or fname.endswith('.JPG'):
                print "Extracting GPS information from %s" % fname
                fpath = dirName+"\\"+fname
                gpsInfo = gpsExtract.gpsInfo
                gpsOut = gpsInfo(fpath)
                if 2<= (gpsOut[2]- 87.2) <=16:
                    outDir = orgDir+"/30"
                    shutil.copy2(fpath, outDir)
                elif 23<= (gpsOut[2]- 87.2) <=37:
                    outDir = orgDir+"/100"
                    shutil.copy2(fpath, outDir)
                elif 53<= (gpsOut[2]- 87.2) <=67:
                    outDir = orgDir+"/200"
                    shutil.copy2(fpath, outDir)
                elif 84<= (gpsOut[2]- 87.2) <=98:
                    outDir = orgDir+"/300"
                    shutil.copy2(fpath, outDir)
                elif 115<= (gpsOut[2]- 87.2) <=129:
                    outDir = orgDir+"/400"
                    shutil.copy2(fpath, outDir)
                elif 145<= (gpsOut[2]- 87.2) <=159:
                    outDir = orgDir+"/500"
                    shutil.copy2(fpath, outDir)
                elif 175<= (gpsOut[2]- 87.2) <=189:
                    outDir = orgDir+"/600"
                    shutil.copy2(fpath, outDir)
                elif 206<= (gpsOut[2]- 87.2) <=220:
                    outDir = orgDir+"/700"
                    shutil.copy2(fpath, outDir)
                elif 236<= (gpsOut[2]- 87.2) <=250:
                    outDir = orgDir+"/800"
                    shutil.copy2(fpath, outDir)
except:
    pass                    
print "Processing complete"

 ##END##
                

  
