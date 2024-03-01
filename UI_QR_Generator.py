# import tkinter as tk
# from tkinter.filedialog import askopenfilename, asksaveasfilename

# def save_file():
#     """Save the current file as a new file."""
#     filepath = asksaveasfilename(
#         defaultextension=".txt",
#         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
#     )
#     if not filepath:
#         return
#     with open(filepath, mode="w", encoding="utf-8") as output_file:
#         text = txt_edit.get("1.0", tk.END)
#         output_file.write(text)
#     window.title(f"Simple Text Editor - {filepath}")

# def open_file():
#     """Open a file for editing."""
#     filepath = askopenfilename(
#         filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")]
#     )
#     if not filepath:
#         return
#     txt_edit.delete("1.0", tk.END)
#     with open(filepath, mode="r", encoding="utf-8") as input_file:
#         text = input_file.read()
#         txt_edit.insert(tk.END, text)
#     window.title(f"Simple Text Editor - {filepath}")


# window = tk.Tk()
# window.title("QR GENERATOR")

# # window.rowconfigure(0, minsize=800, weight=1)
# # window.columnconfigure(1, minsize=800, weight=1)

# label = tk.Label(text="ITCH.IO URL")
# entry = tk.Entry(window)
# txt_edit = tk.Text(window)
# frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
# btn_open = tk.Button(frm_buttons, text="Open" , command=open_file)
# btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

# btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
# btn_save.grid(row=1, column=0, sticky="ew", padx=5)

# label.grid(row=0, column=0, sticky="ns")
# label.grid(row=0, column=1, sticky="ns")
# frm_buttons.grid(row=1, column=0, sticky="ns")
# txt_edit.grid(row=1, column=1, sticky="nsew")

# window.mainloop()



# from tkinter import filedialog, ttk
# import tkinter as tk
# window = tk.Tk()

# window.title("ITCH.IO QR GENERATOR")
# window.resizable(width=False, height=False)

# frm_URL = tk.Frame(master=window)
# frm_browsers = tk.Frame(master=window)
# frm_Buttons = tk.Frame(master=window)


# lbl_URL = tk.Label(master=frm_URL, text="URL")
# ent_URL = tk.Entry(master=frm_URL, width=320)

# frm_URL.grid(row=0, column=0, padx=10)

# # label.pack()
# # entry_URL.pack()

# # url = entry_URL.get()
# window.mainloop()



# Set up the window
# window = tk.Tk()
# window.title("Temperature Converter")
# window.config(width=3400, height=200)

# window.resizable(width=False, height=False)


# frm_entry = tk.Frame(master=window)

# lbl_url = tk.Label(master=frm_entry, text="Insert URL")
# ent_url = tk.Entry(master=frm_entry, width=20)

# lbl_url.grid(row=0, column=0, sticky="w")
# ent_url.grid(row=0, column=1, sticky="nswe")

# combo = ttk.Combobox()
# combo.place(x=50, y=50)
# combo = ttk.Combobox(state="readonly")
# combo = ttk.Combobox(
#     state="readonly",
#     values=["Python", "C", "C++", "Java"]
# )
# # Create the Fahrenheit entry frame with an Entry
# # widget and label in it
# frm_entry = tk.Frame(master=window)
# ent_temperature = tk.Entry(master=frm_entry, width=10)
# lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")

# # Layout the temperature Entry and Label in frm_entry
# # using the .grid() geometry manager
# ent_temperature.grid(row=0, column=0, sticky="e")
# lbl_temp.grid(row=0, column=1, sticky="w")

# # Create the conversion Button and result display Label
# btn_convert = tk.Button(
#     master=window,
#     text="\N{RIGHTWARDS BLACK ARROW}",
#     command=fahrenheit_to_celsius
# )
# lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

# # Set up the layout using the .grid() geometry manager
# frm_entry.grid(row=0, column=0, padx=10)
# btn_convert.grid(row=0, column=1, pady=10)
# lbl_result.grid(row=0, column=2, padx=10)

# Run the application
# window.mainloop()

from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog

def display_selection():
    # Get the selected value.
    selection = combo.get()
    messagebox.showinfo(
        message=f"The selected value is: {selection}",
        title="Selection"
    )

    print(checkboxImg, checkboxQR)


def openImageOfCenter():
    filename = filedialog.askopenfilename(defaultextension=".png",  filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpeg"), ("All Files", "*.*")])
    if filename:
        # Read and print the content (in bytes) of the file.
        ent_img.delete(0,tk.END)
        ent_img.insert(0,filename)
    else:
        print("No file selected.")

def checkCheckboxImage():
    global checkboxImg
    if (centerImageWanted.get() == 1):
        checkboxImg = True
        print("1")
        show_button(btn_img, 50, 200)
        show_button(ent_img, 150, 200)
    else:
        checkboxImg = False
        hide_button(btn_img)
        hide_button(ent_img)


def checkCheckboxQR():
    global checkboxQR
    if (deleteQrs.get() == 1):
        checkboxQR = True
    else:
        checkboxQR = False

def hide_button(widget): 
    # This will remove the widget from toplevel 
    widget.place_forget() 

def show_button(widget, row, col): 
    # This will recover the widget from toplevel 
    widget.place(x=row, y=col) 
  

window = tk.Tk()
window.config(width=500, height=300)
window.title("Combobox")
combo = ttk.Combobox(
    state="readonly",
    values=["Python", "C", "C++", "Java"],
)
combo.current(0)

combo.place(x=50, y=75)

lbl_url = tk.Label(master=window, text="Insert URL")
lbl_url.place(x=50, y = 50)

ent_url = tk.Entry(master=window, width=50)
ent_url.place(x=120, y = 50)

btn_img = ttk.Button(text="Select Image", command=openImageOfCenter)

ent_img = tk.Entry(master=window, width=50)


centerImageWanted = tk.IntVar()
deleteQrs = tk.IntVar()
cb_Img = tk.Checkbutton(window, text='Añadir imagen central',variable=centerImageWanted, onvalue=1, offvalue=0, command=checkCheckboxImage)
cb_Img.place(x=50, y=100)
cb_QRs = tk.Checkbutton(window, text='Eliminar imagenes de QR generadas',variable=deleteQrs, onvalue=1, offvalue=0, command=checkCheckboxQR)
cb_QRs.place(x=50, y=130)

checkboxImg = False
checkboxQR = False

button = ttk.Button(text="Display selection", command=display_selection)
button.place(x=150, y=100)

window.mainloop()