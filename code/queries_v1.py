import os
from os import walk
import psycopg2
import psycopg2.extras
import h5py
from datetime import datetime
import numpy as np

# add self to functions?
# switch to user input instead of hard-coding
# print results
# check user input for errors

# Query 1: Identify hospitals in counties with river flooding or coastal flooding risk index
# above a user-defined threshold

# Query 2: Identify hospitals in counties with river flooding or coastal flooding risk index
# above a user-defined threshold and list average monthly rainfall

# Query 3: 

connection_string = "dbname='hospital' user='hospital' password='hospital'"
conn = psycopg2.connect(connection_string)

hdf5_path = "C:\\Users\\Elly Breves\\Desktop\\Elly\\RPI\\Courses\\ITWS-6250\\Final Project\\data\\gpm"

class Queries:

    def __init__(connection_string):
        conn = psycopg2.connect(connection_string)

    def read_hdf5(filename):
        f = h5py.File(filename, "r")
        timestamp = datetime.utcfromtimestamp(f['Grid']['time'][(0)])
        year = timestamp.year
        month = timestamp.month
        lat = f['Grid']['lat'][()] # 1800 x 1 array
        lon = f['Grid']['lon'][()] # 3600 x 1 array
        precip = f['Grid']['precipitation'][(0,...)] # 3600 x 1800 array
        f.close()
        return year, month, lat, lon, precip

    ### builds a dictionary with hdf5 filenames, year, month, lat, lon
    def build_hdf5_index(hdf5_path):
        file_list = {}
        (_, _, hdf5_filenames) = next(walk(hdf5_path))
        for i in range(len(hdf5_filenames)):
            print("Working on file " + str(i+1) + " of " + str(len(hdf5_filenames)) + " ...")
            [year, month, lat_array, lon_array, _] = read_hdf5(hdf5_path + "\\" + hdf5_filenames[i])
            file_list[i]={}
            file_list[i]['filename'] = hdf5_filenames[i]
            file_list[i]['year'] = year
            file_list[i]['month'] = month
            file_list[i]['lat'] = lat_array
            file_list[i]['lon'] = lon_array
        return file_list

    file_list = build_hdf5_index(hdf5_path)

    def query_1(rfld_thresh, cfld_thresh):
        cursor = conn.cursor()
        query = ("""SELECT hosp_address_info.id, name, rfldrisks, rfldriskr, cfldrisks, cfldriskr FROM hosp_address_info JOIN hosp_general_info ON hosp_address_info.id
        = hosp_general_info.id JOIN nri_risk ON countyfips = stcofips WHERE rfldrisks >= %s OR cfldrisks >= %s""")
        cursor.execute(query, (rfld_thresh, cfld_thresh))
        records = cursor.fetchall()
        return records

    def query_2(rfld_thresh, cfld_thresh, hdf5_path, file_list):
        cursor = conn.cursor()
        query = ("""SELECT hosp_address_info.id, name, rfldrisks, rfldriskr, cfldrisks, cfldriskr, ROUND(latitude, 1), ROUND(longitude, 1) FROM hosp_address_info JOIN hosp_general_info ON hosp_address_info.id
        = hosp_general_info.id JOIN nri_risk ON countyfips = stcofips WHERE rfldrisks >= %s OR cfldrisks >= %s""")
        cursor.execute(query, (rfld_thresh, cfld_thresh))
        records = cursor.fetchall()
        records_list = []
        for k in range(len(records)):
            print("Working on record " + str(k+1) + " of " + str(len(records)) + " ...")
            monthly_precip = {}
            latitude = float(records[k][6])
            longitude = float(records[k][7])
            for i in range(len(file_list)):
                lat_idx = np.searchsorted(file_list[i]['lat'], latitude, side="left")
                lon_idx = np.searchsorted(file_list[i]['lon'], longitude, side="left")
                f = h5py.File(hdf5_path + "\\" + file_list[i]['filename'], "r")
                precip = f['Grid']['precipitation'][(0,lon_idx,lat_idx)] # 3600 x 1800 array
                f.close()
                if file_list[i]['year'] not in monthly_precip:
                    monthly_precip[file_list[i]['year']] = {}
                monthly_precip[file_list[i]['year']][file_list[i]['month']] = precip
            monthly_avg = []
            for i in range(12):
                monthly_data = []
                for j in range(len(monthly_precip.keys())):
                    monthly_data.append(monthly_precip[list(monthly_precip.keys())[j]][i+1])
                monthly_avg.append(sum(monthly_data)/len(monthly_data))
            new_row = list(records[k])
            new_row.append(monthly_avg)
            records_list.append(new_row)
        return records_list

    def query_3(rfld_thresh, cfld_thresh, trauma_level, hdf5_path, file_list):
        cursor = conn.cursor()
        query = ("""SELECT hosp_address_info.id, rfldrisks, rfldriskr, cfldrisks, cfldriskr, trauma, ROUND(latitude, 1), ROUND(longitude, 1) FROM
        hosp_address_info JOIN hosp_general_info ON hosp_address_info.id = hosp_general_info.id JOIN nri_risk ON countyfips = stcofips WHERE
        (rfldrisks >= %s OR cfldrisks >= %s) AND trauma = %s""")
        cursor.execute(query, (rfld_thresh, cfld_thresh, trauma_level))
        high_risk_records = cursor.fetchall()
        query = ("""SELECT hosp_address_info.id, rfldrisks, rfldriskr, cfldrisks, cfldriskr, trauma, ROUND(latitude, 1), ROUND(longitude, 1) FROM
        hosp_address_info JOIN hosp_general_info ON hosp_address_info.id = hosp_general_info.id JOIN nri_risk ON countyfips = stcofips WHERE trauma = %s""")
        cursor.execute(query, (trauma_level,))
        all_records = cursor.fetchall()
        ################# in progress ###################
