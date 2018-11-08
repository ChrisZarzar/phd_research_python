"""
Purpose: This script will loop
up values is one csv file based 
on an index values in another csv file

Notes: I would eventually like to 
evolve this script so that it can 
take user provided paths to the index csv
and the lookup csv. It will also need 
the index value column and the lookup
value column. Finally, it will automatically 
add a new column to the end of the index
csv file. 


"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/19 14:28:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar

________________________________________________________
#### HISTORY ####

CREATED Chris Zarzar 19-Oct-2016:

EDITED Chris Zarzar 19-Oct-2016:
Had to add the "_1.tif" to the row of the index values
so that it would match with the first band of the sorted column
without taking the altitude value of every band for each image. 
I also had to add in a counter and another conditonal statement to make sure that
the header was put into the output file. 
Realized that I could not just do nested for loops because once it 
made its way through the lookup reader, it could not go back up the list. 
once read through, it was done. So 'with open' fixed that.

***If I do list.seek(0), this will rewind and go to the top of the list.  This is much much faster. To look for certain values, I should you list.index(<value>). This would be much faster than if then statement. I could have been an issue of not closing the files, because even if you don’t store it in ram, it stores that search location on the harddrive. 

______________________________________________________________________________
"""

import os
import csv

#Set up the file paths
indexPath = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\Micasense_Image_Extract\\AltitudesCombined44%.csv"
lookupPath = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\MicaSense\\sortedAltitude.csv"
outPath = "F:\\NGI_UAS\\NorthFarm_Experiment\\uasImages\\2016_04_22\\Micasense_Image_Extract\\AltitudesCombined44%_csvCompare.csv"

#Set the rows that will be used as index values, lookup values, and output data values.
indexRow = 0
lookRow = 0
dataRow = 5
pathRow = 8

csvOut = open(outPath, 'w')   

print "Searching the lookup table for values provided from the index table."
#Set up a list that will hold all data  I want to write out
outList = []

count = 0
with open(indexPath, 'r') as csvIn:
    dataIn = csv.reader(csvIn, delimiter = ',')
    for row in dataIn:
        # Assign the column for index values. #Had to add the "_1.tif" so that it would match with the first band of the sorted column
        if count == 0:
            header = []
            header.extend(row)
            header.extend(["adj_alt_ft"])
            header.extend(["path"])
            headStr = ','.join(header) 
            csvOut.write(headStr+"\n")
            inRow = 'start'
        else: 
            inRow = row[indexRow]+"_1.tif"
        # Copy the row to a list to later write out 
        with open(lookupPath, 'r') as csvLo:
            dataLo = csv.reader(csvLo, delimiter = ',')
            for row2 in dataLo:
                loRow = row2[lookRow]
                outList = []
                if inRow == loRow:
                    data = row2[dataRow]
                    path = row2[pathRow]
                    outList.extend(row)
                    outList.extend([data])
                    outList.extend([path])
                    outList.extend("\n")
                else:
                    pass 
                outStr = ','.join(outList) 
                csvOut.write(outStr)
        count += 1

print "SUCCESS" 
csvIn.close()
csvLo.close()
csvOut.close()
#END