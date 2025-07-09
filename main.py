import tkinter as tk
import connect_db as con

root = tk.Tk()
root.geometry("600x500")
root.configure(bg="#212121")

tk.Label(root,
         text="Please enter the name of the site you want to visit",
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
    command=con.host_files
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


scrollbar = tk.Scrollbar(
    frame,
    command=textbox.yview
)
textbox.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
textbox["state"] = "normal"

root.mainloop()