import tkinter as tk
from tkinter import filedialog
#from cryptography.fernet import Fernet
import pymysql
import os
from connect_db import get_config, get_all_from_db, add_to_db

db_config = get_config()

add_to_db(db_config)
add_to_db(db_config)
add_to_db(db_config)

root = tk.Tk()
root.geometry("600x500")
root.configure(bg="#212121")

tk.Label(root,
         text="Access the database...",
         font=("Helvetica", "16"),
         bg="#212121",
         fg="white"
).place(relx=0.5, y=40, anchor="center")

tk.Entry(root,
         width="40",
         font=("Helvetica", "16"),
         bg="#404040",
         fg="white",
         relief="flat"
).place(relx=0.5, y=80, anchor="center")

tk.Button(
    root,
    text="Enter",
    width="20",
    font=("Helvetica", "12"),
    bg="#1f538d",
    relief="flat",
    activebackground="#14375e",
    activeforeground="black",
    #command=open_file() need to create open_file(). open file needs to check if the file is hostable (as stored in db) then if it is a html file ask if they want it hosted as a site. if yes host like did with eaglecraft. if no put it in a text box like normal
).place(relx=0.5, y=120, anchor="center")

frame = tk.Frame(
    root,
    bg="#212121"
)
frame.place(relx=0.5, rely=0.6, anchor="center", width=500, height=250)


textbox = tk.Text(
    frame,
    width="60",
    height="15",
    font=("Helvetica", "15"),
    bg="#404040",
    fg="white",
    insertbackground="white",
    relief="flat",
)
def place_in_da_textbox():
    items = get_all_from_db(db_config)

    for idx, item in enumerate(items, start=1):
        name = item[1] or ''
        extension = item[4] or ''
        description = item[2] or ''

        name_with_ext = f"{name}{extension}"
        formatted_line = f"{idx}) {name_with_ext}  -   description: {description}\n"
        textbox.insert(tk.END, formatted_line)

#no interacting with text box          at all.
    textbox.config(state="disabled")
    textbox.bind("<Key>", lambda e: "break")
    textbox.config(cursor="arrow")
    textbox.config(insertontime=0, insertofftime=0)
    textbox.config(insertwidth=0)
    textbox.bind("<B1-Motion>", lambda e: "break")
    textbox.bind("<Double-Button-1>", lambda e: "break")
    textbox.bind("<Triple-Button-1>", lambda e: "break")

def on_click(event):
    index = textbox.index(f"@{event.x},{event.y}")
    line_num = int(index.split('.')[0])
    line_text = textbox.get(f"{line_num}.0", f"{line_num}.end")

    if ") " in line_text and " - " in line_text:
        _, rest = line_text.split(") ", 1)
        name_with_ext, _ = rest.split(" - ", 1)
        name_with_ext = name_with_ext.strip()
        download_file(name_with_ext)

textbox.bind("<Button-1>", on_click)

def download_file(name_with_ext):
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


place_in_da_textbox()

scrollbar = tk.Scrollbar(
    frame,
    command=textbox.yview
)
textbox.config(
    yscrollcommand=scrollbar.set,
    wrap="none"
)

scrollbar_down = tk.Scrollbar(
    frame,
    orient="horizontal",
    command=textbox.xview
)
scrollbar_down.pack(side="bottom", fill="x")

textbox.config(
    xscrollcommand=scrollbar_down.set,
    wrap="none"
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
textbox["state"] = "normal"

root.mainloop()
