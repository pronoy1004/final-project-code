# Project

This project integrates FEMA's National Risk Index database, NASA'S GPM IMERG global precipitation database, and a Homeland Infrastructure Foundation-Level Data hospital database. Users can identify hospitals in areas of high riverine or coastal flooding risk, explore the average monthy precipitation at their locations, and identify nearby hospitals offering similar services.

## Data

FEMA National Risk Index Dataset: https://hazards.fema.gov/nri/data-resources#csvDownload. Download .csv using 'All Counties - County-level detail (Table)' under 'County Level'. The National Risk Index (NRI) is a score from 0 - 100 calculated from the expected occurrence of a given natural hazard, social vulnerability, and community resilience. The NRI is calculated for 18 types of natural hazards for every county in the US. A composite risk index encompassing the risk of all naturals hazards is also given for each county. This project considers riverine flooding, coastal flooding, and composite risk index.

NASA GPM IMERG Precipitation Dataset (non-relational database): https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_06/summary. Select 'Subset / Get Data' on right. In the pop-up, select Download Method: Get Original Files, Refine Date Range: can use any, our code was tested with data from 2015 - 2020, File Format: HDF5. Click 'Get Data'. In the pop-up, either follow instructions in 'Instructions for downloading' link (requires creating user account and using wget) or download files in list individually by right-clicking and saving. This dataset contains monthly precipitation estimates from satellite data at 0.1 degree latitude x 0.1 degree longitude resolution.

Homeland Infrastructure Foundation-Level Data Hospital Dataset: https://hifld-geoplatform.opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0/explore?location=6.916414%2C-15.457895%2C2.00&showTable=true. Click cloud-shaped 'Download' button, select 'Download' in 'CSV' box on left. This dataset contains locations and services offered by hospitals in the US.

## Build

1. Create 'hospital' database and user in Postgres. Table schemas will be created later in Python.
```
psql -U postgres postgres < setup.sql
```
2. Install Python dependencies.
```
pip install os
pip install psycopg2
pip install h5py
pip install datetime
pip install numpy
pip install tabulate
```

## Run

Explain how to run your application from the terminal. That should include the step needed to run the code that loads the data into your database (as well as any additional step needed to load your supporting dataset(s), if you're taking the course at the graduate level). Also be clear about the entry point for your application. If you've created a web application, remember to include a link to the page hosted by your application.

Example:

Load data: `python3 code/load_data.py`

Run application: `python3 code/application.py`
