import os
import re
import shutil
import time
import qrcode
from urllib.parse import urlparse
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle
from reportlab.lib.units import inch
from PIL import Image as PILImage

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager



class QRGenerator:
    def __init__(self):
        self.URL = None
        self.LOGOPATH = None
        self.WEBDRIVER = None
        self.SAVEDIRECTORY = os.getcwd()

        self.PDFName = "Games_QRs"
        self.AddLogo = False
        self.DeleteQRFolder = False
        self.QRSIZE = 180
        self.FONTSIZE = 15
        self.PROGRESS = 0
        self.PROGRESS_MSG = "Iniciando proceso"

    # ------------------------- CONFIGURACIONES -------------------------
    def Set_Url(self, url): 
        self.URL = url
    def Set_Logo_Path(self, path): 
        self.LOGOPATH = path
    def Set_Webdriver(self, driver): 
        self.WEBDRIVER = driver
    def Set_Add_Logo(self, add_logo, path): 
        self.AddLogo, self.LOGOPATH = add_logo, path
    def Set_Delete_QR_Folder(self, delete): 
        self.DeleteQRFolder = delete
    def Set_Save_Directory(self, path): 
        self.SAVEDIRECTORY = path
    def Get_Progress_Number(self): 
        return self.PROGRESS
    def Get_Progress_Message(self): 
        return self.PROGRESS_MSG

    # ------------------------- FLUJO PRINCIPAL -------------------------
    def Create_PDF(self):
        try:
            self.Change_Working_Directory()
            games = self.Get_Itchio_Data()
            qrs = self.Create_QR_Images(games)
            self.Create_PDF_With_Table(qrs)
            if self.DeleteQRFolder:
                self.Delete_QR_Folders()
            self.PROGRESS, self.PROGRESS_MSG = 100, "PDF creado correctamente ✅"
        except Exception as e:
            print("❌ Error:", e)
            raise e

    # ------------------------- UTILIDADES -------------------------
    def Change_Working_Directory(self):
        folder = os.path.join(self.SAVEDIRECTORY, "Games_QR")
        os.makedirs(folder, exist_ok=True)
        os.chdir(folder)
        self.SAVEDIRECTORY = folder
        print(f"[INFO] Directorio de guardado: {folder}")

    def _create_driver(self):

        """Crea el driver automáticamente según el navegador seleccionado, sin necesidad de instalación manual."""
        match self.WEBDRIVER:
            case "Chrome":
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                opts = ChromeOptions()
                opts.add_argument("--headless")
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
                return driver

            case "Firefox":
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                opts = FirefoxOptions()
                opts.add_argument("--headless")
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=opts)
                return driver

            case "Microsoft Edge":
                from selenium.webdriver.edge.options import Options as EdgeOptions
                opts = EdgeOptions()
                opts.add_argument("--headless")
                opts.add_argument("--disable-gpu")
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=opts)
                return driver

            case _:
                raise ValueError(f"Navegador no reconocido: {self.WEBDRIVER}")

    def _sanitize_filename(self, name):
        return re.sub(r'[<>:"/\\|?*\x00-\x1F]', ' ', name).replace("&amp;", "&")

    # ------------------------- SCRAPING -------------------------
    def Get_Itchio_Data(self):
        self.PROGRESS, self.PROGRESS_MSG = 10, f"Abriendo navegador {self.WEBDRIVER}..."
        driver = self._create_driver()

        self.PROGRESS, self.PROGRESS_MSG = 15, f"Buscando juegos..."
        try:
            driver.get(self.URL)
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            elems = driver.find_elements(By.CSS_SELECTOR, ".label [href]")
            if not elems:
                raise Exception("No se encontraron enlaces de juegos. Verifica la URL o el selector.")
            data = [(e.get_attribute('innerHTML'), e.get_attribute('href')) for e in elems]
            data.sort(key=lambda x: x[0])
            self.PROGRESS, self.PROGRESS_MSG = 50, f"{len(data)} juegos encontrados."
            return data
        finally:
            driver.quit()

    # ------------------------- GENERACIÓN DE QRs -------------------------
    def Create_QR_Images(self, data):
        qr_folder = os.path.join(self.SAVEDIRECTORY, "Qrs")
        os.makedirs(qr_folder, exist_ok=True)
        total = len(data)

        self.PROGRESS_MSG = "Generando imágenes QR..."
        for i, (name, link) in enumerate(data, start=1):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2,
            )
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

            if self.AddLogo and self.LOGOPATH:
                try:
                    logo = PILImage.open(self.LOGOPATH)
                    logo = logo.resize((80, 80))
                    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                    img.paste(logo, pos)
                except Exception as e:
                    print(f"[WARN] No se pudo insertar el logo: {e}")

            filename = self._sanitize_filename(name)
            img.save(os.path.join(qr_folder, f"{filename}.png"))

            self.PROGRESS = int(50 + (i / total) * 40)
            self.PROGRESS_MSG = f"QR {i}/{total} creado..."
        self.PROGRESS, self.PROGRESS_MSG = 90, f"QR {total} creados..."
        return data

    # ------------------------- PDF -------------------------
    def Create_PDF_With_Table(self, data):
        pdf_name = self._get_unique_pdf_name()
        self.PROGRESS_MSG = "Generando PDF con códigos QR..."
        doc = SimpleDocTemplate(pdf_name, rightMargin=5, leftMargin=5, topMargin=5, bottomMargin=5)
        elems, rows = [], []
        tabStyle = [('ALIGN', (0, 0), (-1, -1), 'CENTER')]

        for i, (name, _) in enumerate(data):
            image = Image(os.path.join("Qrs", f"{self._sanitize_filename(name)}.png"), self.QRSIZE, self.QRSIZE)
            if i % 2 == 0:
                rows.append([self._truncate_name(name)])
                rows.append([image])
            else:
                rows[-2].append(self._truncate_name(name))
                rows[-1].append(image)

        table = Table(rows, colWidths=inch * 4)
        table.setStyle(TableStyle(tabStyle))
        elems.append(table)
        self.PROGRESS, self.PROGRESS_MSG = 95, f"PDF generado: {pdf_name}"
        doc.build(elems)

    def _truncate_name(self, name):
        return name[:25] + "..." if len(name) > 28 else name

    def _get_unique_pdf_name(self):
        base = os.path.join(self.SAVEDIRECTORY, f"{self.PDFName}.pdf")
        i, name = 1, base
        while os.path.exists(name):
            name = os.path.join(self.SAVEDIRECTORY, f"{self.PDFName}_{i}.pdf")
            i += 1
        return name

    # ------------------------- LIMPIEZA -------------------------
    def Delete_QR_Folders(self):
        path = os.path.join(self.SAVEDIRECTORY, "Qrs")
        if os.path.isdir(path):
            shutil.rmtree(path)
