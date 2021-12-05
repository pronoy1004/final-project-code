# Project

This project integrates FEMA's National Risk Index database, NASA'S GPM IMERG global precipitation database, and a Homeland Infrastructure Foundation-Level Data hospital database. Users can identify hospitals in areas of high riverine or coastal flooding risk, explore the average monthy precipitation at their locations, and identify nearby hospitals offering similar services.

## Data

FEMA National Risk Index Dataset: https://hazards.fema.gov/nri/data-resources#csvDownload. Download .csv using 'All Counties - County-level detail (Table)' under 'County Level'.

NASA GPM IMERG Precipitation Dataset: https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_06/summary. Select 'Subset / Get Data' on right. In the pop-up, select Download Method: Get Original Files, Refine Date Range: Can use any, our code was tested with data from 2015 - 2020, File Format: HDF5. Click 'Get Data'. In the pop-up, either follow instructions in 'Instructions for downloading' link (requires creating user account and using wget) or download files in list individually by right-clicking and saving.

Homeland Infrastructure Foundation-Level Data Hospital Dataset: https://hifld-geoplatform.opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0/explore?location=6.916414%2C-15.457895%2C2.00&showTable=true. Click cloud-shaped 'Download' button, select 'Download' in 'CSV' box on left.

## Build

1. Create 'hospital' database and user in Postgres: As user 'Postgres', run 

List the steps needed to build your application from the terminal. That should include the step needed to install dependencies (including your non-relational datastore).

You should also include the step needed to set up the database and configure your schema. Assume a clean Postgres install.

Example:

```
psql -U postgres postgres < setup.sql
psql -U myAppAdmin appDatabase < schema.sql

pip install
```

## Run

Explain how to run your application from the terminal. That should include the step needed to run the code that loads the data into your database (as well as any additional step needed to load your supporting dataset(s), if you're taking the course at the graduate level). Also be clear about the entry point for your application. If you've created a web application, remember to include a link to the page hosted by your application.

Example:

Load data: `python3 code/load_data.py`

Run application: `python3 code/application.py`
