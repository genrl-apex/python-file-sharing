#pip install PyMySQL
import pymysql
#pip install python-dotenv
from dotenv import load_dotenv, dotenv_values
import os
from tkinter import filedialog
import tkinter as tk

#load_dotenv()


ip = input("ip: ")

db_config = {
    "host": os.getenv("DB_HOST", f"{ip}"),
    "port": int(os.getenv("DB_PORT", 25565)),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "files")
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
