import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from QR_Generator import QRGenerator


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Generator for Itch.io")
        self.geometry("520x380")
        self.resizable(False, False)

        self.generator = None
        self.browser = "Chrome"
        self.saved_dir = os.getcwd()

        self._create_ui()
        self._update_create_button_state()


    # ------------------------- INTERFAZ -------------------------
    def _create_ui(self):
        tk.Label(self, text="Itch.io URL").place(x=30, y=40)
        tk.Label(self, text="*", fg="red", font=("Arial", 12, "bold")).place(x=95, y=40)

        self.ent_url = tk.Entry(self, width=55)
        self.ent_url.place(x=120, y=40)
        self.ent_url.bind("<KeyRelease>", lambda e: self._update_create_button_state())

        tk.Label(self, text="Browser:").place(x=30, y=75)
        self.cmb_browser = ttk.Combobox(values=["Chrome", "Firefox", "Microsoft Edge"], state="readonly")
        self.cmb_browser.current(0)
        self.cmb_browser.place(x=120, y=75)

        self.btn_folder = ttk.Button(text="Select Folder", command=self._select_folder)
        self.btn_folder.place(x=30, y=110)
        tk.Label(self, text="*", fg="red", font=("Arial", 12, "bold")).place(x=107, y=108)

        self.ent_folder = tk.Entry(self, width=55)
        self.ent_folder.place(x=120, y=110)
        self.ent_folder.bind("<KeyRelease>", lambda e: self._update_create_button_state())

        self.var_logo = tk.IntVar()
        self.cb_logo = tk.Checkbutton(text="Add logo in QR", variable=self.var_logo, command=self._toggle_logo)
        self.cb_logo.place(x=30, y=150)

        self.btn_logo = ttk.Button(text="Select Logo", command=self._select_logo)
        self.ent_logo = tk.Entry(self, width=55)

        self.var_delete = tk.IntVar()
        self.cb_delete = tk.Checkbutton(text="Delete QR images after PDF creation", variable=self.var_delete)
        self.cb_delete.place(x=30, y=180)

        # 🔸 Botón deshabilitado al iniciar
        self.btn_create = ttk.Button(text="Create PDF", command=self._start_thread, state="disabled")
        self.btn_create.place(x=210, y=330)


    # ------------------------- FUNCIONALIDAD -------------------------

    def _update_create_button_state(self):
        """Habilita o deshabilita el botón de 'Create PDF' según los campos rellenos."""
        url_filled = bool(self.ent_url.get().strip())
        folder_filled = bool(self.ent_folder.get().strip())
        if url_filled and folder_filled:
            self.btn_create["state"] = "normal"
        else:
            self.btn_create["state"] = "disabled"

    def _select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.saved_dir = folder
            self.ent_folder.delete(0, tk.END)
            self.ent_folder.insert(0, folder)
            self._update_create_button_state()  # 🔹 <- Añade esta línea


    def _select_logo(self):
        logo = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if logo:
            self.ent_logo.delete(0, tk.END)
            self.ent_logo.insert(0, logo)

    def _toggle_logo(self):
        if self.var_logo.get():
            self.btn_logo.place(x=30, y=210)
            self.ent_logo.place(x=120, y=210)
        else:
            self.btn_logo.place_forget()
            self.ent_logo.place_forget()

    def _start_thread(self):
        url = self.ent_url.get().strip()
        if not url:
            messagebox.showwarning("Error", "Please enter a valid URL.")
            return

        self.generator = QRGenerator()
        self.generator.Set_Url(url)
        self.generator.Set_Webdriver(self.cmb_browser.get())
        self.generator.Set_Save_Directory(self.ent_folder.get() or os.getcwd())
        self.generator.Set_Delete_QR_Folder(bool(self.var_delete.get()))
        if self.var_logo.get():
            logo_path = self.ent_logo.get()
            if not logo_path:
                messagebox.showwarning("Error", "Select a logo image first.")
                return
            self.generator.Set_Add_Logo(True, logo_path)

        self._open_progress_window()

        thread = threading.Thread(target=self._generate_pdf)
        thread.start()
        self._check_thread(thread)

    def _generate_pdf(self):
        try:
            self.generator.Create_PDF()
        except Exception as e:
            self._thread_error = e
        else:
            self._thread_error = None

    def _check_thread(self, thread):
    # Guardamos los mensajes previos para no repetirlos
        if not hasattr(self, "_last_progress_msg"):
            self._last_progress_msg = ""
            self._last_progress_val = -1

        if thread.is_alive():
            new_val = self.generator.Get_Progress_Number()
            new_msg = self.generator.Get_Progress_Message()

            # Solo actualizar si el progreso ha cambiado
            if new_val != self._last_progress_val:
                self.progress["value"] = new_val
                self._last_progress_val = new_val

            # Solo mostrar el mensaje si es nuevo
            if new_msg and new_msg != self._last_progress_msg:
                self._last_progress_msg = new_msg
                self.log_text["state"] = "normal"
                self.log_text.insert(tk.END, new_msg + "\n")
                self.log_text["state"] = "disabled"
                self.log_text.see(tk.END)
                print(new_msg)  # opcional: también lo imprime en consola para depurar

            # volver a comprobar en 0.8 s
            self.after(800, self._check_thread, thread)
        else:
            self._finish_thread()

    def _finish_thread(self):
        if hasattr(self, "_thread_error") and self._thread_error:
            messagebox.showerror("Error", str(self._thread_error))
        else:
            messagebox.showinfo("Success", "PDF successfully created!")
        self.progress_window.destroy()

    # ------------------------- PROGRESO -------------------------
    def _open_progress_window(self):
        self.progress_window = tk.Toplevel(self)
        self.progress_window.title("Generating PDF...")
        self.progress_window.geometry("420x200")

        tk.Label(self.progress_window, text="Please wait...").pack(pady=10)
        self.progress = ttk.Progressbar(self.progress_window, length=350, mode="determinate")
        self.progress.pack(pady=5)

        self.log_text = tk.Text(self.progress_window, height=6, width=50, state="disabled")
        self.log_text.pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("listo")
