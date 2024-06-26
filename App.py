import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from QR_Generator import QRGenerator

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR GENERATOR ITCHIO")    
        self.config(width=500, height=300)
        self.resizable(False, False)
        self.savedDirectory = os.getcwd()
        self.browser = None

        self.prev_val = 0
        self.prev_msg = ""
        self.exception_list = []
        self.generator = None

        self.progressWindow = None
        self.progressBar = None
        self.msg_Label = None

        self.UI_elements = {}
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

        self.UI_elements["ent_url"] = tk.Entry(self, width=50)
        self.UI_elements["ent_url"].place(x=150, y = 40)

    def Add_Browser_Dropdown(self):
        lbl_dropdown = tk.Label(self, text="Select browser")
        lbl_dropdown.place(x=50, y = 75)
        
        self.UI_elements["dropdown"] = ttk.Combobox(values=["Firefox", "Chrome", "Microsoft Edge"], state="readonly")
        self.UI_elements["dropdown"].current(0)
        self.UI_elements["dropdown"].place(x=150, y=75)

    def Add_Logo_Selector(self):
        self.UI_elements["btn_logo"] = ttk.Button(text="Select Logo", command = self.Select_Logo_Image)
        self.UI_elements["ent_logo"] = tk.Entry(self, width=50)

    def Add_Select_Folder_Section(self):
        self.UI_elements["btn_SaveFolder"] = ttk.Button(text="Select Folder", command = self.Select_Save_Directory)
        self.UI_elements["btn_SaveFolder"].place(x=50, y = 110)

        self.UI_elements["ent_SaveFolder"] = tk.Entry(self, width=50)
        self.UI_elements["ent_SaveFolder"].place(x=150, y = 110)

    def Add_Delete_QRs_Checkbox(self):
        self.UI_elements["deleteQrs"] = tk.IntVar()
        self.UI_elements["cb_QRs"] = tk.Checkbutton(self, text='Delete QR images generated', variable = self.UI_elements["deleteQrs"], onvalue=1, offvalue=0)
        self.UI_elements["cb_QRs"].place(x=50, y=140)

    def Add_Logo_Checkbox(self):
        self.UI_elements["logoWanted"] = tk.IntVar()
        self.UI_elements["cb_Img"] = tk.Checkbutton(self, text='Add logo in the QR center', variable = self.UI_elements["logoWanted"], onvalue=1, offvalue=0, command = self.Check_Checkbox_Image)
        self.UI_elements["cb_Img"].place(x=50, y=170)

    def Add_Create_Button(self):
        self.UI_elements["btn_Create"] = ttk.Button(text="Create PDF", command = self.Create_QR_PDF)
        self.UI_elements["btn_Create"].place(x=200, y = 250)

    def Select_Save_Directory(self):
        self.savedDirectory = filedialog.askdirectory()
        if(self.savedDirectory != ""):
            self.UI_elements["ent_SaveFolder"].delete(0,tk.END)
            self.UI_elements["ent_SaveFolder"].insert(0,self.savedDirectory)

    def Select_Logo_Image(self):
        filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
        if filename:
            self.UI_elements["ent_logo"].delete(0,tk.END)
            self.UI_elements["ent_logo"].insert(0,filename)
    
    def Thread_Target(self):
        try:
            if(self.UI_elements["ent_url"].get() == ""):
                self.exception_list.append("URL is missing. \nPlease, fill the URL before creating th PDF")
                return
            
            self.generator.Set_Url(self.UI_elements["ent_url"].get())
            if(self.UI_elements["logoWanted"].get() == 1):
                logoDirectory = self.UI_elements["ent_logo"].get()
                if(logoDirectory == ""):
                    self.exception_list.append("Logo is missing.\nPlease, select an image before creating th PDF")   
                    return 
                self.generator.Set_Add_Logo(True, logoDirectory)
            self.generator.Set_Delete_QR_Folder(self.UI_elements["deleteQrs"].get() == 1)
            self.generator.Set_Webdriver(self.browser)
            self.generator.Set_Save_Directory(self.savedDirectory)
            self.Enable_Buttons(False) 
            self.generator.Create_PDF()
        except Exception as error:
            self.exception_list.append(error)


    def Create_QR_PDF(self):
        try:
            self.generator = QRGenerator()
            self.browser = self.UI_elements["dropdown"].get()
            self.Open_Progress_Indicator_Window()
            main_thread = threading.Thread(target = self.Thread_Target)
            main_thread.start()   
            self.Schedule_Check(main_thread)
        except Exception as error:
            self.Enable_Buttons(True)
            self.Empty_Fields()
            messagebox.showwarning(message = f"Something went wrong. Try again \n{error}", title = "Error")


    def Enable_Buttons(self, enabled):
        fields = [self.UI_elements["ent_logo"], self.UI_elements["ent_SaveFolder"], self.UI_elements["ent_url"],  self.UI_elements["dropdown"],  self.UI_elements["btn_Create"],  self.UI_elements["btn_logo"], self.UI_elements["btn_SaveFolder"], self.UI_elements["cb_Img"], self.UI_elements["cb_QRs"]]
        for field in fields:
            field["state"] = "normal" if enabled else "disabled"  
    
    def Open_Progress_Indicator_Window(self):
        self.progressWindow = tk.Toplevel() 
        self.progressWindow.title("Creating PDF")
        self.progressWindow.geometry("400x125")

        info_label = ttk.Label(master = self.progressWindow, text="Please, wait a moment until the process is done.")
        info_label.place(x = 20, y = 20)

        self.msg_Label = ttk.Label(master = self.progressWindow)
        self.msg_Label.place(x = 20, y = 50)

        self.progressBar = ttk.Progressbar(master = self.progressWindow, mode='determinate')
        self.progressBar.place(x=20, y=75, width=350)

        self.progressWindow.focus()
    
    def Schedule_Check(self, thread):
        new_val = self.generator.Get_Progress_Number()
        new_msg = self.generator.Get_Progress_Message()
        if(self.prev_val != new_val ):
            self.progressBar.step(new_val - self.prev_val)
            self.prev_val = new_val
        if(self.prev_msg != new_msg):
            self.msg_Label.config(text = new_msg)
            self.prev_msg = new_msg
        self.after(1000, self.Check_If_Thread_Is_Completed, thread)

            

    
    def Check_If_Thread_Is_Completed(self, thread):
        # If the thread has finished, re-enable the button and show a message.
        if not thread.is_alive():
            self.progressWindow.destroy()
            if self.exception_list:
                error_message = self.exception_list[0]
                messagebox.showwarning(message=f"Something went wrong.\n{error_message}", title="Error")
            elif(self.prev_val>50):
                messagebox.showinfo(message="Process finished. The PDF has been created in the selected folder", title="PDF Created")   
            self.Enable_Buttons(True)
            self.Empty_Fields()                
        else:
            # Otherwise check again after one second.
            self.Schedule_Check(thread)
        
    def Empty_Fields(self):
        self.UI_elements["ent_SaveFolder"].delete(0,tk.END)
        self.UI_elements["ent_url"].delete(0,tk.END)
        self.UI_elements["ent_logo"].delete(0,tk.END)
        self.UI_elements["deleteQrs"].set(0)
        self.UI_elements["logoWanted"].set(0)
        self.Check_Checkbox_Image()
        self.prev_val = 0
        self.prev_msg = ""

    def Check_Checkbox_Image(self):
        if (self.UI_elements["logoWanted"].get() == 1):            
            self.UI_elements["btn_logo"].place(x=50, y=200)
            self.UI_elements["ent_logo"].place(x=150, y=200)
        else:
            self.UI_elements["btn_logo"].place_forget()
            self.UI_elements["ent_logo"].place_forget()
            self.UI_elements["ent_logo"].delete(0,tk.END)

if __name__ == "__main__":    
    try:
        App()
    except Exception as error:
        messagebox.showwarning(message = f"Something went wrong \n{error}", title = "Error")