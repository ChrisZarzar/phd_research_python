#!/usr/bin/python

"""
Purpose: This script will call the command line 
subprocess and will backup all the folders defined by the above variables.

____________________________________________
Author: Chris Zarzar
Created: 25 October 2016
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 25-Oct-2016

EDITED: Chris Zarzar 01-Nov-2016
Added the ability to have two way communication between the 
drives being backed up.
If there are any issues with the directory dissapearing, something probably 
happened wiht the copying of hidden system folders. Just add this to the end 
of the script and run it again
subprocess.call('attrib -h -s %s' %(src1))
subprocess.call('attrib -h -s %s' %(dst1))
_______________________________________________________


"""
import subprocess 
import sys 

print "Executing backup"


# This will allow two way communication backup between the drives. This can later be made into an innteractive argument provided by the user.
twoWay = 'y' # 'y' option is not available because the second portion of the script is not working. I cannot figure out why it is not working

#Set up the source and the backup directories
#dst1 = 'F:\\Research\\2014_2017'
#dst1 = 'K:\\general\\cmzarzar'
src1 = 'E:\\Research'
dst1 = 'C:\\Users\\Chris\\Desktop\\Research'
# Assign where the list of files copied will go. Not working, will have to work on later
#sys.stdout = open(src1+'\\FilesBackedUp.txt', "w")
#Set up a text file list of files and directories to exclude from the backup
excludeList = src1+'\\excludedFiles.txt'
writeList = open(excludeList,'w')
exclude = [src1+'\\CIR_UAS_Imagery\\', src1+'\\gefsData\\', src1+'\\Images_For_Presentation_and_Paper\\', src1+'\\NFIE_SI_2016\\', src1+'\\NGI_UAS\\', src1+'\\$RECYCLE.BIN\\', excludeList]
#exclude = [src1+'\\gefsData\\', src1+'\\$RECYCLE.BIN\\', excludeList]
for file in exclude:
    writeList.write(file+'\n')
    
writeList.close()
subprocess.call('xcopy %s %s /s /d /e /i /r /y /c /exclude:%s' %(src1, dst1, excludeList)) # add /q to quite on screen writing of the output of files copied. add /h to also save hidden files /k retains read only permissions

if twoWay != 'y':
    print "Backup complete"
else:
    #simply switch the src and directory folds and adjust the exclude list appropriately. This is probably the slowest way to have two way communication
    src2 = dst1
    dst2 = src1
    #Set up a text file list of files and directories to exclude from the backup
    # Assign where the list of files copied will go 
    sys.stdout = open(src1+'\\FilesBackedUp.txt', "w")
    excludeList = src2+'\\excludedFiles.txt'
    writeList = open(excludeList,'w')
    exclude = [src2+'\\$RECYCLE.BIN\\', excludeList]
    #exclude = [src2+'\\$RECYCLE.BIN\\',src2+'IntroductionToWRFHydro.pdf', src2+'Image-ExifTool-10.26.tar.gz', src2+'VCForPython27.msi', src2+'\\BackupOnDrive\\', src2+'\\CIR_UAS_Imagery\\', src2+'\\Field_Remote_Sensing_Labs\\', src2+'\\GIS_data\\', src2+'\\Micasense_UAS_Imagery\\', src2+'\\Poland_Dem\\', src2+'\\Pre_10-10-16_Backup\\', src2+'\\RS_Image_Analysis_Labs\\', src2+'\\Snow_Trend_Data_Map_Creation\\', src2+'\\Mendeley-Desktop-1.14-win32.exe', src2+'\\exiftool-10.26.zip', src2+'\\exiftool(-k).exe', src2+'\\documents-export-2016-03-08.zip', src2+'\\dirList.txt', src2+'\\Dataflex_Letters-162439300411.pdf', src2+'\\collage-2015-09-02.png', excludeList]
    for file in exclude:
        writeList.write(file+'\n')
        
    writeList.close()
    subprocess.call('xcopy %s %s /s /d /e /i /r /y /c /exclude:%s' %(src1, dst1, excludeList)) # add /q to quite on screen writing of the output of files copied. add /h to also save hidden files /k retains permissions
    print "Backup complete"


##END 