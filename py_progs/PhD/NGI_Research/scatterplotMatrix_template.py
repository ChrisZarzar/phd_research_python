"""
Purpose: This script will create 
a scatterplot matrix

Notes: This script is based on a script
Dr. Jamie Dyer provided as an example

"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/10/19 14:28:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar

________________________________________________________
#### HISTORY ####

CREATED Chris Zarzar 19-Oct-2016:


______________________________________________________________________________
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

# Open data file

dataFile = open ('F:\\py_progs\\PhD\\NGI Research\\zarzar.csv','r')
dataArr = csv.reader (dataFile)
dataArr.next()

xVals = []
yVals = list()

for row in dataArr:
    xVals.append (float(row[3]))
    yVals.append (float(row[4]))
x=np.asarray(xVals)
y=np.asarray(yVals)
# Figure a
plt.subplot(221)
plt.scatter (x, y)
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
#plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05),)

# Figure b
plt.subplot(222)
plt.scatter (x, y)
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)

# Figure c
plt.subplot(223)
plt.scatter (x, y)
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)

# Figure d
plt.subplot(224)
plt.scatter (x, y)
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)

plt.show()

dataFile.close()
