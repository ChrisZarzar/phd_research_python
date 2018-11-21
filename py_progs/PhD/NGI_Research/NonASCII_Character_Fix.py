# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:11:56 2016
Notes:  This script will find the lines that have the error,  “SyntaxError: Non-ASCII character '\xe2' in file”


@author: cmzarzar
"""

with open("I:\\Research\\py_progs\\PhD\\NGI_Research\\fileBackup.py") as fp:
    for i, line in enumerate(fp):
        if "\xe2" in line:
            print i, repr(line)