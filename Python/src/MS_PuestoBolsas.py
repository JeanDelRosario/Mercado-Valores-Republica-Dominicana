#!/usr/bin/env python3

# coding: utf-8

# In[ ]:


import os
import pandas as pd
import numpy as np


# In[ ]:


excels = os.listdir('/home/jeancarlos/Desktop/InversionesReservas/Excels')


# In[ ]:


#Creando tabla con valores transados por puestos de bolsas en renta fija (Sin incluir market makers)
columns_names = ['MS_USD','MS_USD_DOP','MS_DOP','MS_AC_MES','MS_AC_ANO']
inversiones2 = pd.DataFrame(columns=['PUESTO']+columns_names+['FECHA_CORTE']+['RENTA'])
columns = []


# In[ ]:


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
    
    data1 = data.iloc[row,[0,2,3,4,5,6]]
    data1.columns = ['PUESTO'] + columns_names
    data1['FECHA_CORTE'] = excels[i][0:8]
    data1['RENTA'] = 1 #Renta Fija

    inversiones2 = pd.concat([inversiones2, data1], axis = 0)
    
    if i % 50 == 0:
        print(i)


# In[ ]:


inversiones2['MARKET_MAKERS'] = 0 #0 no es informacion del programa de Hacienda Market Makers

inversiones2_sorted = inversiones2.sort_values(['PUESTO','FECHA_CORTE'])

inversiones2_sorted['MES'] = inversiones2_sorted['FECHA_CORTE'].str[4:6]

inversiones2_sorted['ANO'] = inversiones2_sorted['FECHA_CORTE'].str[0:4]

inversiones2_sorted['MS_DIARIO'] = inversiones2_sorted.groupby(['PUESTO','ANO','MES'])['MS_AC_MES'].diff()

inversiones2_sorted['MS_DIARIO'][inversiones2_sorted['MS_DIARIO'].isnull()]=inversiones2_sorted['MS_AC_MES'][inversiones2_sorted['MS_DIARIO'].isnull()]

inversiones2_sorted['MS_DIARIO'][abs(inversiones2_sorted['MS_DIARIO'])<0.0001] = 0

inversiones2_sorted.to_csv('/home/jeancarlos/Desktop/InversionesReservas/inversiones.csv')


# In[ ]:


inversiones2_sorted


# In[ ]:


inversiones3 = pd.DataFrame(columns=['PUESTO']+columns_names+['FECHA_CORTE']+['RENTA'])
columns = []


# In[ ]:


for i in range(len(excels)):
    workbook = pd.ExcelFile('/home/jeancarlos/Desktop/InversionesReservas/Excels/'+excels[i])
    
    # get the total number of rows
    #rows = workbook.book.sheet_by_name('BB_ResumenGeneralMercado').nrows
    
    # define how many rows to read
    #nrows = 70
    #0
    # subtract the number of rows to read from the total number of rows (and another 1 for the header)
    data = pd.read_excel(workbook, sheet_name = 'BB_RFRegistro')
    
    row = np.where(data.iloc[:,0].str.contains('Participante|Total', na=False))[0]
    
    #Lo siguiente es para elegir siempre las filas que solo contengan informaciones de los puestos de bolsas
    
    #Primero verificamos si el documento tiene la estructura esperada
    #Esta es: dos filas con la palabra participante y una con total
    if len(row) != 3:
        print('El documento '+excels[i]+' tiene un error en su estructura')
        continue
    
    #Se eligen las filas entre la segunda vez que aparece la palabra participante y la ultima que aparece total
    row = list(range(row[1]+1,row[2]-1))
    
    data1 = data.iloc[row,[0,2,3,4,5,6]]
    data1.columns = ['PUESTO'] + columns_names
    data1['FECHA_CORTE'] = excels[i][0:8]
    data1['RENTA'] = 1 #Renta Fija

    inversiones3 = pd.concat([inversiones3, data1], axis = 0)
    
    if i % 50 == 0:
        print(i)


# In[ ]:


inversiones3['MARKET_MAKERS'] = 1 #1 es informacion del programa de Hacienda Market Makers

inversiones3_sorted = inversiones3.sort_values(['PUESTO','FECHA_CORTE'])

inversiones3_sorted['MES'] = inversiones3_sorted['FECHA_CORTE'].str[4:6]

inversiones3_sorted['ANO'] = inversiones3_sorted['FECHA_CORTE'].str[0:4]

inversiones3_sorted['MS_DIARIO'] = inversiones3_sorted.groupby(['PUESTO','ANO','MES'])['MS_AC_MES'].diff()

inversiones3_sorted['MS_DIARIO'][inversiones3_sorted['MS_DIARIO'].isnull()]=inversiones3_sorted['MS_AC_MES'][inversiones3_sorted['MS_DIARIO'].isnull()]

inversiones3_sorted['MS_DIARIO'][abs(inversiones3_sorted['MS_DIARIO'])<0.0001] = 0


# In[ ]:


inversiones3_sorted


# In[ ]:


inversiones4 = pd.DataFrame(columns=['PUESTO']+columns_names+['FECHA_CORTE']+['RENTA'])
columns = []


# In[ ]:


for i in range(len(excels)):
    workbook = pd.ExcelFile('/home/jeancarlos/Desktop/InversionesReservas/Excels/'+excels[i])
    
    # get the total number of rows
    #rows = workbook.book.sheet_by_name('BB_ResumenGeneralMercado').nrows
    
    # define how many rows to read
    #nrows = 70
    #0
    # subtract the number of rows to read from the total number of rows (and another 1 for the header)
    data = pd.read_excel(workbook, sheet_name = 'BB_RVVTransPBolsa')
    
    row = np.where(data.iloc[:,0].str.contains('Puesto de Bolsa|Total', na=False))[0]
    
    #Lo siguiente es para elegir siempre las filas que solo contengan informaciones de los puestos de bolsas
    
    #Primero verificamos si el documento tiene la estructura esperada
    #Esta es: dos filas con la palabra participante y una con total
    if len(row) != 3:
        print('El documento '+excels[i]+' tiene un error en su estructura')
        continue
    
    #Se eligen las filas entre la segunda vez que aparece la palabra participante y la ultima que aparece total
    row = list(range(row[1]+1,row[2]-1))
    
    data1 = data.iloc[row,[0,2,3,4,5,6]]
    data1.columns = ['PUESTO'] + columns_names
    data1['FECHA_CORTE'] = excels[i][0:8]
    data1['RENTA'] = 2 #Renta Variable

    inversiones4 = pd.concat([inversiones4, data1], axis = 0)
    
    if i % 50 == 0:
        print(i)


# In[ ]:


inversiones4.loc[:,'MARKET_MAKERS'] = 0

inversiones4_sorted = inversiones4.sort_values(['PUESTO','FECHA_CORTE'])

inversiones4_sorted.loc[:,'MES'] = inversiones4_sorted['FECHA_CORTE'].str[4:6]

inversiones4_sorted.loc[:,'ANO'] = inversiones4_sorted['FECHA_CORTE'].str[0:4]

inversiones4_sorted.loc[:,'MS_DIARIO'] = inversiones4_sorted.groupby(['PUESTO','ANO','MES'])['MS_AC_MES'].diff()

inversiones4_sorted.loc[inversiones4_sorted['MS_DIARIO'].isnull(),'MS_DIARIO']=inversiones4_sorted.loc[inversiones4_sorted['MS_DIARIO'].isnull(),'MS_AC_MES']

inversiones4_sorted.loc[abs(inversiones4_sorted.loc[:,'MS_DIARIO'])<0.0001,'MS_DIARIO'] = 0


# In[ ]:


#Uniendo todos los data frames creados en una sola tabla
final = pd.concat([inversiones2_sorted, inversiones3_sorted, inversiones4_sorted], axis = 0)
final
