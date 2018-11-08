# -*- coding: utf-8 -*-
"""
Purpose: This script will take the CSV ouput
from iRIC and will delete the first two 
unecessary lines and save them to new files



"""

__version__ = "$Revision: 2.4 $"[11:-2]
__date__ = "$Date: 2016/07/6 16:25:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 20 June 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 21-Jun-2016
Created script and set up to take a directory of ensembles
and add together grid cells that correspond to certain criteria

____________________________________________
"""
import os 

##Input location of CSV files 
csvDir = "C:\\Users\\chris\\OneDrive\\Desktop\\Research\\groupProject\\modelOutput\\csvFiles\\Day2\\"

#List the files in the CSV directory
dirList = os.listdir(csvDir)

#List the files found in dirList with their full pathname
fileList = [csvDir+"\\"+filename for filename in dirList]

#other way of doing it if no subfolders for csvFile in os.walk(csvDir):
for csvFile in fileList:
    if csvFile.endswith('.csv'):
        with open(csvFile,'r') as f:
            csvName = os.path.basename(csvFile[:-4])
            with open(csvDir+csvName+"_edited.csv",'w') as f1:
                f.next() # skip header line
                f.next() # skip next unnecessary line
                for line in f:
                    f1.write(line)
            
##END
