#pip install PyMySQL
import pymysql
from cryptography.fernet import Fernet
import os
from tkinter import filedialog
from dotenv import load_dotenv

def get_config():
    dev = input("Are you developing with a local db? (y/n): ")
    if dev.strip().lower() == "y":

        load_dotenv()

        db_config = {
            "host" : os.getenv("DB_HOST"),
            "user" : os.getenv("DB_USER"),
            "password" : os.getenv("DB_PASSWORD"),
            "database" : os.getenv("DB_NAME")
        }
    else:
        ip = input("ip: ")

        db_config = {
            "host": f"{ip}",
            "port": 25565,
            "user": "user",
            "password": f"{Fernet("_dkff6Kov3V1Olvq8C4AO4EaYFPoXlvQONyH-dUdOM8=".encode()).decrypt("gAAAAABoe3Pq4ND3CITZpkrMvGForJUKwSLJevOzSlOqj4G8eyXkEdCKzhYiBeRddkkjClaGb1e2nqSiyI-ilM4c6G8xGdQANQ==r4IFiHw==".encode()).decode()}",
            "database": "files"
        }

    return db_config


def add_to_db(db_config):

    name = input("Enter name: ")
    description = input("Enter description: ")

    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("All Files", "*.*")]
    )
    file_type = os.path.splitext(file_path)[1]

    if file_type == ".html":
        hostable = 1
    else:
        hostable = 0

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute("""
                INSERT INTO files (name, description, file, file_type, hostable)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, description, file_content, file_type, hostable))
        conn.commit()

    except pymysql.Error as err:
        print(f"There was an unexpected error connecting to the database: {err}")
    except FileNotFoundError:
        print(f"no file found at {file_path}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")


def get_all_from_db(db_config):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute(f"""SELECT * FROM file_hosting.files WHERE id > 0""")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except pymysql.Error as err:
        print(f"There was an unexpected error with your database: {err}")
        return []
    except Exception as e:
        print(f"There was an unexpected error: {e}")
        return []