#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 15:53:38 2018

@author: jeancarlos
"""

from calendar import monthrange
import requests

link1 = 'http://bvrd.com.do/sites/default/files/bulletins/bd_new_'
link3 = '.xls'

#Looping through the months and then the days of the month
for years in [2017,2018]:
    years_str = str(years)
    print(years)
    
    for months in range(12):
        print(months)
        
        if len(str(months + 1)) < 2:
            months_str = '0' + str(months + 1)
        else:
            months_str = str(months + 1)
                
        number_days_month = monthrange(years, months + 1)[1]
        
        for days in range(number_days_month):
            
            #Add zero if necessary to beggining of days and months
            
            if len(str(days + 1)) < 2:
                days_str = '0' + str(days + 1)
            else:
                days_str = str(days + 1)
            
            
            excel_link = link1 + days_str + months_str + years_str + link3
            
            resp = requests.get(excel_link)
                
            #Instead of .xls trying with .xlsx
            if resp.status_code == 404:
                
                resp = requests.get(excel_link + 'x')
                
                #Adding a _0 that sometimes the documents get
                if resp.status_code == 404:
                    
                    resp = requests.get(link1 + days_str + months_str +years_str + '_0' + '.xlsx')
                    
                    #If none of the above work, just skip to next day (file)
                    if resp.status_code == 404:
                        
                        continue
            
            #Opening a file to save the Excel
            output = open(years_str + months_str + days_str  + link3, 'wb')
            
            #Writing content of the excel downloaded into the file
            output.write(resp.content)
            
            #Closing the file
            output.close()
