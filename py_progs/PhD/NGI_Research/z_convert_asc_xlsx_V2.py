#!/usr/bin/python

"""
Purpose: This script will extract classification 
sample information from point shapefiles created in Arc

NOTES:
The working Excel document that you create must be save in Excel 97-2003 format (.xls)
The purpose of this script is to recursively search through a directory and import all files to Excel

PACKAGE REQUIREMENTS:
csv
fnmatch
xlwt
xlrd
xlutils


If ImportError is received, the above packages are not install. To install these packages, use the reference
IN  LINUX OR OSX, TYPE THIS INTO TERMINAL
pip install PackageName

IN WINDOWS, TYPE THIS INTO COMMAND PROMPT 
python -m pip install PackageName

"""

__version__ = "$Revision: 1.2 $"[11:-2]
__date__ = "$Date: 03/22/2017 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 04 June 2015
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 04-Jun-2015

EDITED: Chris Zarzar 08-Jun-2015
*Changing script so that it will correctly bring in any tab seperated file to excel 
into a single, preset workbook
*Found out that the Excel document must be saved in Excel 97-2003 format to work (xls)

EDITED: Chris Zarzar 03-Mar-2017
*Making it possible for the script to work when headers are present. Headers currently break the script
*Adjusted script so that it will use the csv module to do most of the file manipulation.
*Adding features to import data more like how Sauree needs the final product. 
*The headers will stay consistent, so I added test that if the first row has GER in the name, skip the first 14 rows. 
__________________________________

"""
import os
import csv
import fnmatch
import xlwt
import xlrd
from xlutils.copy import copy as copy


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False      
workbook = raw_input("Enter the name of the excel workbook you created to put the data (use the format C:\\user\\...\\Workbook.xls):")        
rootdir = raw_input("Enter the directory which holds the subdirectories of the radiometric data (use the format C:\\user\\...):") 

for root, dirnames, files in os.walk(rootdir):    
    for files in fnmatch.filter(files, '*.sig'): 
        fname = (os.path.join(root,files))
        sheet = os.path.basename(fname[:-4]) #this grabs the name of the file I am working with and will use it to name the sheets
        
        style = xlwt.XFStyle()
        style.num_format_str = '#,###0.00'  
        ##CZ, CHANGE THIS TO READ IN USING CSV READER
        rb = xlrd.open_workbook(workbook,formatting_info=True) #open the workbook I want to eventually work with
        wb = copy(rb) #create a temporary workbook to do write into
        ws = wb.add_sheet(sheet) #add a new sheet to the temporary wrinting workbook
        csvOut = open(rootdir+"temp.csv", 'w') #Create the output CSV file
        f = open(fname, 'rb')
        readCSV = csv.reader(f, delimiter=' ', skipinitialspace = True)
        row_num = 0
        for  row in readCSV:
            if "///GER" in row:
                for _ in xrange(13): #Skip the next 14 header lines if there are headers. 
                    next(readCSV)
            else: 
                #csvOut.write(row) 
                for col in range(len(row)):
                    ## Convert the values to a float for proper excel formatting 
                    if is_number(row[col]): 
                        ws.write(row_num, col, float(row[col]), style=style)
                    else:
                        ws.write(row_num, col, row[col])
                row_num += 1

        wb.save(workbook) # Save the updated workbook
        csvOut.close()
        #os.remove(rootdir+"temp.csv")

print "Script complete"
## END ##
        
     
