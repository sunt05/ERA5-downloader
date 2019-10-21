# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:47:33 2019

@author: tyh
"""
import pandas as pd
df_input=pd.read_csv('cq_2013_data_60.txt',sep='\s+')
from netCDF4 import Dataset
import pathlib
import time
p = pathlib.Path('.')
path=p.rglob('*2013*sfc*.nc')
#for i in path:
#    print(i)
#    nc=Dataset(i)
def u10(nc):
    
#    kdown=nc.variables['strd'][:,0,0]
    time=nc.variables['time'][:,]
    u10=nc.variables['u10'][:,0,0]
    v10=nc.variables['v10'][:,0,0]
#    d2m=nc.variables['d2m'][:,0,0]
#    pd.to_datetime(time)
    #timeStamp = 
    #pd.Timestamp(1, unit='h',stapd.Timestamprt='1900')
    
    df1=pd.DataFrame(data=((v10.data**2+u10.data**2)**0.5),columns=['u10'])
    df1['datatime']=pd.to_datetime(
                pd.to_datetime(
                    190001, format='%Y%m')+ pd.to_timedelta(
                    time.data, unit='h'))
    
    df1.set_index('datatime',inplace=True)
    return df1

df=pd.concat(u10(Dataset(i))  for i in p.rglob('*2013*sfc*.nc'))
    
