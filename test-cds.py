#!/usr/bin/env python
import cdsapi
from pathlib import Path

print('cdsapirc:')
with open(Path('~/.cdsapirc').expanduser(), 'r') as fin:
    print(fin.read())

c = cdsapi.Client()
c.retrieve(
    "reanalysis-era5-pressure-levels",
           {
               "variable": "temperature",
               "pressure_level": "1000",
               "product_type": "reanalysis",
               "year": "2008",
               "month": "01",
               "day": "01",
               "time": "12:00",
               "format": "grib"
           },
           "download.grib")
