# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:47:33 2019

@author: tyh
"""
import atmosp
import pandas as pd
#df_input=pd.read_csv('cq_2013_data_60.txt',sep='\s+')
from netCDF4 import Dataset
import pathlib
import time

g0=9.80665
global columns
columns=['iy', 'id', 'it', 'imin', 'qn', 'qh', 'qe', 'qs', 'qf', 'U', 'RH',
       'Tair', 'pres', 'rain', 'kdown', 'snow', 'ldown', 'fcld', 'wuh', 'xsmd',
       'lai', 'kdiff', 'kdir', 'wdir']

#for i in path:
#    print(i)
#    nc=Dataset(i)
def sfc(nc): 
    
#    kdown=nc.variables['strd'][:,0,0]
    time=nc.variables['time'][:,]
#    u10=nc.variables['u10'][:,0,0]
#    v10=nc.variables['v10'][:,0,0]
    sp=nc.variables['sp'][:,0,0]
    ssrd=nc.variables['ssrd'][:,0,0]/3600   #Surface solar radiation downwards J m**-2
    z=nc.variables['z'][:,0,0]                         #geopotential m**2 s**-2
    t2m=nc.variables['t2m'][:,0,0]      #2 metre temperature K
    d2m=nc.variables['d2m'][:,0,0]      #2 metre dewpoint temperature K
    tp=nc.variables['tp'][:,0,0]*1000
    strd=nc.variables['strd'][:,0,0]/3600 #Surface thermal radiation downwards

#    print (nc.variables['level'][:])
#    d2m=nc.variables['d2m'][:,0,0]
#    pd.to_datetime(time)
    #timeStamp = 
    #pd.Timestamp(1, unit='h',stapd.Timestamprt='1900')
    
    df=pd.DataFrame(data=(sp),columns=['sp'])
    df['z']=z
    df['t2m']=t2m
    df['d2m']=d2m
    df['ssrd']=ssrd
    df['ssrd'][df['ssrd']<0.1]=0
    df['tp']=tp
    df['strd']=strd

#    df1=pd.DataFrame(data=((v10.data**2+u10.data**2)**0.5),columns=['u10'])
    df['datatime']=pd.to_datetime(
                pd.to_datetime(
                    190001, format='%Y%m')+ pd.to_timedelta(
                    time.data, unit='h')+ pd.to_timedelta(
                    8, unit='h'))
    df['RH']=atmosp.calculate(

        "RH",

        T=df['t2m'].values,

        Td=(df['d2m'].values),

        p=df['sp'].values)
    
    df.set_index('datatime',inplace=True)
    return df
def ml(nc):
    
#    kdown=nc.variables['strd'][:,0,0]
    time=nc.variables['time'][:,]
    u=nc.variables['u'][:,0,0]
    v=nc.variables['v'][:,0,0]
    t=nc.variables['t'][:,0,0]
    q=nc.variables['q'][:,0,0]
    z=nc.variables['z'][:,0,0] 
    p=nc.variables['level'][0]/10
    
#    print (nc.variables['level'][:])
#    d2m=nc.variables['d2m'][:,0,0]
#    pd.to_datetime(time)
    #timeStamp = 
    #pd.Timestamp(1, unit='h',stapd.Timestamprt='1900')
    
    df=pd.DataFrame(data=((v.data**2+u.data**2)**0.5),columns=['U'])
    df['z']=z
    df['t']=t
    df['q']=q
    df['p']=p
    df['datatime']=pd.to_datetime(
                pd.to_datetime(
                    190001, format='%Y%m')+ pd.to_timedelta(
                    time.data, unit='h')+ pd.to_timedelta(
                    8, unit='h'))
    df['RH']=atmosp.calculate(

        "RH",

        T=df['t'].values,

        qv=(df['q'].values),

#        RH=df_tmy['RH2'].values,

        rho=1.23)

    df.set_index('datatime',inplace=True)
    return df
def gen_input_data(df_sfc,df_ml,year):
    df1_sfc=df_sfc.loc[str(year)+' 1 1 01':str(year+1)+' 1 1 00']
    df1_ml=df_ml.loc[str(year)+' 1 1 01':str(year+1)+' 1 1 00']
    df_out=pd.DataFrame(data=df1_sfc.index.values,columns=['datetime'])
    df_out.set_index('datetime',inplace=True)
    df_out['iy']=df_out.index.year
    df_out['id']=df_out.index.dayofyear
    df_out['it']=df_out.index.hour
    df_out['imin']=df_out.index.minute
    for var in ['qn','qh','qe','qs','qf','fcld', 'wuh', 'xsmd',
       'lai', 'kdiff', 'kdir', 'wdir','snow']:
        df_out[var]=-999
    df_out['U']=df1_ml['U']
    df_out['RH']=df1_ml['t']
    df_out['Tair']=df1_ml['t']-273.15
    df_out['pres']=df1_ml['p']
    df_out['kdown']=df1_sfc['ssrd']
    df_out['rain']=df1_sfc['tp']
    df_out['ldown']=df1_sfc['strd']
    df_out=df_out[columns]
    return df_out
def gen_data_from_era5(path,year,filecode):
    df_sfc=pd.concat(sfc(Dataset(i))  for i in path.glob('*sfc*.nc'))
    df_ml=pd.concat(ml(Dataset(i))  for i in path.glob('*ml*.nc'))
    h=(df_sfc.sp/100-df_ml.p)/g0
    print(h.mean())
    df_out=gen_input_data(df_sfc,df_ml,year).round(2)
    df_out.reset_index(drop=True,inplace=True)
    out_path='./output/'+filecode+'_'+str(year)+'_data_60.txt'
    df_out.to_csv(out_path,sep=' ')
    return out_path,h.mean()
if __name__ == '__main__':    
    p = pathlib.Path('.')
    path=(p/'data'/'29.625N106.5E')
    gen_data_from_era5(path,2013,'cq')


    





