"""
Purpose: This script will organize
and reformat cells in a csv file 


"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/21 09:06:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar

________________________________________________________
#### HISTORY ####

CREATED Chris Zarzar 20-Oct-2016:


______________________________________________________________________________
"""

import csv

csvPath = "F:\\py_progs\\PhD\\NGI Research\\sorted_flight_data_LW.csv"
outPath = "F:\\py_progs\\PhD\\NGI Research\\adj_flight_data.csv"

#Set the rows that will be reformatted
dateRow = 0
timeRow = 1
latRow = 4
lonRow = 6
altRow = 8
relAltRow = 10

csvOut = open(outPath, 'w')  

count = 0
with open(csvPath, 'r') as csvIn:
    dataIn = csv.reader(csvIn, delimiter = ',')
    for row in dataIn:
        # Assign the column for index values. #Had to add the "_1.tif" so that it would match with the first band of the sorted column
        if count == 0:
            header = ["Date", "Time_24hr", "Lat", "Lon", "Alt", "Rel_Alt"]
            headStr = ','.join(header) 
            csvOut.write(headStr+"\n")
        else: 
            outList = []
            date = row[dateRow]
            outList.extend([date])
            time = row[timeRow]
            outList.extend([time])
            lat = row[latRow]
            latForm = lat[:-7]+"."+lat[-7:]
            outList.extend([latForm])   
            lon = row[lonRow]
            lonForm = lon[:-7]+"."+lon[-7:]
            outList.extend([lonForm])
            alt = row[altRow]
            altForm = alt[:-3]+"."+alt[-3:]
            outList.extend([altForm])
            relAlt = row[relAltRow]
            relAltForm = relAlt[:-3]+"."+relAlt[-3:]
            outList.extend([relAltForm])            
            outList.extend("\n")    
            outStr = ','.join(outList) 
            csvOut.write(outStr)
        count += 1

csvOut.close()    
print "COMPLETE"
#END