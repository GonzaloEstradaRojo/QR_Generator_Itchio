from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog
import os
from QR_Generator import QRGenerator

SAVEDIRECTORY = os.getcwd()
BROWSER = ""

def get_Browser_Selection():
    BROWSER = dropdown.get()

def openImageOfCenter():
    filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
    if filename:
        ent_logo.delete(0,tk.END)
        ent_logo.insert(0,filename)
    else:
        print("No file selected.")

def selectSaveDirectory():
    SAVEDIRECTORY = filedialog.askdirectory()
    print(SAVEDIRECTORY)

def move_button(widget, row, col):
    widget.place_forget() 
    widget.place(x=row, y=col) 

def checkCheckboxImage():
    if (logoWanted.get() == 1):
        show_button(btn_logo, 50, 175)
        show_button(ent_logo, 150, 175)
        move_button(btn_Save, 50, 210)
        move_button(btn_Create, 250, 210)
    else:
        hide_button(btn_logo)
        hide_button(ent_logo)
        ent_logo.delete(0,tk.END)
        move_button(btn_Save, 50, 175)
        move_button(btn_Create, 250, 175)

def createPDF():
    generator = QRGenerator()
    if(ent_url.get() == ""):
        messagebox.showwarning(
            message=f"URL is missing. \nPlease, fill the URL before creating th PDF",
            title="Populate URL"
        )
        return
    # generator.Set_Url("https://itch.io/jam/malagajam-weekend-17/entries")
    generator.Set_Url(ent_url.get())

    if(logoWanted):
        if(ent_logo.get() == ""):
            messagebox.showwarning(
                message=f"Logo is missing.\nPlease, select an image before creating th PDF",
                title="Populate URL"
            )   
            return 
        # generator.Set_Logo_Path("G:\My Drive\Sincronizacion\Programacion\Python\QR_Generator_Itchio\MJW LOGO.png")
        generator.Set_Logo_Path("G:\My Drive\Sincronizacion\Programacion\Python\QR_Generator_Itchio\MJW LOGO.png")
    
    if(deleteQrs):
        generator.Set_Delete_QR_Folder(True)
    else:
        generator.Set_Delete_QR_Folder(False)
        
    generator.Set_Webdriver(BROWSER)
    generator.Set_Save_Directory(SAVEDIRECTORY)
    generator.Create_PDF()

def hide_button(widget): 
    # This will remove the widget from toplevel 
    widget.place_forget() 

def show_button(widget, row, col): 
    # This will recover the widget from toplevel 
    widget.place(x=row, y=col) 
  
window = tk.Tk()
window.title("QR GENERATOR ITCHIO")
window.config(width=500, height=300)

lbl_url = tk.Label(master=window, text="Insert URL")
lbl_url.place(x=50, y = 50)


dropdown = ttk.Combobox(
    state="readonly",
    values=["Firefox", "Chrome", "Microsoft Edge"],
)
dropdown.current(0)
dropdown.place(x=175, y=75)
BROWSER = dropdown.get()

lbl_dropdown = tk.Label(master=window, text="Select browser")
lbl_dropdown.place(x=50, y = 75)

ent_url = tk.Entry(master=window, width=50)
ent_url.place(x=120, y = 50)

btn_logo = ttk.Button(text="Select logo", command=openImageOfCenter)
ent_logo = tk.Entry(master=window, width=50)

button = ttk.Button(text="Get dropdown value", command=get_Browser_Selection)
button.place(x=250, y=100)

logoWanted = tk.IntVar()
cb_Img = tk.Checkbutton(window, text='Añadir imagen central',variable = logoWanted, onvalue=1, offvalue=0, command=checkCheckboxImage)
cb_Img.place(x=50, y=100)

deleteQrs = tk.IntVar()
cb_QRs = tk.Checkbutton(window, text='Eliminar imagenes de QR generadas',variable = deleteQrs, onvalue=1, offvalue=0)
cb_QRs.place(x=50, y=130)

btn_Save = ttk.Button(text="Select Save Directory", command=selectSaveDirectory)
btn_Save.place(x=50, y = 175)

btn_Create = ttk.Button(text="Create PDF", command=createPDF)
btn_Create.place(x=250, y = 175)

window.mainloop()