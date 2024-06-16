import os
from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog
from QR_Generator import QRGenerator
import threading



def Select_Logo_Image():
    filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
    if filename:
        ent_logo.delete(0,tk.END)
        ent_logo.insert(0,filename)

def Open_Progress_Indicator_Window():
    newWindow = tk.Toplevel() 
    newWindow.title("Creating PDF")
    newWindow.geometry("400x125")
    info_label = ttk.Label(master=newWindow, text="Please, wait a moment until the process is done.")
    info_label.place(x = 20, y = 20)
    msg_label = ttk.Label(master=newWindow)
    msg_label.place(x = 20, y = 50)
    progressbar = ttk.Progressbar(master=newWindow, mode='determinate')
    progressbar.place(x=20, y=75, width=350)
    newWindow.focus()
    return newWindow, progressbar, msg_label

 
def Select_Save_Directory():
    global SAVEDIRECTORY
    SAVEDIRECTORY = filedialog.askdirectory()
    if(SAVEDIRECTORY != ""):
        ent_SaveFolder.delete(0,tk.END)
        ent_SaveFolder.insert(0,SAVEDIRECTORY)

def Move_Element(widget, row, col):
    widget.place_forget() 
    widget.place(x=row, y=col) 

def Check_Checkbox_Image():
    if (logoWanted.get() == 1):
        Show_Button(btn_logo, 50, 200)
        Show_Button(ent_logo, 150, 200)
    else:
        Hide_Button(btn_logo)
        Hide_Button(ent_logo)
        ent_logo.delete(0,tk.END)

def Create_PDF():
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
    Enable_Buttons(False) 
    progressWindow, progressBar, msgLabel = Open_Progress_Indicator_Window()
    main_thread = threading.Thread(target=generator.Create_PDF)
    main_thread.start()    
    Schedule_Check(main_thread, progressWindow, progressBar, msgLabel, generator)


prev_val = 0
prev_msg = ""

def Schedule_Check(thread, progressWindow, progressBar, msgLabel, generator):
    global prev_val, prev_msg

    new_val = generator.Get_Progress_Number()
    new_msg = generator.Get_Progress_Message()
    if(prev_val != new_val ):
        progressBar.step( new_val-prev_val)
        prev_val = new_val
    if(prev_msg != new_msg):
        msgLabel.config(text = new_msg)
        prev_msg = new_msg
    window.after(1000, Check_If_Thread_Is_Completed, thread, progressWindow, progressBar, msgLabel, generator)
    

def Check_If_Thread_Is_Completed(thread, progressWindow, progressBar, msgLabel, generator):
    # If the thread has finished, re-enable the button and show a message.
    if not thread.is_alive():
        progressWindow.destroy()
        messagebox.showinfo(
            message="Process finished. The PDF has been created in the selected folder",
            title="PDF Created"
        )   
        Enable_Buttons(True)
        Empty_Fields()
    else:
        # Otherwise check again after one second.
        Schedule_Check(thread, progressWindow, progressBar, msgLabel, generator)
   
def Enable_Buttons(enable):
    fields = [ent_logo, ent_SaveFolder, ent_url,  dropdown,  btn_Create,  btn_logo, btn_SaveFolder, cb_Img,  cb_QRs]
    for field in fields:
        field["state"] = "normal" if enable else "disabled"

def Empty_Fields():
    global prev_val, prev_msg
    ent_SaveFolder.delete(0,tk.END)
    ent_url.delete(0,tk.END)
    ent_logo.delete(0,tk.END)
    deleteQrs.set(0)
    logoWanted.set(0)
    Check_Checkbox_Image()
    prev_val = 0
    prev_msg = ""

def Hide_Button(widget): 
    widget.place_forget() 

def Show_Button(widget, row, col): 
    widget.place(x=row, y=col) 

if __name__ == "__main__":    
    try:
        window = tk.Tk()
        window.title("QR GENERATOR ITCHIO")
        window.config(width=500, height=300)
        window.resizable(False, False)

        SAVEDIRECTORY = os.getcwd()
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

        btn_logo = ttk.Button(text="Select Logo", command = Select_Logo_Image)
        ent_logo = tk.Entry(master=window, width=50)

        btn_SaveFolder = ttk.Button(text="Select Folder", command = Select_Save_Directory)
        btn_SaveFolder.place(x=50, y = 110)

        ent_SaveFolder = tk.Entry(master=window, width=50)
        ent_SaveFolder.place(x=150, y = 110)

        deleteQrs = tk.IntVar()
        cb_QRs = tk.Checkbutton(window, text='Delete QR images generated',variable = deleteQrs, onvalue=1, offvalue=0)
        cb_QRs.place(x=50, y=140)

        logoWanted = tk.IntVar()
        cb_Img = tk.Checkbutton(window, text='Add logo in the QR center',variable = logoWanted, onvalue=1, offvalue=0, command=Check_Checkbox_Image)
        cb_Img.place(x=50, y=170)

        btn_Create = ttk.Button(text="Create PDF", command=Create_PDF)
        btn_Create.place(x=200, y = 250)

        window.mainloop()
    except Exception as error:
      print("An error occurred: ", error) 