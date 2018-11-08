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

31-may-2017 [Chris Zarzar]: Edited; adjusted so to use os.walk to go through
the directory and set up so that it will work only for JPEGS
______________________________________________________________________________
"""

from imageinfo import gpsExtract
from imageinfo import dateExtract
import os

imgDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\NorthFarm_Experiment\\phantom\\images"

#create textfile to write out to
with open(imgDir+"\\phantomAlt.txt", "w") as txtfile:    
    try: 
        # Loop through the image directory and extract metadata information from each image. 
        for dirName, subdirList, fileList in os.walk(imgDir):
            for fname in fileList:
                if fname.endswith('.jpg') or fname.endswith('.JPG'):
                    fpath = dirName+"\\"+fname
                    print "Extracting GPS information from image file %s" % fname
                    gpsInfo = gpsExtract.gpsInfo
                    gpsOut = gpsInfo(fpath)
                    dateInfo = dateExtract.dateInfo
                    dateOut = dateInfo(fpath)
                    if gpsOut[2] == None:
                        line = "%s,%s,%s,%s,%s\n" % (os.path.basename(fpath), dateOut[0], dateOut[1], gpsOut[2], gpsOut[3])
                        txtfile.write(line)
                    else: 
                        line = "%s,%s,%s,%f,%f\n" % (os.path.basename(fpath), dateOut[0], dateOut[1],  gpsOut[2], gpsOut[3])
                        txtfile.write(line)
    except:
        pass                    
    print "Processing complete"
txtfile.close() #Close the textfile once GPS data has been written for all images in dir