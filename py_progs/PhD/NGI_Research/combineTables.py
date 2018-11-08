#!/usr/bin/python

"""
______________________________________________
Author: Christopher M. Zarzar
Created: 01-27-16

NOTES: This script with take those values extracted from each site from the
UAS imagery and will organize them into spreadsheets organized by Band number.
So each spreadsheet will have all the ZonalStatics output for each site
according to the Band number those values are assoicated with.

_____________________________________________
"""

# Set up the variables and environment
import numpy
import os
workDir = "C:\Users\zarza\Desktop\NGI\Brightness_values_extracted_Dec2015\csv_files"


# Create arrrays of zeros for each band
csv06B1 = workDir+"\\Band1_06%.csv" # Array for band 1 6% reflectance that new data will be added to
csv22B1 = workDir+"\\Band1_22%.csv" # Array for band 1 22% reflectance that new data will be added to
csv44B1 = workDir+"\\Band1_44%.csv" # Array for band 1 44% reflectance that new data will be added to

csv06B2 = workDir+"\\Band2_06%.csv" # Array for band 2 6% reflectance that new data will be added to
csv22B2 = workDir+"\\Band2_22%.csv" # Array for band 2 22% reflectance that new data will be added to
csv44B2 = workDir+"\\Band2_44%.csv" # Array for band 2 44% reflectance that new data will be added to

csv06B3 = workDir+"\\Band3_06%.csv" # Array for band 3 6% reflectance that new data will be added to
csv22B3 = workDir+"\\Band3_22%.csv" # Array for band 3 22% reflectance that new data will be added to
csv44B3 = workDir+"\\Band3_44%.csv" # Array for band 3 44% reflectance that new data will be added to

csv06B4 = workDir+"\\Band4_06%.csv" # Array for band 4 6% reflectance that new data will be added to
csv22B4 = workDir+"\\Band4_22%.csv" # Array for band 4 22% reflectance that new data will be added to
csv44B4 = workDir+"\\Band4_44%.csv" # Array for band 4 44% reflectance that new data will be added to

# List all variables in the working directory
dirList = os.listdir(workDir)
fileList = [workDir+"\\"+filename for filename in dirList]

# Loop to read through all of the files in the given directory for each of the bands
for band in range (1,5):
    bnum = str(band)
    for fname in fileList:
        if "06%_Band_"+bnum in fname: # Use files with 6% reflectance 
            csvOut = open(workDir+"\\Band"+bnum+"_06%.csv", 'a') 
            csvFile = open(fname) 
            csvFile.next() # Skip the header line, I will add that in later
            for row in csvFile:
                csvOut.write(row) # Write data to output csv file
            csvFile.close()
            csvOut.close()
            
        if "22%_Band_"+bnum in fname: # Use files with 22% reflectance 
            csvOut = open(workDir+"\\Band"+bnum+"_22%.csv", 'a')
            csvFile = open(fname) 
            csvFile.next() # Skip the header line, I will add that in later
            for row in csvFile:
                csvOut.write(row) # Write data to output csv file
            csvFile.close()
            csvOut.close()
            
        if "44%_Band_"+bnum in fname: # Use files with 44% reflectance 
            csvOut = open(workDir+"\\Band"+bnum+"_44%.csv", 'a')
            csvFile = open(fname) 
            csvFile.next() # Skip the header line, I will add that in later
            for row in csvFile:
                csvOut.write(row) # Write data to output csv file
            csvFile.close()
            csvOut.close()

print "Processing complete"    
