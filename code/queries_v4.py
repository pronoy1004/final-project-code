import os
from os import walk
import psycopg2
import psycopg2.extras
import h5py
from datetime import datetime
import numpy as np
from tabulate import tabulate

# block after ### get number of logins ### is new
# 'query_*_insert' functions are new

# add self to functions?
# prompt for user input
# change to relative paths
# print results
# check user input for errors
# user log insertions
# add more attributes to outputs (include hospital name and address instead of just ID)?
# add function allowing user to view their entries in the user activity log table

# Query 1: Identify hospitals in counties with river flooding or coastal flooding risk index
# above a user-defined threshold

# Query 2: Identify hospitals in counties with river flooding or coastal flooding risk index
# above a user-defined threshold and list average monthly rainfall.

# Query 3: Identify hospitals in counties with river flooding risk index above a user-defined
# threshold. For each high-risk hospital, identify hospitals of the same type within the same state with
# river flooding risk index below a user-defined threshold and within a user-defined mile radius.

# Query 4: List states in order of largest population living in counties with total risk above
# a user-defined threshold.

# Query 5: Display the number of hospitals per county in counties with risk of any natural disaster above a
# user-defined threshold and with population above a user-defined threshold, ordered by descending population.

connection_string = "dbname='hospital' user='hospital' password='hospital'"
conn = psycopg2.connect(connection_string)

### get number of logins ###
cursor = conn.cursor()
dsn_param = conn.get_dsn_parameters()
query = ("""SELECT * FROM user_data WHERE user_name = %s""")
cursor.execute(query, (dsn_param['user'],))
records = cursor.fetchall()
if len(records) == 0:
    login_count = 1
elif len(records) == 1:
    login_count = records[0][2] + 1

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
        headers = ['ID', 'Name', 'River Flood Score', 'River Flood Rating', 'Coastal Flood Score', 'Coastal Flood Rating']
        table = [[records[i][0], records[i][1], round(float(records[i][2]),2), records[i][3], round(float(records[i][4]),2), records[i][5]] for i in range(0, len(records))]
        print(tabulate(table, headers))
        return records

    def query_1_insert(rfld_thresh, cfld_thresh):
        cursor = conn.cursor()
        dsn_param = conn.get_dsn_parameters()
        #query = ("""SELECT * FROM user_activity_log WHERE user_name = %s""")
        #cursor.execute(query, (dsn_param['user'],))
        #records = cursor.fetchall()
        #if len(records) = 0:
            #login_count = 1
        #if len(records) = 1:
            #login_count = records[0][3] + 1
        query = ("""INSERT INTO user_data(user_name, password, login_count) VALUES (%s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 'private', login_count))
        conn.commit()
        param_string = str(rfld_thresh) + ", " + str(cfld_thresh)
        query = ("""INSERT INTO user_activity_log(user_name, query_run, tables_accessed, input_params, login_count) VALUES (%s, %s, %s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 1, "hosp_address_info, hosp_general_info, nri_risk", param_string, login_count))
        conn.commit()
        
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
        headers = ['ID', 'Name', 'River Flood Score', 'River Flood Rating', 'Coastal Flood Score', 'Coastal Flood Rating', 'Latitude', 'Longitude', 'Precip Jan',
                   'Precip Feb', 'Precip Mar', 'Precip Apr', 'Precip May', 'Precip Jun', 'Precip Jul', 'Precip Aug', 'Precip Sep', 'Precip Oct', 'Precip Nov',
                   'Precip Dec']
        table = [[records_list[i][0], records_list[i][1], round(float(records_list[i][2]),2), records_list[i][3], round(float(records_list[i][4]),2),
                  records_list[i][5], round(float(records_list[i][6]),2), round(float(records_list[i][7]),2), round(float(records_list[i][8][0]),2),
                  round(float(records_list[i][8][1]),2), round(float(records_list[i][8][2]),2), round(float(records_list[i][8][3]),2),
                  round(float(records_list[i][8][4]),2), round(float(records_list[i][8][5]),2), round(float(records_list[i][8][6]),2),
                  round(float(records_list[i][8][7]),2), round(float(records_list[i][8][8]),2), round(float(records_list[i][8][9]),2),
                  round(float(records_list[i][8][10]),2), round(float(records_list[i][8][11]),2)] for i in range(0, len(records_list))]
        print(tabulate(table, headers))
        return records_list

    def query_2_insert(rfld_thresh, cfld_thresh):
        cursor = conn.cursor()
        dsn_param = conn.get_dsn_parameters()
        query = ("""INSERT INTO user_data(user_name, password, login_count) VALUES (%s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 'private', login_count))
        conn.commit()
        param_string = str(rfld_thresh) + ", " + str(cfld_thresh)
        query = ("""INSERT INTO user_activity_log(user_name, query_run, tables_accessed, input_params, login_count) VALUES (%s, %s, %s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 2, "hosp_address_info, hosp_general_info, nri_risk, precip", param_string, login_count))
        conn.commit()

    def query_3(rfld_high, rfld_low, mile_radius):
        lat_range = mile_radius/69
        lon_range = mile_radius/53 #at 40 degrees latitude
        cursor = conn.cursor()
        query = ("""CREATE VIEW hosp_combined AS SELECT hosp_general_info.id, NAICS_DESC, state, rfldrisks, latitude, longitude FROM hosp_general_info 
        JOIN hosp_address_info ON hosp_general_info.id = hosp_address_info.id JOIN nri_risk ON countyfips = stcofips;""")
        cursor.execute(query)
        conn.commit()
        query = ("""SELECT c1.id, c2.id, c1.NAICS_DESC, c1.state, c1.rfldrisks, c2.rfldrisks
                FROM hosp_combined c1, hosp_combined c2
                WHERE c1.NAICS_DESC = c2.NAICS_DESC AND c1.state = c2.state AND c1.id <> c2.id AND c1.rfldrisks >= %s AND c2.rfldrisks <= %s
                AND ABS(c1.latitude - c2.latitude) <= %s AND ABS(c1.longitude - c2.longitude) <= %s
                ORDER BY c1.rfldrisks DESC, c1.id, c2.rfldrisks;""")
        cursor.execute(query, (rfld_high, rfld_low, lat_range, lon_range))
        records = cursor.fetchall()
        headers = ['ID', 'ID', 'NAICS Description', 'State', 'River Flood Score', 'River Flood Score']
        table = [[records[i][0], records[i][1], records[i][2], records[i][3], round(float(records[i][4]),2), round(float(records[i][5]),2)] for i in range(0, len(records))]
        print(tabulate(table, headers))
        return records

    def query_3_insert(rfld_high, rfld_low, mile_radius):
        cursor = conn.cursor()
        dsn_param = conn.get_dsn_parameters()
        query = ("""INSERT INTO user_data(user_name, password, login_count) VALUES (%s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 'private', login_count))
        conn.commit()
        param_string = str(rfld_high) + ", " + str(rfld_low) + ", " + str(mile_radius)
        query = ("""INSERT INTO user_activity_log(user_name, query_run, tables_accessed, input_params, login_count) VALUES (%s, %s, %s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 3, "hosp_address_info, hosp_general_info, nri_risk", param_string, login_count))
        conn.commit()

    def query_4(risk_thresh):
        cursor = conn.cursor()
        query = ("""SELECT stateabbrv, sum(population) as at_risk_population
            FROM nri_risk JOIN nri_demographics ON nri_risk.stcofips = nri_demographics.stcofips JOIN nri_county ON nri_demographics.stcofips = nri_county.stcofips
            WHERE riskscore >= %s
            GROUP BY stateabbrv
            ORDER BY at_risk_population DESC;""")
        cursor.execute(query, (risk_thresh,))
        records = cursor.fetchall()
        headers = ['State', 'At-risk Population']
        table = [[records[i][0], records[i][1]] for i in range(0, len(records))]
        print(tabulate(table, headers))
        return records

    def query_4_insert(risk_thresh):
        cursor = conn.cursor()
        dsn_param = conn.get_dsn_parameters()
        query = ("""INSERT INTO user_data(user_name, password, login_count) VALUES (%s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 'private', login_count))
        conn.commit()
        param_string = str(risk_thresh)
        query = ("""INSERT INTO user_activity_log(user_name, query_run, tables_accessed, input_params, login_count) VALUES (%s, %s, %s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 4, "nri_risk, nri_demographics, nri_county", param_string, login_count))
        conn.commit()

    def query_5(risk_thresh, pop_thresh):
        cursor = conn.cursor()
        query = ("""SELECT countyfips, population, riskscore, hospitals
            FROM (
            SELECT COUNT(id) as hospitals, countyfips
            FROM hosp_address_info JOIN nri_risk ON countyfips = stcofips
            JOIN nri_demographics ON nri_risk.stcofips = nri_demographics.stcofips
            WHERE riskscore >= %s AND population >= %s
            GROUP BY countyfips
            ) as hosp_count
            JOIN nri_risk ON countyfips = stcofips JOIN nri_demographics ON nri_risk.stcofips = nri_demographics.stcofips
            ORDER BY population DESC;""")
        cursor.execute(query, (risk_thresh, pop_thresh))
        records = cursor.fetchall()
        headers = ['County FIPS', 'Population', 'Total Risk', 'Number of Hospitals']
        table = [[records[i][0], records[i][1], round(float(records[i][2]),2), records[i][3]] for i in range(0, len(records))]
        print(tabulate(table, headers))
        return records

    def query_5_insert(risk_thresh, pop_thresh):
        cursor = conn.cursor()
        dsn_param = conn.get_dsn_parameters()
        query = ("""INSERT INTO user_data(user_name, password, login_count) VALUES (%s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 'private', login_count))
        conn.commit()
        param_string = str(risk_thresh) + ", " + str(pop_thresh)
        query = ("""INSERT INTO user_activity_log(user_name, query_run, tables_accessed, input_params, login_count) VALUES (%s, %s, %s, %s, %s)""")
        cursor.execute(query, (dsn_param['user'], 5, "hospital_address_info, nri_risk, nri_demographics", param_string, login_count))
        conn.commit()
