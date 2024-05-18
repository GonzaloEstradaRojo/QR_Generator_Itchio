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

def openProgressIndicatorWindow():
    # Toplevel object which will 
    # be treated as a new window
    newWindow = tk.Toplevel()
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Creating PDF")
    print("Abro")

    # sets the geometry of toplevel
    newWindow.geometry("400x125")
    info_label = ttk.Label(master=newWindow, text="The PDF is being created. \nPlease, wait a moment until the process is done.")
    info_label.place(x = 20, y = 20)
    progressbar = ttk.Progressbar(master=newWindow, mode="indeterminate")
    progressbar.place(x=20, y=70, width=350)

    progressbar.start()


    progressbar.start()
    newWindow.focus()
    return newWindow

def closeProgressIndicatorWindow(window):
    print("Cierro")
    window.destroy()
 
def selectSaveDirectory():
    global SAVEDIRECTORY
    SAVEDIRECTORY = filedialog.askdirectory()
    print("DIRE "+ SAVEDIRECTORY)
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
    enableButtons(False) 

    progressWindow = openProgressIndicatorWindow()
    t = threading.Thread(target=generator.Create_PDF)
    t.start()
    schedule_check(t, progressWindow)

def schedule_check(t, progressWindow):
    window.after(1000, check_if_done, t, progressWindow)

def check_if_done(t, progressWindow):
    # If the thread has finished, re-enable the button and show a message.
    if not t.is_alive():
        progressWindow.destroy()
        messagebox.showinfo(
            message="Process finished. The PDF has been created in the selected folder",
            title="PDF Created"
        )   
        enableButtons(True)
        emptyFields()

    else:
        # Otherwise check again after one second.
        schedule_check(t, progressWindow)
   
def enableButtons(enable):
    ent_logo["state"] = "normal" if enable else "disabled"
    ent_SaveFolder["state"] = "normal" if enable else "disabled"
    ent_url["state"] = "normal" if enable else "disabled"
    
    dropdown["state"] = "normal" if enable else "disabled"

    btn_Create["state"] = "normal" if enable else "disabled"
    btn_logo["state"] = "normal" if enable else "disabled"
    btn_SaveFolder["state"] = "normal" if enable else "disabled"
    
    cb_Img["state"] = "normal" if enable else "disabled"
    cb_QRs["state"] = "normal" if enable else "disabled"


def emptyFields():
    ent_SaveFolder.delete(0,tk.END)
    ent_url.delete(0,tk.END)
    ent_logo.delete(0,tk.END)
    deleteQrs.set(0)
    logoWanted.set(0)
    checkCheckboxImage()


def hide_button(widget): 
    widget.place_forget() 

def show_button(widget, row, col): 
    widget.place(x=row, y=col) 


if __name__ == "__main__":    
    try:
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
    except Exception as error:
      print("An error occurred: ", error) 