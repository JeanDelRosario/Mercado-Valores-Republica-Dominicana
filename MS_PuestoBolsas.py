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

inversiones2 = pd.DataFrame(columns=['PUESTO']+columns_names+['FECHA_CORTE'])

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
    
    row = np.where(data.iloc[:,0].str.contains('Participante|Total', na=False))[0]
    
    #Lo siguiente es para elegir siempre las filas que solo contengan informaciones de los puestos de bolsas
    
    #Primero verificamos si el documento tiene la estructura esperada
    #Esta es: dos filas con la palabra participante y una con total
    if len(row) != 3:
        print('El documento '+excels[i]+' tiene un error en su estructura')
        continue
    
    #Se eligen las filas entre la segunda vez que aparece la palabra participante y la ultima que aparece total
    row = list(range(row[1]+1,row[2]-1))
    
    data1 = data.iloc[row,[0,2,3,4,5,9]]
    data1.columns = ['PUESTO'] + columns_names
    data1['FECHA_CORTE'] = excels[i][0:8]

    inversiones2 = pd.concat([inversiones2, data1], axis = 0)
    
    if i % 10 == 0:
        print(i)
    
    
inversiones2_sorted = inversiones2.sort_values(['PUESTO','FECHA_CORTE'])

inversiones2_sorted['MES'] = inversiones2_sorted['FECHA_CORTE'].str[0:2]

inversiones2_sorted['MS_RF_DIARIO'] = inversiones2_sorted.groupby(['PUESTO','MES'])['MS_RF_AC_MES'].diff()

inversiones2_sorted['MS_RF_DIARIO'][inversiones2_sorted['MS_RF_DIARIO'].isnull()]=inversiones2_sorted['MS_RF_AC_MES'][inversiones2_sorted['MS_RF_DIARIO'].isnull()]

inversiones2_sorted['MS_RF_DIARIO'][abs(inversiones2_sorted['MS_RF_DIARIO'])<0.0001] = 0

inversiones2_sorted.to_csv('/home/jeancarlos/Desktop/InversionesReservas/inversiones.csv')
