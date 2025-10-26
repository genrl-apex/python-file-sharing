import tkinter as tk
from connect_db import get_config, get_all_from_db, add_to_db, download_file, open_file

db_config = get_config()

def handle_open_file():
    index = entry.get()
    index = int(index)
    try:
        items = get_all_from_db(db_config)

        if 1 <= index and index <= len(items):
            for idx, item in enumerate(items, start=1):
                if idx == index:
                    name = item[1] or ''
                    extension = item[4] or ''

                    name_with_ext = f"{name}{extension}"
                else:
                    continue

            open_file(db_config, name_with_ext)

        else:
            print("Invalid input. Please enter a valid number.")

    except Exception as e:
        print(e)


root = tk.Tk()
root.geometry("600x500")
root.configure(bg="#212121")

tk.Label(root,
         text="Access the database...\nEnter the number of the file you want to preview/host",
         font=("Helvetica", "16"),
         bg="#212121",
         fg="white"
).place(relx=0.5, y=40, anchor="center")

entry = tk.Entry(root,
         width="40",
         font=("Helvetica", "16"),
         bg="#404040",
         fg="white",
         relief="flat"
)
entry.place(relx=0.5, y=80, anchor="center")

tk.Button(
    root,
    text="Enter",
    width="20",
    font=("Helvetica", "12"),
    bg="#1f538d",
    relief="flat",
    activebackground="#14375e",
    activeforeground="black",
    command=handle_open_file
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