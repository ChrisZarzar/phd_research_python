# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 09:12:51 2016

@author: Chris
"""


"""
Purpose: This script will check the progress
of a script by tracking the directory and drive
that the script is writing to



"""

__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/12/07 11:17:00 $"[7:-2]
__author__ = "Chris Zarzar <chris.zarzar@gmail.com>"


"""
____________________________________________
Author: Chris Zarzar
Created: 7 December 2016
Contact: chris.zarzar@gmail.com


Notes: I original set up the script to run constantly 
and to check up on the progress once per hour
    
----History----



_______________________________________________________


"""
## Import required modules
import os 
import time 
import ctypes
import platform

## Define a function that will allow the extraction of disk space for all platforms
def get_free_space_gb(dirname):
    ## Return folder/drive free space (in gigabytes). For mb, just take away one of the 1024 divisions
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024
        
## Define global variables
#txtOut = "K:/general/cmzarzar/scriptProgress.txt"
txtOut = "K:/general/cmzarzar/scriptProgress.txt"
txtWriting = "K:/general/cmzarzar/WritingInProgress.txt"
txtDone = "K:/general/cmzarzar/WritingComplete_SafeToOpen.txt"
mainDrive = "E:" 
#listDir = "E:/CIR_UAS_Imagery"
#listDir1 = "E:/CIR_UAS_Imagery/Original_Clipped_Mosaics/"
listDir1 = "G:/zarzar_lpr_mosaics/"
#listDir2 = "E:/Research/CIR_UAS_Imagery/OriginalCIR/"
listDir2 = "E:/CIR_UAS_Imagery/Original_Clipped/"

print "Progress tracking script running"
while True:
    time.sleep(1800)  
    os.remove(txtDone)
    ## Create a text files so I can remotely see if the script is currently writing and I don't mess it up
    fStatus = open(txtWriting, 'w')
    fStatus.close()
    f = open(txtOut,'w')
    ## Check disk space on main drive
    diskStats = get_free_space_gb(mainDrive)
    ## List file creation progress in the script output dir
    ## Write all information to ouput text file
    f.write("Main disk space information free space: "+str(diskStats)+" GB \n\n")
    f.write("Contents of the Original Image Mosaic directory: \n")
    ## This will write a nicely formatted table style list
    dirList = os.listdir(listDir1)
    fileList = os.listdir(listDir1)
    for fname in fileList:
        f.write("\t"+fname+"\n")        
    ## List contents in directories that I need to recursively look through    
    f.write("Contents of the Original Image directory: \n\n")
    for dirName2, subdirList2, fileList2 in os.walk(listDir2):
        f.write("Contents in "+dirName2+"\n")
        for fname2 in fileList2:
            f.write("\t"+fname2+"\n") 
    fStatus = open(txtDone, 'w')
    fStatus.close()
    os.remove(txtWriting)
    ## Close the text file to free the RAM
    f.close()

   
    
#END