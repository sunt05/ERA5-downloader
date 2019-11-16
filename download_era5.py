#!/usr/bin/env python
#%%
# load packages
import supy as sp
import numpy as np
import pandas as pd
from pathlib import Path
import os
from supy.util._era5 import roundPartial, load_filelist_era5
from supy._env import logger_supy

#%%
path_root = Path('.').resolve()
os.chdir(path_root)

#%%
df_request = pd.read_csv('site_request.csv',
                         dtype={
                             'latitude': float,
                             'longitude': float,
                             'start': str,
                             'end': str,
                             'scale': int
                         })

#%%
path_data = path_root / 'data'

#%%
for ind in df_request.index:
    lat_x, lon_x = df_request.loc[ind, ['latitude', 'longitude']]
    grid = [0.125, 0.125]

    lat_c, lon_c = (roundPartial(x, grid[0]) for x in [lat_x, lon_x])

    lat_x = f'{lat_c}N' if lat_c > 0 else f'{-lat_c}S'
    lon_x = f'{lon_c}E' if lon_c > 0 else f'{-lon_c}W'
    path_x = path_data / f'{lat_x}{lon_x}'
    if not path_x.exists():
        path_x.mkdir(parents=True)
    os.chdir(path_x)

    start_x, end_x = df_request.loc[ind, ['start', 'end']]

    # note: `scale` is currently not used.
    scale_x = df_request.loc[ind, 'scale']

    logger_supy.info(f'working on {lat_c}, {lon_c}, {start_x}, {end_x}:')

    try:
        # examine if requested files have already been downloaded
        list_fn_sfc, list_fn_ml = load_filelist_era5(lat_c, lon_c, start_x,
                                                     end_x)
        logger_supy.info(f'requested files are existing!')
    except:
        logger_supy.info(f'downloading started!')
        # download requested files then exit otherwise GH would timeout for many requests
        dict_era5 = sp.util.download_era5(lat_c, lon_c, start_x, end_x)
        break

    # list_fn_forcing=sp.util.gen_forcing_era5(lat_c,lon_c,start_x,end_x)

    os.chdir(path_root)

#%%
