"""
Purpose: Purpose: This script will take tranformation information from one
raster and apply it to list of similar rasters



"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2018/11/02 16:40:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar

Requirements:
1. os.system
2. gdal
______________________________________________________________________________
#### HISTORY ####

2018/11/02 [Chris Zarzar]: Created

EDITED Chris Zarzar 
______________________________________________________________________________
"""



import os

inRas = "C:/Users/zarzarc/OneDrive/Desktop/Research/MSU/NF_updated/Lee_revised_8_3_17_data/radiance_100ft/400/stack/IMG_0198_1.tif" 
tmpRas = "C:/Users/zarzarc/AppData/Local/Temp/IMG_0198_1.tif"
outRas = "C:/Users/zarzarc/OneDrive/Desktop/Research/MSU/NF_updated/Lee_revised_8_3_17_data/radiance_100ft/400/stack/IMG_0198_1_modified.tif"

#The settings below apply georeferencing from the 400 ft IMG_0000_1.tif file. 
#os.system('"C:/Program Files/QGIS 3.2/bin/gdal_translate.exe" -a_srs EPSG:4326 %s %s' %(inRas, tmpRas1))

os.system('"C:/Program Files/QGIS 3.2/bin/gdal_translate.exe" -of GTiff \
-gcp -88.77807840365286 33.47641047263815 -88.77807966365464 33.47641132647519 \
-gcp -88.7780199693518 33.476472222422466 -88.77802076469791 33.47647305079945 \
-gcp -88.77798001507846 33.47648098324635 -88.77798120530467 33.47648178650048 \
-gcp -88.77790696331213 33.476436599205755 -88.77790813434251 33.476437182939705 \
-gcp -88.77793146225929 33.47656957622988 -88.77793224636152 33.476570286261015 \
-gcp -88.77798640414903 33.476509392799635 -88.77798734085776 33.47651052963219 \
-gcp -88.77802769538418 33.47650960739602 -88.77802863147198 33.476510916558965 \
-gcp -88.77810965066473 33.476557944957435 -88.77811085724393 33.476558903197954 \
%s %s' %(inRas, tmpRas))

os.system('"C:/Program Files/QGIS 3.2/bin/gdalwarp.exe" -r bilinear -tps -co COMPRESS=NONE -dstalpha %s %s' %(tmpRas, outRas))

print "Processing complete"

 ##END##
                

  
