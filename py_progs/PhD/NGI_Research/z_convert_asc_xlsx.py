# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 13:01:33 2015

@author: cmz39
"""

"""
_________________________________
The purpose of this script is to recursively search through a directory and import all files to excel

Author: Chris Zarzar

Created: 6-4-15

Edited: 6-8-15
*Changing script so that it will correctly bring in any tab seperated file to excel 
into a single, preset workbook
*Found out that the Excel document must be saved in Excel 97-2003 format to work (xls)

__________________________________

"""
import os
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
workbook = raw_input("Enter the name of the excel workbook you created to put the data (use the format C:\\user\\...\Workbook.xls):")        
rootdir = raw_input("Enter the directory which holds the subdirectories of the radiometric data (use the format C:\\user\\...):")   
for root, dirnames, files in os.walk(rootdir):    
    for files in fnmatch.filter(files, '*.asc'): 
        fname = (os.path.join(root,files))
        sheet = os.path.basename(fname[:-4]) #this grabs the name of the file I am working with and will use it to name the sheets
        
        style = xlwt.XFStyle()
        style.num_format_str = '#,###0.00'  
        
        f = open(fname, 'r+')
        row_list = []
        for row in f:
            row_list.append(row.split())
        column_list = zip(*row_list)
        rb = xlrd.open_workbook(workbook,formatting_info=True) #open the workbook I want to eventually work with
        wb = copy(rb) #create a temporary workbook to do write into
        ws = wb.add_sheet(sheet) #add a new sheet to the temporary wrinting workbook
        i = 0
        for column in column_list:
            for item in range(len(column)):
                value = column[item].strip()
                if is_number(value):
                    ws.write(item, i, float(value), style=style)
                else:
                    ws.write(item, i, value)
            i+=1
            
        wb.save(workbook) # Save the updated workbook
