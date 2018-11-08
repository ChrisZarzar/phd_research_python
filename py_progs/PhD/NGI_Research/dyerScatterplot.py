import csv
import numpy as np
import matplotlib.pyplot as plt

# Open data file

dataFile = open ('zarzar.csv','r')
dataArr = csv.reader (dataFile)
dataArr.next()

xVals = list()
yVals = list()

for row in dataArr:
    xVals.append (float(row[3]))
    yVals.append (float(row[4]))

# Make the figure

plt.scatter (yVals, xVals)
plt.show()

dataFile.close()
