import os
from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog
from QR_Generator import QRGenerator
import threading
import time

def get_Browser_Selection():
    global BROWSER
    BROWSER = dropdown.get()

def selectLogoImage():
    filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
    if filename:
        ent_logo.delete(0,tk.END)
        ent_logo.insert(0,filename)

def selectSaveDirectory():
    global SAVEDIRECTORY
    SAVEDIRECTORY = filedialog.askdirectory()
    if(SAVEDIRECTORY != ""):
        ent_SaveFolder.delete(0,tk.END)
        ent_SaveFolder.insert(0,SAVEDIRECTORY)


def move_element(widget, row, col):
    widget.place_forget() 
    widget.place(x=row, y=col) 

def checkCheckboxImage():
    if (logoWanted.get() == 1):
        show_button(btn_logo, 50, 200)
        show_button(ent_logo, 150, 200)
    else:
        hide_button(btn_logo)
        hide_button(ent_logo)
        ent_logo.delete(0,tk.END)

def createPDF():
    generator = QRGenerator()
    if(ent_url.get() == ""):
        messagebox.showwarning(
            message=f"URL is missing. \nPlease, fill the URL before creating th PDF",
            title="Populate URL"
        )
        return
    generator.Set_Url(ent_url.get())

    if(logoWanted.get() == 1):
        if(ent_logo.get() == ""):
            messagebox.showwarning(
                message = f"Logo is missing.\nPlease, select an image before creating th PDF",
                title = "Populate URL"
            )   
            return 
        generator.Set_Add_Logo(True, ent_logo.get() )
    
    generator.Set_Delete_QR_Folder(deleteQrs.get() == 1)

        
    generator.Set_Webdriver(BROWSER)
    generator.Set_Save_Directory(SAVEDIRECTORY)
    generator.Create_PDF()

def hide_button(widget): 
    widget.place_forget() 

def show_button(widget, row, col): 
    widget.place(x=row, y=col) 

window = tk.Tk()
window.title("QR GENERATOR ITCHIO")
window.config(width=500, height=300)

SAVEDIRECTORY = os.getcwd()
BROWSER = ""
lbl_url = tk.Label(master=window, text="Insert URL")
lbl_url.place(x=50, y = 40)

ent_url = tk.Entry(master=window, width=50)
ent_url.place(x=150, y = 40)

dropdown = ttk.Combobox(
    state="readonly",
    values=["Firefox", "Chrome", "Microsoft Edge"],
)
dropdown.current(0)
dropdown.place(x=150, y=75)
BROWSER = dropdown.get()

lbl_dropdown = tk.Label(master=window, text="Select browser")
lbl_dropdown.place(x=50, y = 75)

btn_logo = ttk.Button(text="Select Logo", command = selectLogoImage)
ent_logo = tk.Entry(master=window, width=50)

btn_SaveFolder = ttk.Button(text="Select Folder", command = selectSaveDirectory)
btn_SaveFolder.place(x=50, y = 110)

ent_SaveFolder = tk.Entry(master=window, width=50)
ent_SaveFolder.place(x=150, y = 110)

deleteQrs = tk.IntVar()
cb_QRs = tk.Checkbutton(window, text='Delete QR images generated',variable = deleteQrs, onvalue=1, offvalue=0)
cb_QRs.place(x=50, y=140)


logoWanted = tk.IntVar()
cb_Img = tk.Checkbutton(window, text='Add logo in the QR center',variable = logoWanted, onvalue=1, offvalue=0, command=checkCheckboxImage)
cb_Img.place(x=50, y=170)



btn_Create = ttk.Button(text="Create PDF", command=createPDF)
btn_Create.place(x=200, y = 250)

window.mainloop()

# Insertar multithreading 
# Ajsutar UI
# Pensar en cambiar a grid en vez de usar place