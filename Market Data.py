# -*- coding: utf-8 -*-
"""
Datos de Mercado con Pandas
Datos Deutsche Bank Ger.

"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

# Input
ric = 'DBK.DE'   # DBK.DE -  MXN=X

# Obtener Datos de Mercado - Get Market Data
path = 'C:\\Users\casa\\Downloads\\Finanzas Cuantitativas Py\\Bases de Datos\\' +ric+ '.csv'
table_raw = pd.read_csv(path) 


#Crear la tabla de Rendimientos - create table of returns
t = pd.DataFrame()
t['date'] = pd.to_datetime(table_raw['Date'], dayfirst=True)
t['close'] = table_raw['Close']
t.sort_values(by='date', ascending=True)
t['close_previous'] = table_raw['Close'].shift(1)
t['returns_close'] = t['close']/t['close_previous'] -1 
t = t.dropna()
t = t.reset_index(drop=True)

# Plot Timeseries of Prices - Gráfica de Series de Tiempo del Precio 
plt.figure()
plt.plot(t['date'],t['close'])
plt.title('Time Series Real Prices' + ric)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()


# Input para Jarque-Bera
x = t['returns_close'].values           #Returns - Array
x_str = 'Real_returns' + ric       #Etiquetas - Label RIC
x_size = len(x)      #Tamaño de los Rendimientos - Size of Returns 



# Compute "Risk Metrics"
x_mean = np.mean(x)
x_stdev = np.std(x)    #Volatility 
x_skew = skew(x)
x_kurt = kurtosis(x) # excess kurtosis 
x_sharpe = x_mean / x_stdev * np.sqrt(252)
x_var_95 = np.percentile(x,5)
x_cvar_95 = np.mean(x[x <= x_var_95]) 
jb = x_size/6*(x_skew**2 + 1/4*x_kurt**2)
p_value = 1 - chi2.cdf(jb, df=2) #Degree Freedom 
is_normal = (p_value > 0.05 ) #Equivalenty x_jarque_bera < 6



# Print Metrics
print('mean ' + str(x_mean))
print('std ' + str(x_stdev))
print('skewness ' + str(x_skew))
print('kurtosis ' + str(x_kurt))
print('sharpe ' + str(x_sharpe))  
print('VaR 95% ' + str (x_var_95))
print('CVaR 95% ' + str (x_cvar_95))
print('Jarque-Bera ' + str(jb))
print('p_value ' + str(p_value))
print('is_normal ' + str(is_normal))




# plot histogram
plt.figure()
plt.hist(x,bins=100)
plt.title('Histogram ' + x_str)
plt.show()
























