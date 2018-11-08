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

imageDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/Canon_CIR/"

#create required directories

dirList = os.listdir(imageDir)
fileList = [imageDir+filename for filename in dirList]
for fname in fileList:
    if fname.endswith('.jpg') or fname.endswith('.JPG'):
        print "Extracting GPS information from %s" % fname
        gpsInfo = gpsExtract.gpsInfo
        gpsOut = gpsInfo(fname)
        if 250 <= gpsOut[3] <=300:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/250_300"
            shutil.copy2(fname, outDir)
        elif 301 <= gpsOut[3] <=350:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/301_350"
            shutil.copy2(fname, outDir)
        elif 351 <= gpsOut[3] <=400:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/351_400"
            shutil.copy2(fname, outDir)
        elif 401 <= gpsOut[3] <=450:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/401_450"
            shutil.copy2(fname, outDir)
        elif 451 <= gpsOut[3] <=500:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/451_500"
            shutil.copy2(fname, outDir)
        elif 501 <= gpsOut[3] <=550:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/501_550"
            shutil.copy2(fname, outDir)
        elif 551 <= gpsOut[3] <=600:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/551_600"
            shutil.copy2(fname, outDir)
        elif 601 <= gpsOut[3] <=650:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/601_650"
            shutil.copy2(fname, outDir)
        elif 651 <= gpsOut[3] <=700:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/651_700"
            shutil.copy2(fname, outDir)
        elif 701 <= gpsOut[3] <=750:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/701_750"
            shutil.copy2(fname, outDir)
        elif 751 <= gpsOut[3] <=800:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/751_800"
            shutil.copy2(fname, outDir)
        elif 801 <= gpsOut[3] <=850:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/801_850"
            shutil.copy2(fname, outDir)
        elif 851 <= gpsOut[3] <=900:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/851_900"
            shutil.copy2(fname, outDir)
        elif 901 <= gpsOut[3] <=950:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/901_950"
            shutil.copy2(fname, outDir)
        elif 951 <= gpsOut[3] <=1000:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/951_1000"
            shutil.copy2(fname, outDir)
        elif 1001 <= gpsOut[3] <=1050:
            outDir = "F:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/canonOrganized/1001_1050"
            shutil.copy2(fname, outDir)

             
print "Processing complete"

 ##END##
                

  
