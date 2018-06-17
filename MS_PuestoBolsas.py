#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 02:15:23 2018

@author: jeancarlos
"""
import os
import pandas as pd
import numpy as np


excels = os.listdir('/home/jeancarlos/Desktop/InversionesReservas/Excels')

columns_names = ['MS_RF_USD','MS_RF_USD_DOP','MS_RF_DOP','MS_RF_AC_MES','MS_RF_AC_ANO']
puestos = ['ALPHA', 'ATLANBBA', 'BHDVAL','INRES', 'CCI','CITIV','EXCEL','IPSA',
           'JMMB','PARVA','PCMDOM']

inversiones2 = pd.DataFrame(columns=['puesto']+columns_names+['fecha_corte'])

columns = []
#Competidores
for i in range(len(excels)):
    workbook = pd.ExcelFile('/home/jeancarlos/Desktop/InversionesReservas/Excels/'+excels[i])
    
    # get the total number of rows
    #rows = workbook.book.sheet_by_name('BB_ResumenGeneralMercado').nrows
    
    # define how many rows to read
    #nrows = 70
    #0
    # subtract the number of rows to read from the total number of rows (and another 1 for the header)
    data = pd.read_excel(workbook, sheet_name = 'BB_RFMSVTPBolsa')
    
    row = np.where(data.iloc[:,0].str.contains('ALPHA|ATLANBBA|BHDVAL|INRES|CCI|CITIV|EXCEL|IPSA|JMMB|PARVA|PCMDOM', na=False))[0]
    
    puestos_bolsa = list(data.iloc[row,0])
    
    data1 = data.iloc[row,[0,2,3,4,5,9]]
    data1.columns = ['puesto'] + columns_names
    data1['fecha_corte'] = excels[i][0:8]

    inversiones2 = pd.concat([inversiones2, data1], axis = 0)
    
    if i % 10 == 0:
        print(i)
    
inversiones2_sorted = inversiones2.sort_values(['puesto','fecha_corte'])

inversiones2_sorted['mes'] = inversiones2_sorted['fecha_corte'].str[0:2]

inversiones2_sorted['MS_RF_DIARIO'] = inversiones2_sorted.groupby(['puesto','mes'])['MS_RF_AC_MES'].diff()

inversiones2_sorted['MS_RF_DIARIO'][inversiones2_sorted['MS_RF_DIARIO'].isnull()]=inversiones2_sorted['MS_RF_AC_MES'][inversiones2_sorted['MS_RF_DIARIO'].isnull()]

inversiones2_sorted['MS_RF_DIARIO'][abs(inversiones2_sorted['MS_RF_DIARIO'])<0.0001] = 0

inversiones2_sorted.to_csv('/home/jeancarlos/Desktop/InversionesReservas/inversiones.csv')
