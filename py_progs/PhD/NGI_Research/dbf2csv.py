#!/usr/bin/python

"""
______________________________________________
Author: Christopher M. Zarzar
Created: 01-13-16

NOTES: This script will take any ArcMap dbf file and wil convert it
to csv format. The first step of asking if you would like to put the csv files
in another location does not work. Therefore, say no for this statement and
manually move the files until a resolution for this problem is found.

_____________________________________________
"""


import csv
from dbfpy import dbf
import os
import sys
newDir = raw_input('Would you like to move the converted csv files to a new directory (y or n): ')
if newDir == "y":
    outDir = raw_input('Enter full path for directory to move converted csv files: ')
workDir = raw_input('Enter full directory path for DBF files: ')
dirList = os.listdir(workDir+"\\")
fileList = [workDir+"\\"+filename for filename in dirList]
for fname in fileList:
    #Need to add a loop so it will go through all of the files in a directory
    if fname.endswith('.dbf'):
        print "Converting %s to csv" % fname
        csv_fn = fname[:-4]+ ".csv"
        with open(csv_fn,'wb') as csvfile:
            in_db = dbf.Dbf(fname)
            out_csv = csv.writer(csvfile)
            names = []
            for field in in_db.header.fields:
                names.append(field.name)
            out_csv.writerow(names)
            for rec in in_db:
                out_csv.writerow(rec.fieldData)
            in_db.close()
            if newDir == "y":
                os.rename("%s\%s","%s\%s") % (workDir, csvfile, outDir, csvfile)
            print "Done..."
    else:
      print "Filename does not end with .dbf"
