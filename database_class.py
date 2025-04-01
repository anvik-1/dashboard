import streamlit as st
import sqlite3
import pandas as pd

class dbfunctions:
    def __init__(self, database="final.db"):
        self.database = database  
        self.connection = sqlite3.connect(self.database, check_same_thread=False)  
    
    def inittable(self):
        cursor = self.connection.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS inventory (
            pkey INTEGER PRIMARY KEY AUTOINCREMENT, 
            input1 TEXT, 
            input2 TEXT
        )
        ''')
        self.connection.commit()

    def readsql(self, userstring="SELECT * FROM inventory"):
        with sqlite3.connect(self.database) as connection:
            print("Successfully connected to database")
            cursor = connection.cursor()
            cursor.execute(userstring)
            returnlist = cursor.fetchall()
            print(returnlist)
        return returnlist

    def createrow(self, table_name, columns, values):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] *len(values))
        query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()

    def deleterow(self, tablename, id_name, id_number):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {tablename} WHERE {id_name} = ?", (id_number,))
            connection.commit()


