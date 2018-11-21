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

***
With the expontential line in my script, you can set the axis label and give it a list of values, rather than the points, that will force it to match the same length. 
So create the curve with zx = np.arrange(0,100,1) y=function(x)

______________________________________________________________________________
"""

import csv
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Open data file

dataFile = open ('F:\\NGI_UAS\\GER_UAS_Regressions\\CIR Calibration\\Radiance_Regressions\\GER_Nova_DecAug_B1_DevData.csv','r')
dataArr = csv.reader (dataFile)
dataArr.next()

xVals = []
yVals = list()

for row in dataArr:
    xVals.append (float(row[3]))
    yVals.append (float(row[4]))
    
x=np.asarray(xVals)
y=np.asarray(yVals)
fitLineB1 = 2773.7*np.exp(0.0168*x)
fitLineB2 = 2247.1*np.exp(0.0171*x)
fitLineB3 = 2501.7*np.exp(0.0182*x)

# Figure Band 4
plt.subplot(131)
plt.scatter (x, y)
plt.plot(np.sort(x), np.sort(fitLineB1), 'r')
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
#plot.text('$y=%3.7sx+%3.7s$'%(slope, intercept))
plt.grid(False)
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
#plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05),)

# Figure Band 2 (y = 2247.1e0.0171x)
plt.subplot(132)
plt.scatter (x, y)
plt.plot(np.sort(x), np.sort(fitLineB2), 'r')
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)

# Figure Band 3
plt.subplot(133)
plt.scatter (x, y)
plt.plot(np.sort(x), np.sort(fitLineB3), 'r')
#plt.xscale()
#plt.yscale()
plt.xlabel('Brightness Values (0-255)')
plt.ylabel('Radiance')
plt.title('Title')
plt.grid(False)

#def func(x, a, c):
#    return a*np.exp(c*(x))
#
#popt, pcov = curve_fit(func, xVals, yVals)
#popt, pcov = curve_fit(func, x, y, [100,400,0.001,0])
#print popt
#plot.text('$y=%3.7sx+%3.7s$'%(slope, intercept))
#plt.scatter(xVals, yVals)
#x=linspace(400,6000,10000))




plt.show()

dataFile.close()
