import sqlite3
import io
import os
import streamlit as st
database_name = 'final.db'

def create_table(name):
    sqlite_connection = sqlite3.connect(database_name)
    with sqlite_connection as connection:
        cursor = connection.cursor()
        print("Connected to SQLite")

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{name}"  (
            "img_id"	INTEGER,      
            "img_name"	TEXT,
            "img_data"	BLOB,
            PRIMARY KEY("img_id")
        );''')
    

def to_binary(filename):
    '''Convert file data to binary format'''
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_image(name, image_file):
    try:
        sqlite_connection = sqlite3.connect(database_name)
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        sqlite_query = "INSERT INTO images (img_name, img_data) VALUES (?, ?)"
        
        image_data = to_binary(image_file)

        data_tuple = (name, image_data)
        cursor.execute(sqlite_query, data_tuple)
        sqlite_connection.commit()
        
        print("Image inserted successfully as a BLOB into the table " + name)
        
        cursor.close()

    except sqlite3.Error as error:
        print(f"Failed to insert image data into SQLite table {error}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")

def write_file(data, filename):
    '''Convert binary data and write it to disk'''
    with open(filename, 'wb') as file:
        print(type(data.decode()))
        file.write(data.decode())
    print(f"Stored blob data into: {filename}\n")
 
# reading images from database, blob type
def read_image(filename):
    with sqlite3.connect(database_name) as conn:
        cur = conn.cursor()
        cur.execute(f'select img_data from images where img_name = "{filename}"')
        data = cur.fetchone()
        tempstore = io.BytesIO(data[0])
    return tempstore
 
def get_folder_files():
    path = "c:\\Users\\anvik1\\Downloads\\images"
    contents = os.listdir(path)

    for item in contents:
        insert_image(item, path+"\\"+item)

if __name__ == '__main__':
    get_folder_files()
   
