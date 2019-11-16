# ERA5 Downloader
Download ERA5 data at near surface levels to drive land surface models.

## What are included?

``` bash
# tree  -L 1
.
├── README.md # this file
├── data # downloaded data
├── download_era5.py # main script to download ERA5 data
├── site_request.csv # request info for CDS API
└── test-cds.py # example script to test CDS API

```

## How to use this repo?

This repo is set up to use GitHub Actions to automatically download ERA5 data.

To trigger download, one just need to modify `site_request.csv`, which has the format:

```csv
latitude,longitude,start,end,scale
51,1,19790101,19890101,0
```

These headings are the same as arguments set in [`supy.util.download_era5`](https://supy.readthedocs.io/en/latest/api/supy.util/supy.util.download_era5.html#supy.util.download_era5).

The download task is handled by `download_era5.py`, which will loop over all records in `site_request.csv` to get the requested data.

> Note:
> Given the limit by GitHub Actions, it is suggested to set a time span of <1 year in each request; otherwise no data would be effectively pushed back to the repo.

