import pymysql
from cryptography.fernet import Fernet
import os
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
import  http.server
import socketserver
from webbrowser import open

PORT = 8000

def make_handler(content):
    class html_handler(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
    return html_handler

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
    

def download_file(db_config, name_with_ext):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        name, ext = os.path.splitext(name_with_ext)

        cursor.execute("SELECT file FROM files WHERE name=%s AND file_type=%s", (name, ext))
        result = cursor.fetchone()

        if result:
            file_data = result[0]

            save_path = filedialog.asksaveasfilename(
                defaultextension=ext,
                initialfile=name_with_ext,
                filetypes=[("All files", "*.*")]
            )

            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                print(f"Downloaded to: {save_path}")
            else:
                print("Save cancelled.")
        else:
            print("File not found in database.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")


def open_in_txt_box():
    print("this will get added i promise :)")

def open_file(db_config, name_with_ext):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        name, ext = os.path.splitext(name_with_ext)

        cursor.execute("SELECT file, file_type, hostable FROM files WHERE name=%s AND file_type=%s", (name, ext))
        result = cursor.fetchone()
        file_data, file_type, hostable = result
        
        if hostable == 1:
            content = file_data.decode("utf-8")

            host = messagebox.askokcancel("Question", "Do you want to host this html file as a website")
            if host == True:

                with socketserver.TCPServer(("", PORT), make_handler(content)) as httpd:
                    print(f"Serving {name_with_ext} at http://localhost:{PORT}")
                    open(f"http://localhost:{PORT}")
                    httpd.serve_forever()

            else:
                print("something went wrong hosting file")
        else:
            open_in_txt_box()

        cursor.close()
        conn.close()

    except pymysql.Error:
        print("something went wrong while connecting to the database!")
