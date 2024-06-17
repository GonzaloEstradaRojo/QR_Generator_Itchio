import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from QR_Generator import QRGenerator

class QRGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR GENERATOR ITCHIO")    
        self.config(width=500, height=300)
        self.resizable(False, False)
        self.savedDirectory = os.getcwd()
        self.browser = None # dropdown.get()

        self.prev_val = 0
        self.prev_msg = ""

        self.ent_SaveFolder = None
        self.ent_logo = None
        self.ent_url = None
        self.logoWanted = None
        self.deleteQrs = None
        self.dropdown = None
        self.btn_Create = None
        self.btn_logo = None
        self.btn_SaveFolder = None
        self.cb_Img = None
        self.cb_QRs = None        

        self.Create_UI()
        self.mainloop()

    def Create_UI(self):
        self.Add_URL_Section()
        self.Add_Browser_Dropdown()
        self.Add_Logo_Selector()
        self.Add_Select_Folder_Section()
        self.Add_Delete_QRs_Checkbox()
        self.Add_Logo_Checkbox()
        self.Add_Create_Button()

    def Add_URL_Section(self):
        lbl_url = tk.Label(self, text="Insert URL")
        lbl_url.place(x=50, y = 40)   

        self.ent_url = tk.Entry(self, width=50)
        self.ent_url.place(x=150, y = 40)

    def Add_Browser_Dropdown(self):
        lbl_dropdown = tk.Label(self, text="Select browser")
        lbl_dropdown.place(x=50, y = 75)
        
        self.dropdown = ttk.Combobox(values=["Firefox", "Chrome", "Microsoft Edge"], state="readonly")
        self.dropdown.current(0)
        self.dropdown.place(x=150, y=75)

    def Add_Logo_Selector(self):
        self.btn_logo = ttk.Button(text="Select Logo", command = self.Select_Logo_Image)
        self.ent_logo = tk.Entry(self, width=50)

    def Add_Select_Folder_Section(self):
        self.btn_SaveFolder = ttk.Button(text="Select Folder", command = self.Select_Save_Directory)
        self.btn_SaveFolder.place(x=50, y = 110)

        self.ent_SaveFolder = tk.Entry(self, width=50)
        self.ent_SaveFolder.place(x=150, y = 110)

    def Add_Delete_QRs_Checkbox(self):
        self.deleteQrs = tk.IntVar()
        self.cb_QRs = tk.Checkbutton(self, text='Delete QR images generated', variable = self.deleteQrs, onvalue=1, offvalue=0)
        self.cb_QRs.place(x=50, y=140)

    def Add_Logo_Checkbox(self):
        self.logoWanted = tk.IntVar()
        self.cb_Img = tk.Checkbutton(self, text='Add logo in the QR center', variable = self.logoWanted, onvalue=1, offvalue=0, command = self.Check_Checkbox_Image)
        self.cb_Img.place(x=50, y=170)

    def Add_Create_Button(self):
        self.btn_Create = ttk.Button(text="Create PDF", command = self.Create_PDF)
        self.btn_Create.place(x=200, y = 250)

    def Select_Save_Directory(self):
        self.savedDirectory = filedialog.askdirectory()
        # print("AAA   " + self.SAVEDIRECTORY)
        if(self.savedDirectory != ""):
            self.ent_SaveFolder.delete(0,tk.END)
            self.ent_SaveFolder.insert(0,self.savedDirectory)

    def Select_Logo_Image(self):
        filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
        if filename:
            self.ent_logo.delete(0,tk.END)
            self.ent_logo.insert(0,filename)
    
    def Create_PDF(self):
        self.browser = self.dropdown.get()
        generator = QRGenerator()
        if(self.ent_url.get() == ""):
            messagebox.showwarning(message=f"URL is missing. \nPlease, fill the URL before creating th PDF",title="Populate URL")
            return
        
        generator.Set_Url(self.ent_url.get())
        if(self.logoWanted.get() == 1):
            if(self.ent_logo.get() == ""):
                messagebox.showwarning(message = f"Logo is missing.\nPlease, select an image before creating th PDF",title = "Populate URL")   
                return 
            generator.Set_Add_Logo(True, self.ent_logo.get() )
        
        generator.Set_Delete_QR_Folder(self.deleteQrs.get() == 1)
        generator.Set_Webdriver(self.browser)
        generator.Set_Save_Directory(self.savedDirectory)
        self.Enable_Buttons(False) 
        progressWindow, progressBar, msgLabel = self.Open_Progress_Indicator_Window()
        main_thread = threading.Thread(target=generator.Create_PDF)
        main_thread.start()    
        self.Schedule_Check(main_thread, progressWindow, progressBar, msgLabel, generator)

    def Enable_Buttons(self, enabled):
        fields = [self.ent_logo, self.ent_SaveFolder, self.ent_url,  self.dropdown,  self.btn_Create,  self.btn_logo, self.btn_SaveFolder, self.cb_Img, self.cb_QRs]
        for field in fields:
            field["state"] = "normal" if enabled else "disabled"  
    
    def Open_Progress_Indicator_Window(self):
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
    
    def Schedule_Check(self, thread, progressWindow, progressBar, msgLabel, generator):

        new_val = generator.Get_Progress_Number()
        new_msg = generator.Get_Progress_Message()
        if(self.prev_val != new_val ):
            progressBar.step( new_val - self.prev_val)
            self.prev_val = new_val
        if(self.prev_msg != new_msg):
            msgLabel.config(text = new_msg)
            self.prev_msg = new_msg
        self.after(1000, self.Check_If_Thread_Is_Completed, thread, progressWindow, progressBar, msgLabel, generator)
    
    def Check_If_Thread_Is_Completed(self, thread, progressWindow, progressBar, msgLabel, generator):
        # If the thread has finished, re-enable the button and show a message.
        if not thread.is_alive():
            progressWindow.destroy()
            if(self.prev_val>50):
                messagebox.showinfo(
                    message="Process finished. The PDF has been created in the selected folder",
                    title="PDF Created"
                )   
            self.Enable_Buttons(True)
            self.Empty_Fields()
        else:
            # Otherwise check again after one second.
            self.Schedule_Check(thread, progressWindow, progressBar, msgLabel, generator)
   
    def Empty_Fields(self):
        self.ent_SaveFolder.delete(0,tk.END)
        self.ent_url.delete(0,tk.END)
        self.ent_logo.delete(0,tk.END)
        self.deleteQrs.set(0)
        self.logoWanted.set(0)
        self.Check_Checkbox_Image()
        self.prev_val = 0
        self.prev_msg = ""

    def Check_Checkbox_Image(self):
        if (self.logoWanted.get() == 1):            
            self.btn_logo.place(x=50, y=200)
            self.ent_logo.place(x=150, y=200)
        else:
            self.btn_logo.place_forget()
            self.ent_logo.place_forget()
            self.ent_logo.delete(0,tk.END)

# class ProgressBarWindow:
#     def __init__(self):
#         self.window = tk.Toplevel() 
#         self.window.title("Creating PDF")
#         self.window.geometry("400x125")

if __name__ == "__main__":    
    try:
        QRGeneratorApp()

    except Exception as error:
        print("An error occurred: ", error) 
        messagebox.showwarning(message = f"Something went wrong \n {error}", title = "Error")