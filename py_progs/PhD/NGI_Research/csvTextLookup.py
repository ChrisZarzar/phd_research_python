"""
Purpose: This script will loop
up for specific text in a row and
will extract that entire row that 
text falls in.


"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/20 15:24:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar

________________________________________________________
#### HISTORY ####

CREATED Chris Zarzar 20-Oct-2016:
Wrote this for Louis simply for text file management. More advance techniques
can be used if csv module is used. 

****If I do list.seek(0), this will rewind and go to the top of the list.  This is much much faster. To look for certain values, I should you list.index(<value>). This would be much faster than if then statement. I could have been an issue of not closing the files, because even if you don’t store it in ram, it stores that search location on the harddrive. 

______________________________________________________________________________
"""


csvPath = "F:\\py_progs\\PhD\\NGI Research\\Louis_Flight_Data.csv"
outPath = "F:\\py_progs\\PhD\\NGI Research\\sorted_flight_data.csv"


#Set the text that will be used to search for.
searchText = "mavlink_global_position_int_t"

textOut = open(outPath, 'w')   

  
print "Searching the table table for information provided."
#Set up a list that will hold all data  I want to write out
outList = []
count = 0
with open(csvPath, 'r') as textIn:
    for line in textIn:
        # Assign the column for index values. #Had to add the "_1.tif" so that it would match with the first band of the sorted column
        if searchText in line:
            textOut.write(line)            
        count += 1
         
print "COMPLETE" 
textIn.close()
textOut.close()
#END          
            
            
            
            
            
            