# Project

This project integrates FEMA's National Risk Index database, NASA'S GPM IMERG global precipitation database, and a Homeland Infrastructure Foundation-Level Data hospital database. Users can identify hospitals in areas of high riverine or coastal flooding risk, explore the average monthy precipitation at their locations, and identify nearby hospitals offering similar services.

## Data

FEMA National Risk Index Dataset: https://hazards.fema.gov/nri/data-resources#csvDownload. Download .csv from 'All Counties - County-level detail (Table)' under 'County Level'. The National Risk Index (NRI) is a score from 0 - 100 calculated from the expected occurrence of a given natural hazard, social vulnerability, and community resilience. The NRI is calculated for 18 types of natural hazards for every county in the US. A composite risk index encompassing the risk of all 18 naturals hazards is also given for each county. This project considers riverine flooding, coastal flooding, and composite risk index.

NASA GPM IMERG Precipitation Dataset (non-relational database): https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_06/summary. Multiple steps are required to download. Data from 2015 - 2020 are available here: https://rpi.box.com/s/5poa05avnfixpbsrb01dd354crex2hzv. Alternatively, go to above NASA url, select 'Subset / Get Data' on right. In the pop-up, select Download Method: Get Original Files, Refine Date Range: can use any, our code was tested with data from 2015 - 2020, File Format: HDF5. Click 'Get Data'. In the pop-up, either follow instructions in 'Instructions for downloading' link (requires creating user account and using wget) or download files in list individually by right-clicking and saving. This dataset contains monthly precipitation estimates from satellite data at 0.1 degree latitude x 0.1 degree longitude resolution.

Homeland Infrastructure Foundation-Level Data Hospital Dataset: https://hifld-geoplatform.opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0/explore?location=6.916414%2C-15.457895%2C2.00&showTable=true. Click cloud-shaped 'Download' button, select 'Download' in 'CSV' box on left. This dataset contains locations and services offered by hospitals in the US.

## Build

1. Create 'hospital' database and user in Postgres. Table schemas will be created later in Python. A 'schema.sql' file is provided to show the schema, but this file should not be run.
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
3. The code looks for NRI and hospital .csv files in the data directory. HDF5 files from the precipitation dataset should be located in data/gpm. Only HDF5 files should exist in that folder.

## Run

1. Load hospital and NRI data into Postgres and create user log tables. Change path to 'nri_filename' and 'hospital_filename' in lines 3 and 4 if necessary. Precipitation data in HDF5 format will be loaded by the application. Change 'hdf5_path' in line 12 of database.py if necessary.
```
python3 code/load_data.py
```
2. Run application. 
```
python3 code/application.py
```
3. Register or login. If using for the first time, select '2' to register at the prompt. Enter a username. Then enter '1' to login with your username at the prompt.
4. Select a query from the menu and enter the required parameters at the prompt.
5. Login is required for each new query.
6. User logs (user_data and user_activity_log) can be viewed in Postgres.
