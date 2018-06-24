#!/usr/bin/env python3

# coding: utf-8

# In[ ]:


import os
import numpy as np
import pandas as pd


# In[ ]:


excels = os.listdir('/home/jeancarlos/Desktop/InversionesReservas/Excels')


# In[ ]:


#En esta parte se creera la tabla para obtener lo transado diario en el mercado secundario
#Tanto renta fija como renta variable (Sin incluir market makers)
columns = ['TIPO_RENTA','MS_USD','MS_USD_DOP','MS_DOP','TOTAL_DOP', 'FECHA_CORTE']
    
inversiones = pd.DataFrame(columns=columns)


# In[ ]:


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
    
    data1 = data.iloc[row,[2,4,5,6,7]]
    
    data1['FECHA_CORTE'] = excels[i][0:8]
    
    data1.columns = inversiones.columns
    
    inversiones = pd.concat([inversiones, data1], axis = 0, ignore_index=True)
    
    if i % 10 == 0:
        print(i)


# In[ ]:


inversiones['RENTA'] = np.where(inversiones['TIPO_RENTA'].str.contains('RF'), 1, 2) #1 Renta Fija, 2 Renta Variable
inversiones.loc[:,'MARKET_MAKERS'] = 0
inversiones = inversiones.iloc[:,1:]


# In[ ]:


inversiones


# In[ ]:


#Se creera una tabla con lo transado diario por el programa market makers de Ministerio de Hacienda
columns = ['MS_USD','MS_USD_DOP','MS_DOP','TOTAL_DOP', 'FECHA_CORTE']
    
market_makers = pd.DataFrame(columns=columns)


# In[ ]:


for i in range(len(excels)):
    workbook = pd.ExcelFile('/home/jeancarlos/Desktop/InversionesReservas/Excels/'+excels[i])
    
    # get the total number of rows
    #rows = workbook.book.sheet_by_name('BB_ResumenGeneralMercado').nrows
    
    # define how many rows to read
    #nrows = 70
    #0
    # subtract the number of rows to read from the total number of rows (and another 1 for the header)
    data = pd.read_excel(workbook, sheet_name = 'BB_ResOpesRepRegistro')
    
    row = np.where(data.iloc[:,0].str.contains('Mercado de Renta Fija', na=False))[0]
    
    #Buscando la primera linea donde este la palabra acumulado, ya que despues de esta no 
    #me interesa ningun valor
    row_avoid = np.where(data.iloc[:,0].str.contains('Acumulado', na=False))[0][0]
    
    #Actualizando a row
    row = row[row<row_avoid]
    
    data1 = data.iloc[row,[3,5,6,7]]
    
    data1['FECHA_CORTE'] = excels[i][0:8]
    
    data1.columns = market_makers.columns
    
    market_makers = pd.concat([market_makers, data1], axis = 0, ignore_index=True)
    
    #if i % 10 == 0:
    #    print(i)


# In[ ]:


market_makers.loc[:,'RENTA'] = 1  #1 Renta Fija
market_makers.loc[:,'MARKET_MAKERS'] = 1
market_makers


# In[ ]:


transado = pd.concat([inversiones, market_makers], axis = 0)


# In[ ]:


transado
