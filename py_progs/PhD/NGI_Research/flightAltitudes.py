"""
Purpose: Purpose: This script will create
a textfile list of the altitude information
extracted from images in a directory.



"""
__version__ = "$Revision: 2.0 $"[11:-2]
__date__ = "$Date: 2016/06/12 15:38:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar


Purpose: This script will create a textfile list of the altitude information
extracted from images in a directory

Requirements:
1. Python Image Library (PIL)
2. ExifRead
3. imageinfo
    a. gpsExtract 
______________________________________________________________________________
#### HISTORY ####

12-jun-2016 [Chris Zarzar]: Created
______________________________________________________________________________
"""


from imageinfo import gpsExtract
import os

imageDir = "E:/NGI_UAS/NorthFarm_Experiment/uasImages/2016_04_22/Micasense/0003SET/000/test/"
dirList = os.listdir(imageDir)
fileList = [imageDir+filename for filename in dirList]
with open("MicaSenseAltitudes_0003Set.txt", "a") as txtfile:
    for fname in fileList:   
        if fname.endswith('.tif'): #this is required because exifread only reads .tiff, not .tif
            fnameNew = fname.replace('.tif','.tiff')
            fnameOut = os.rename(fname,fnameNew)
            print "Extracting GPS information from image file %s" % fnameNew
            gpsInfo = gpsExtract.gpsInfo
            gpsOut = gpsInfo(fnameNew)
            if gpsOut[2] == None:
                line = "%s,%s,%s\n" % (os.path.basename(fnameNew), gpsOut[2], gpsOut[3])
                txtfile.write(line)
            else: 
                line = "%s,%f,%f\n" % (os.path.basename(fnameNew), gpsOut[2], gpsOut[3])
                txtfile.write(line)
        if fname.endswith('.jpg') or fname.endswith('.JPG') or fname.endswith('.tiff'):
            print "Extracting GPS information from image file %s" % fname
            gpsInfo = gpsExtract.gpsInfo
            gpsOut = gpsInfo(fname)
            if gpsOut[2] == None:
                line = "%s,%s,%s\n" % (os.path.basename(fname), gpsOut[2], gpsOut[3])
                txtfile.write(line)
            else: 
                line = "%s,%f,%f\n" % (os.path.basename(fname), gpsOut[2], gpsOut[3])
                txtfile.write(line)
txtfile.close() #Close the textfile once GPS data has been written for all images in dir
                
