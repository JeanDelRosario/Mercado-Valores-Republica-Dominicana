#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 16:23:34 2018

@author: jeancarlos
"""
import os
import numpy as np
import pandas as pd

excels = os.listdir('/home/jeancarlos/Desktop/InversionesReservas/Excels')

columns = ['TIPO_RENTA','MS_USD','MS_USD_DOP','MS_DOP', 'FECHA_CORTE']
    
inversiones = pd.DataFrame(columns=columns)

for i in range(len(excels)):
    workbook = pd.ExcelFile('/home/jeancarlos/Desktop/InversionesReservas/Excels/'+excels[i])
    
    # get the total number of rows
    #rows = workbook.book.sheet_by_name('BB_ResumenGeneralMercado').nrows
    
    # define how many rows to read
    #nrows = 70
    #0
    # subtract the number of rows to read from the total number of rows (and another 1 for the header)
    data = pd.read_excel(workbook, sheet_name = 'BB_ResumenGeneralMercado')
    
    row = np.where(data['Unnamed: 2'].str.contains('Mdo. Secundario RF|Mdo. Secundario RV', na=False))[0]
    
    #Buscando la primera linea donde este la palabra acumulado, ya que despues de esta no 
    #me interesa ningun valor
    row_avoid = np.where(data.iloc[:,0].str.contains('Acumulado', na=False))[0][0]
    
    #Actualizando a row
    row = row[row<row_avoid]
    
    data1 = data.iloc[row,[2,4,5,6]]
    
    data1['FECHA_CORTE'] = excels[i][0:8]
    
    data1.columns = inversiones.columns
    
    inversiones = pd.concat([inversiones, data1], axis = 0, ignore_index=True)
    
    if i % 10 == 0:
        print(i)
        
