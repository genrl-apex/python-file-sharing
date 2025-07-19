#pip install PyMySQL
import pymysql
from cryptography.fernet import Fernet
import os
from tkinter import filedialog
import tkinter as tk



ip = input("ip: ")

db_config = {
    "host": f"{ip}",
    "port": 25565,
    "user": "user",
    "password": f"{Fernet("_dkff6Kov3V1Olvq8C4AO4EaYFPoXlvQONyH-dUdOM8=".encode()).decrypt("gAAAAABoe3Pq4ND3CITZpkrMvGForJUKwSLJevOzSlOqj4G8eyXkEdCKzhYiBeRddkkjClaGb1e2nqSiyI-ilM4c6G8xGdQANQ==r4IFiHw==".encode()).decode()}",
    "database": "files"
}



def add_to_db(name, description, file_path, file_type):
    with open(file_path, "rb") as file:
        file_content = file.read()
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute("""
                INSERT INTO files (name, description, file, file_type)
                VALUES (%s, %s, %s, %s)
            """, (name, description, file_content, file_type))
        conn.commit()

    except pymysql.Error as err:
        print(f"There was an unexpected error connecting to the database: {err}")
    except FileNotFoundError:
        print(f"no file found at {file_path}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")


#not currently being used
def get_all_from_db(name, file_path):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute(""" """) #need to add statement
        conn.commit()

    except pymysql.Error as err:
        print(f"There was an unexpected error connecting to the database: {err}")
    except FileNotFoundError:
        print(f"no file found at {file_path}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")
#########################################

name = input("Enter name: ")
description = input("Enter description: ")
file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("All Files", "*.*")]
    )
file_type = os.path.splitext(file_path)[1]
add_to_db(name, description, file_path, file_type)
