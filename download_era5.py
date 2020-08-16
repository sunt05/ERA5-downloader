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

sp.show_version()

#%%
path_root = Path(".").resolve()
os.chdir(path_root)

#%%
df_request = pd.read_csv(
    "site_request.csv",
    dtype={
        "latitude": float,
        "longitude": float,
        "start": str,
        "end": str,
        "scale": int,
    },
)

#%%
path_data = path_root / "data"

#%%
for ind in df_request.index:
    lat_x, lon_x = df_request.loc[ind, ["latitude", "longitude"]]
    scale_x = df_request.loc[ind, "scale"]
    grid = [0.125, 0.125]

    lat_c, lon_c = (roundPartial(x, grid[0]) for x in [lat_x, lon_x])
    lat_x, lon_x = lat_c, lon_c
    # identify the upper-left grid for naming
    # lat_x = lat_x + grid[0] * scale_x
    # lon_x = lon_x - grid[0] * scale_x

    lat_x = f"{lat_x}N" if lat_x > 0 else f"{-lat_x}S"
    lon_x = f"{lon_x}E" if lon_x > 0 else f"{-lon_x}W"

    # create data folder
    path_x = path_data / f"{lat_x}{lon_x}"
    if not path_x.exists():
        path_x.mkdir(parents=True)
    os.chdir(path_x)

    start_x, end_x = df_request.loc[ind, ["start", "end"]]
    logger_supy.info(
        f"working on {lat_c}, {lon_c}, {start_x}, {end_x}, area size: {scale_x}:"
    )

    try:
        # examine if requested files have already been downloaded
        list_fn_sfc, list_fn_ml = load_filelist_era5(
            lat_c, lon_c, start_x, end_x, grid=grid, scale=scale_x
        )
        list_existq = [Path(fn).exists() for fn in list_fn_sfc + list_fn_ml]
        if np.all(list_existq):
            logger_supy.info(f"requested files are existing!")
        else:
            raise FileNotFoundError("some of the requested files are missing")
    except:
        logger_supy.info(f"downloading started!")
        # download requested files then exit otherwise GH would timeout for many requests
        dict_era5 = sp.util.download_era5(
            lat_c, lon_c, start_x, end_x, grid=grid, scale=scale_x
        )
        break

    # list_fn_forcing=sp.util.gen_forcing_era5(lat_c,lon_c,start_x,end_x)

    os.chdir(path_root)

#%%
