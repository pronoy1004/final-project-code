import psycopg2
import psycopg2.extras
import json
import pandas as pd
import webbrowser
from psycopg2 import sql

class ApplicationQueries():
    
    def __init__(self):

        self.conn = psycopg2.connect()
    def query1(self):
        try:
            query = sql.SQL("""
             """).format(
                )
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            cursor.execute(query)
            r = cursor.fetchall()
            
            
            return

        except Exception as e:
            print("Error : ")
            print(str(e))
            return

    def query2(self):
        try:
            query = sql.SQL("""
             """).format(
                )
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            cursor.execute(query)
            r = cursor.fetchall()
            
            
            return

        except Exception as e:
            print("Error : ")
            print(str(e))
            return

    def query3(self):
        try:
            query = sql.SQL("""
             """).format(
                )
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            cursor.execute(query)
            r = cursor.fetchall()
            
            
            return

        except Exception as e:
            print("Error : ")
            print(str(e))
            return

    def query4(self):
        try:
            query = sql.SQL("""
             """).format(
                )
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            cursor.execute(query)
            r = cursor.fetchall()
            
            
            return

        except Exception as e:
            print("Error : ")
            print(str(e))
            return

    def query5(self):
        county = input("Enter County Name")
        try:
            query = sql.SQL("""
             """).format(
                )
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            cursor.execute(query)
            r = cursor.fetchall()
            
            
            return

        except Exception as e:
            print("Error : ")
            print(str(e))
            return


    