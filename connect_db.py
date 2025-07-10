import mysql.connector
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

db_config = {
    "host" : os.getenv("HOST"),
    "user" : os.getenv("USER"),
    "password" : os.getenv("PASSWORD"),
    "database" : os.getenv("DATABASE")
}


def add_to_db(name, description, file_path, file_type):
    with open(file_path, "rb") as file:
        file_content = file.read()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute("""
                INSERT INTO websites (name, description, file, file_type)
                VALUES (%s, %s, %s, %s)
            """, (name, description, file_content, file_type))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"There was an unexpected error connecting to the database: {err}")
    except FileNotFoundError:
        print(f"no file found at {file_path}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")


def get_all_from_db(name, file_path):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Successfully connected to mysql database")

        cursor.execute(""" """) #need to add statement
        conn.commit()

    except mysql.connector.Error as err:
        print(f"There was an unexpected error connecting to the database: {err}")
    except FileNotFoundError:
        print(f"no file found at {file_path}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")
    

#need to add statements/output for these
def get_files():
    pass

def host_files():
    get_files()
    #need to add the hosting